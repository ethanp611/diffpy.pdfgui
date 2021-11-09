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

_instructions = """Mouse Controls:>
L. Click: Select atoms for next spin assignment
R. Click: Undo previous spin assignments
Keyboard Controls:
Enter: Assign Spins after selecting
t: Toggle non-magnetic atoms
b: Toggle bounding box
g: Toggle plot grid
n: Toggle plotted numbers on axes ticks
f: Enter fullscreen mode
Escape: Exit Program
CTRL +/CTRL -: Zoom in or out
U/D Arrows: Change atom size
R/L Arrows: Change vector length"""


class DialogInstructions(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyDialog.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetSize((280, 300))
        self.SetTitle("Instructions")

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_3, 0, wx.EXPAND, 0)

        label_instructions = wx.StaticText(self, wx.ID_ANY, "")
        label_instructions.SetLabel(_instructions)
        sizer_3.Add(label_instructions, 0, 0, 0)

        sizer_2 = wx.StdDialogButtonSizer()
        sizer_1.Add(sizer_2, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 0)

        self.button_OK = wx.Button(self, wx.ID_OK, "")
        self.button_OK.SetDefault()
        sizer_2.AddButton(self.button_OK)

        sizer_2.Realize()

        self.SetSizer(sizer_1)

        self.SetAffirmativeId(self.button_OK.GetId())

        self.Layout()
        # end wxGlade
        self.Bind(wx.EVT_CHAR_HOOK, self.onPressI)

    def onPressI(self, event):
        if event.GetKeyCode() == 73:  # Detects if "i" was pressed
            self.Destroy()
            return

# end of class DialogInstructions

##### testing code ###########################################################


if __name__ == "__main__":
    app = wx.App()
    dialog = DialogInstructions(None, -1, "")
    dialog.ShowModal()
