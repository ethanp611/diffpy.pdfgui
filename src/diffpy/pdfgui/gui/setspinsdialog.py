#!/usr/bin/env python
##############################################################################
#
# PDFgui            by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2006 trustees of the Michigan State University.
#                   All rights reserved.
#
# File coded by:    Elizabeth Vargas
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################

import random
import wx
import re
import numpy as np


class DialogSetSpins(wx.Dialog):
    '''"Mag Viewer Set Spins" Dialog: '''

    def __init__(self, *args, **kwds):
        # begin wxGlade: DialogSetSpins.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetSize((290, 410))
        self.SetTitle("Set Spins")

        sizer_main = wx.FlexGridSizer(10, 1, 4, 4)

        self.labelSpinVector = wx.StaticText(self, wx.ID_ANY, "Spin Vector\nFormat: a,b,c")
        sizer_main.Add(self.labelSpinVector, 0, wx.BOTTOM | wx.EXPAND, 20)

        self.textCtrlSpinVector = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        sizer_main.Add(self.textCtrlSpinVector, 0, 0, 0)

        self.checkboxCrystalCoords = wx.CheckBox(self, wx.ID_ANY, "Crystallographic Coordinates (a, b, c)")
        sizer_main.Add(self.checkboxCrystalCoords, 0, 0, 0)

        self.labelMagnitude = wx.StaticText(self, wx.ID_ANY, "Magnitude\n(Optional: will default to unit length)")
        sizer_main.Add(self.labelMagnitude, 0, wx.BOTTOM, 20)

        self.textCtrlMagnitude = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        sizer_main.Add(self.textCtrlMagnitude, 0, 0, 0)

        self.labelPropVec = wx.StaticText(self, wx.ID_ANY, "Propagation Vector\nFormat: k1,k2,k3\n(Optional: will default to (0, 0, 0))")
        sizer_main.Add(self.labelPropVec, 0, 0, 0)

        self.textCtrlPropVec = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        sizer_main.Add(self.textCtrlPropVec, 0, 0, 0)

        self.labelMultProps = wx.StaticText(self, wx.ID_ANY, "For Multiple Propagation Vectors:\ninsert in tuples of 3, delimited by commas:\nEx: (0,0.5,0.5), (1,0,0.5), ...")
        sizer_main.Add(self.labelMultProps, 0, 0, 0)

        sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(sizer_buttons, 1, wx.ALIGN_CENTER, 0)

        self.buttonSetSpin = wx.Button(self, wx.ID_ANY, "Set Spin")
        sizer_buttons.Add(self.buttonSetSpin, 0, 0, 0)

        self.buttonBack = wx.Button(self, wx.ID_OK, "Go Back")
        sizer_buttons.Add(self.buttonBack, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.SetSizer(sizer_main)

        self.Layout()

        self.Bind(wx.EVT_CHECKBOX, self.onCheckCrystalCoords, self.checkboxCrystalCoords)
        self.Bind(wx.EVT_BUTTON, self.onSetSpin, self.buttonSetSpin)
        # end wxGlade
        self.parent = args[0]
        self.__customProperties()

    def __customProperties(self):
        self.multiple_props = re.compile(
            r"^(\({1}((\d+\.{1}\d+|\d+\/{1}\d+|\d+|.\d+),){2}(\d+\.{1}\d+|\d+\/{1}\d+|\d+|.\d+)\){1},)*(\({1}((\d+\.{1}\d+|\d+\/{1}\d+|\d+|.\d+),){2}(\d+\.{1}\d+|\d+\/{1}\d+|\d+|.\d+)\){1})$")
        self.single_prop = re.compile(
            r"^((\d+\.{1}\d+|\d+\/{1}\d+|\d+|.\d+),){2}(\d+\.{1}\d+|\d+\/{1}\d+|\d+|.\d+)$")
        self.save = {}

    def onCheckCrystalCoords(self, event):
        """Set labelSpinVector to appropriate text"""

        if self.checkboxCrystalCoords.GetValue():
            self.labelSpinVector.SetLabel("Spin Vector\nFormat: a,b,c")
        else:
            self.labelSpinVector.SetLabel("Spin Vector\nFormat: sx,sy,sz")

    def resetLabels(self):
        self.labelMagnitude.SetLabel(
            "Magnitude\n(Optional: will default to unit length)")
        self.labelSpinVector.SetLabel("Spin Vector\nFormat: sx,sy,sz")
        self.labelPropVec.SetLabel(
            "Propagation Vector\nFormat: k1,k2,k3\n(Optional: will default to (0, 0, 0))")

    def onSetSpin(self, event):
        """check textCtrl inputs and display error messages if invalid, else set spins"""

        self.resetLabels()

        # check inputs and give messages
        if self.textCtrlMagnitude.GetValue() != "":
            try:
                mag = float(eval(self.textCtrlMagnitude.GetValue()))
            except:
                self.labelMagnitude.SetLabel(
                    "Magnitude\n(Optional: will default to unit length)\nMagnitude must be integer or decimal!")
                return
        else:
            mag = 1

        ### try to read vector and correct format
        text = self.textCtrlSpinVector.GetValue().replace("]", ")").replace("[", "(").replace(
            "{", "(").replace("}", ")").replace(" ", "").replace("\t", "").replace("\n", "")

        if (self.single_prop.search(text)) or (self.single_prop.search(text[1:-1]) and text[0] == "(" and text[-1] == ")"):
            text = text.replace("(", "").replace(")", "").split(",")
            x = float(eval(text[0]))
            y = float(eval(text[1]))
            z = float(eval(text[2]))

        else:
            if self.checkboxCrystalCoords.GetValue():
                self.labelSpinVector.SetLabel(
                    "Spin Vector\nFormat: a,b,c\nEntry did not match the format.  Try again.")
            else:
                self.labelSpinVector.SetLabel(
                    "Spin Vector\nFormat: sx,sy,sz\nEntry did not match the format.  Try again.")
            return

        ### check prop vec
        prop = self.textCtrlPropVec.GetValue().replace("]", ")").replace("[", "(").replace(
            "{", "(").replace("}", ")").replace(" ", "").replace("\t", "").replace("\n", "")

        if prop == "":
            prop_vec = [[0, 0, 0]]

        elif self.multiple_props.search(prop):
            d = prop.split("),(")
            prop_vec = []
            for i in range(len(d)):
                l = d[i].replace("(", "").replace(")", "").split(",")
                l = [float(eval(l[0])), float(eval(l[1])), float(eval(l[2]))]
                prop_vec += [l]

        elif (self.single_prop.search(prop)) or (self.single_prop.search(prop[1:-1]) and prop[0] == "(" and prop[-1] == ")"):

            prop = prop.replace("(", "").replace(")", "").split(",")
            p1 = float(eval(prop[0]))
            p2 = float(eval(prop[1]))
            p3 = float(eval(prop[2]))
            prop_vec = [[p1, p2, p3]]

        else:

            self.labelPropVec.SetLabel(
                "Propagation Vector\nFormat: k1,k2,k3\n(Optional: will default to (0, 0, 0))\nEntry did not match format for either single<br>or multiple propagation vectors.\nTry again.")
            return

        # if valid, set spin
        self.parent.save['spin vector'] = np.array([x, y, z])
        self.parent.save['magnitude'] = mag
        self.parent.save['crystal coords checked'] = self.checkboxCrystalCoords.GetValue(
        )
        self.parent.save['prop vec'] = prop_vec
        self.Close()


# end of class DialogSetSpins

##### testing code ###########################################################

if __name__ == "__main__":
    app = wx.App()
    dialog = DialogSetSpins(None, -1, "")
    dialog.ShowModal()
