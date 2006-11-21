#!/usr/bin/env py
########################################################################
#
# PDFgui            by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2006 trustees of the Michigan State University.
#                   All rights reserved.
#
# File coded by:    Chris Farrow
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
########################################################################

# -*- coding: ISO-8859-1 -*-
# generated by wxGlade 0.4 on Mon Apr 17 15:51:59 2006

import wx
from wxExtensions.listctrls import KeyEventsListCtrl
from wxExtensions.validators import TextValidator, FLOAT_ONLY
import sys
from pdfpanel import PDFPanel
import os.path
from pdfguiglobals import iconsDir

# TODO - After changing the panel with wxglade, some things must be changed by
# hand.
# 1) The declaration of the quickPlotButton does not know where the icons are
# kept. Replace the declaration with the following lines.
#       qpicon = wx.Bitmap(os.path.join(iconsDir,"datasetitem.png"))
#       self.quickPlotButton = wx.BitmapButton(self, -1, qpicon)


class PlotPanel(wx.Panel, PDFPanel):
    def __init__(self, *args, **kwds):
        PDFPanel.__init__(self)
        # begin wxGlade: PlotPanel.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.sizer_3_staticbox = wx.StaticBox(self, -1, "X")
        self.sizer_4_staticbox = wx.StaticBox(self, -1, "Y")
        self.sizer_7_staticbox = wx.StaticBox(self, -1, "Quick Plot")
        qpicon = wx.Bitmap(os.path.join(iconsDir,"datasetitem.png"))
        self.quickPlotButton = wx.BitmapButton(self, -1, qpicon)
        self.xDataText = wx.StaticText(self, -1, "Select x data")
        self.xDataCombo = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.yDataList = KeyEventsListCtrl(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.offsetLabel = wx.StaticText(self, -1, "offset", style=wx.ALIGN_RIGHT)
        self.offsetTextCtrl = wx.TextCtrl(self, -1, "3")
        self.static_line_1 = wx.StaticLine(self, -1)
        self.plotButton = wx.Button(self, -1, "Plot")
        self.resetButton = wx.Button(self, -1, "Reset")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.onQuickPlot, self.quickPlotButton)
        self.Bind(wx.EVT_BUTTON, self.onPlot, self.plotButton)
        self.Bind(wx.EVT_BUTTON, self.onReset, self.resetButton)
        # end wxGlade
        self.__customProperties()

    def __set_properties(self):
        # begin wxGlade: PlotPanel.__set_properties
        self.SetSize((450, 600))
        self.quickPlotButton.SetSize(self.quickPlotButton.GetBestSize())
        self.xDataCombo.SetSelection(-1)
        self.offsetLabel.SetToolTipString("The vertical gap between stacked plots")
        self.plotButton.SetToolTipString("Plot the selected data")
        self.plotButton.SetDefault()
        self.resetButton.SetToolTipString("Reset the plot configuration")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: PlotPanel.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.StaticBoxSizer(self.sizer_4_staticbox, wx.HORIZONTAL)
        sizer_3 = wx.StaticBoxSizer(self.sizer_3_staticbox, wx.HORIZONTAL)
        sizer_7 = wx.StaticBoxSizer(self.sizer_7_staticbox, wx.HORIZONTAL)
        sizer_7.Add(self.quickPlotButton, 1, wx.ALL|wx.ADJUST_MINSIZE, 5)
        sizer_1.Add(sizer_7, 0, wx.EXPAND, 0)
        sizer_3.Add(self.xDataText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        sizer_3.Add((1, 1), 1, wx.ADJUST_MINSIZE, 0)
        sizer_3.Add(self.xDataCombo, 1, wx.ALL|wx.ADJUST_MINSIZE, 5)
        sizer_1.Add(sizer_3, 0, wx.EXPAND, 0)
        sizer_4.Add(self.yDataList, 1, wx.ALL|wx.EXPAND, 5)
        sizer_1.Add(sizer_4, 1, wx.EXPAND, 0)
        sizer_6.Add(self.offsetLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        sizer_6.Add(self.offsetTextCtrl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 5)
        sizer_1.Add(sizer_6, 0, wx.EXPAND, 0)
        sizer_1.Add(self.static_line_1, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 5)
        sizer_2.Add((1, 1), 1, wx.ADJUST_MINSIZE, 0)
        sizer_2.Add(self.plotButton, 0, wx.ALL|wx.ADJUST_MINSIZE, 5)
        sizer_2.Add(self.resetButton, 0, wx.ALL|wx.ADJUST_MINSIZE, 5)
        sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        # end wxGlade

    # USER CONFIGURATION CODE #################################################
    def __customProperties(self):
        """Custom Properties go here."""
        self.yDataList.InsertColumn(0, "Y data")
        self.offsetTextCtrl.SetValidator(TextValidator(FLOAT_ONLY,allowNeg=True))

        # Testing Code. Comment or delete this block when finished.
        #self.yDataList.InsertStringItem(sys.maxint, "y1")
        #self.yDataList.InsertStringItem(sys.maxint, "y2")
        #self.yDataList.InsertStringItem(sys.maxint, "y3")
        #self.yDataList.InsertStringItem(sys.maxint, "y4")
        #self.yDataList.InsertStringItem(sys.maxint, "y5")
        # Initialize the sorter.
        #self.yDataList.makeIDM()
        #self.yDataList.initializeSorter()

        return

    def enableWidgets(self, on=True):
        """Enable or disable the widgets."""
        self.quickPlotButton.Enable(on)
        self.xDataCombo.Enable(on)
        self.yDataList.Enable(on)
        self.offsetTextCtrl.Enable(on)
        self.resetButton.Enable(on)
        self.plotButton.Enable(on)
        return

    def updateWidgets(self):
        """Enable or disable certain widgets depending upon what is selected in
        the tree and in the plotting widgets."""
        selections = self.treeCtrlMain.GetSelections()

        if selections:
            self.enableWidgets()

            # QUICKPLOT
            # Disable quickplot if there is more than one tree node selected or if
            # any selected node is not a 'dataset' node.
            if len(selections) != 1:
                self.quickPlotButton.Enable(False)
            elif self.treeCtrlMain.GetNodeType(selections[0]) != 'dataset':
                self.quickPlotButton.Enable(False)
            else:
                self.quickPlotButton.Enable(True)

            selectiontype = self.treeCtrlMain.GetNodeType(selections[0])
            # Since 'dataset' and 'calculation' items are treated the same, just
            # replace 'calculation' with 'dataset'.

            # X-DATA
            # Setup the xDataCombo
            # r     -   dataset, calculation
            # step  -   All item types.
            # doping,temperature,index
            #       -   All item types, but only if mutiple selections are chosen
            #            from different fits
            # cdata.getXNames() will provide the above names, except that 'step'
            # and 'index' has to be added manually, and x,T have to be removed
            # manually if they don't belong.
            refs = [self.treeCtrlMain.GetControlData(node) for node in
            selections]
            if selectiontype == 'calculation':
                xdata = []
            else:
                xdata = ['step', 'index']

            for cdata in refs:
                xdata.extend(cdata.getXNames())
            xdata = dict.fromkeys(xdata).keys()

            # Remove 'doping' and 'temperature' to xDataCombo if there are not
            # multiple selections with different fit parents.
            parents = dict.fromkeys(map(self.treeCtrlMain.GetItemText,
                    [self.treeCtrlMain.GetFitRoot(sel) for sel in selections]))
            if len(parents) == 1:
                if 'temperature' in xdata: xdata.remove('temperature')
                if 'doping' in xdata: xdata.remove('doping')
                try:
                    xdata.remove('index')
                except ValueError:
                    pass
            xdata.sort()
            self.xDataCombo.Clear()

            # Fill the xDataCombo
            for item in xdata:
                self.xDataCombo.Append(item)

            # Y-DATA
            ydata = []
            for cdata in refs:
                ydata.extend(cdata.getYNames())
            ydata = dict.fromkeys(ydata).keys()

            # Make the parameter entries a bit more presentable.
            yvals = ["@%i"%item for item in ydata if isinstance(item, int)]
            yother = [item for item in ydata if not isinstance(item, int)]
            yvals.extend(yother)
            yvals.sort()

            # Fill the List
            self.yDataList.DeleteAllItems()
            for val in yvals:
                self.yDataList.InsertStringItem(sys.maxint, str(val))
            self.yDataList.makeIDM()
            self.yDataList.initializeSorter()

        else: # there are no selections
            self.enableWidgets(False)

        return

    def getSelectedYVals(self):
        """Get the y-values selected in the y-value ListCtrl."""
        yvals = []
        item = self.yDataList.GetFirstSelected()
        first_item = item
        while item != -1:
            name = self.yDataList.GetItemText(item)
            yvals.append(name)
            item = self.yDataList.GetNextSelected(item)
        return yvals

    def checkTreeSelections(self):
        """Make sure that the tree selections are appropriate for plotting.

        Make sure that all selections are the same type. If not, then the other
        selections are unselected.
        """
        selections = self.treeCtrlMain.GetSelections()
        if not selections: return

        # Get the type of the first valid node
        nodetype = self.treeCtrlMain.GetNodeType(selections[0])

        # Now deselect all nodes of the wrong type
        for node in selections:
            if nodetype != self.treeCtrlMain.GetNodeType(node):
                self.treeCtrlMain.SelectItem(node, False)

        return

    # EVENT CODE #############################################################
    def onTreeSelChanged(self, event):
        """This handles tree selections when in 'plotting' mode.
        
        This method gets called whenever an item is selected from treeCtrlMain
        when the program is in 'plotting' mode. It fills in the xDataCombo and
        yDataList.
        """
        self.updateWidgets()
        return

    def onQuickPlot(self, event): # wxGlade: PlotPanel.<event_handler>
        """Quickly plot the Gobs, Gfit, and Gdiff for a selected dataset."""
        selections = self.treeCtrlMain.GetSelections()
        if len(selections) != 1: return
        node = selections[0]
        refs = [self.treeCtrlMain.GetControlData(node)]
        xval = 'r'
        yvals = ['Gcalc', 'Gtrunc', 'Gdiff']
        offset = 0
        self.mainPanel.control.plot(xval, yvals, refs, shift=offset)
        return

    def onPlot(self, event): # wxGlade: PlotPanel.<event_handler>
        """Plot some stuff."""
        selections = self.treeCtrlMain.GetSelections()
        refs = [self.treeCtrlMain.GetControlData(node) for node in selections]
        xval = self.xDataCombo.GetValue()
        temp = self.getSelectedYVals()
        # Clean up some formatting so the control can understand this.
        yvals = [ int(par[1:]) for par in temp if par[0] == '@']
        yvals.extend([val for val in temp if val[0] != '@'])
        offset = self.offsetTextCtrl.GetValue()
        # FIXME - The program should select this value in an intelligent way
        if offset == "auto":
            offset = 3.0
        else:
            offset = float(offset)

        self.mainPanel.control.plot(xval, yvals, refs, shift=offset)
        return

    def onReset(self, event): # wxGlade: PlotPanel.<event_handler>
        """Reset everything."""
        self.xDataCombo.SetSelection(wx.NOT_FOUND)
        self.yDataList.clearSelections()
        self.offsetTextCtrl.SetValue("auto")
        self.refresh()
        return

    # Methods overloaded from PDFPanel
    def refresh(self):
        """Refresh this panel."""
        #self.treeCtrlMain.UnselectAll()
        #self.xDataCombo.Clear()
        #self.yDataList.DeleteAllItems()
        #self.enableWidgets(False)
        self.checkTreeSelections()
        self.updateWidgets()
        return

    # This validator is designed exclusively for the offsetTextCtrl
    #class OffsetValidator(wx.PyValidator):
    #    """This validator allows non-negative floats and the word 'auto'"""
    #    def __init__(self):
    #        wx.PyValidator.__init__(self)
    #        self.Bind(wx.EVT_CHAR, self.OnChar)
    #        return

    #    def Clone(self):
    #        return PlotPanel.OffsetValidator()

    #    def Validate(self, win):
    #        tc = self.GetWindow()
    #        val = tc.GetValue()
    #        try:
    #            x = float(val)
    #            if x < 0: return False
    #        except ValueError:
    #            if val != "auto"[:len(val)]:
    #                return False
    #        except:
    #            return False
    #        return True

    #    def OnChar(self, event):
    #        key = event.KeyCode()

    #        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
    #            event.Skip()
    #            return

    #        win = self.GetWindow()
    #        val = win.GetValue()
    #        i = win.GetInsertionPoint()
    #        newval = val[:i]+chr(key)+val[i:]
    #        try:
    #            # Skip the event if the text is a float
    #            x = float(newval+"1") # Catches "1e", a float to be
    #            if x >= 0: 
    #                event.Skip()
    #                return
    #        except ValueError:
    #            # Skip the event if the word is in the word 'auto'
    #            if newval.lower() in "auto"[:len(newval)]:
    #                event.Skip()
    #                return
    #        except:
    #            pass
    #        return
    # end of class OffsetValidator

# end of class PlotPanel

__id__ = "$Id$"
