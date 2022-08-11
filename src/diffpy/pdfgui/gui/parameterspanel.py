
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##############################################################################
#
# PDFgui            by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2006 trustees of the Michigan State University.
#                   All rights reserved.
#
# File coded by:    Dmitriy Bryndin, Chris Farrow
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################


# Parameters panel
# Dmitriy Bryndin


# generated by wxGlade 0.9.3 on Fri Jul 19 16:04:38 2019

import wx.grid
from diffpy.pdfgui.gui.pdfpanel import PDFPanel
from diffpy.pdfgui.gui.wxextensions import wx12
from diffpy.pdfgui.gui.wxextensions.autowidthlabelsgrid import \
        AutoWidthLabelsGrid
from diffpy.utils.wx import gridutils


class ParametersPanel(wx.Panel, PDFPanel):
    '''GUI Panel, parameters viewer/editor

    Data members:
        parameters      -- parameters dictionary
        _focusedText    -- value of a cell before it changes
    '''
    def __init__(self, *args, **kwds):
        PDFPanel.__init__(self)
        # begin wxGlade: ParametersPanel.__init__
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.grid_parameters = AutoWidthLabelsGrid(self, wx.ID_ANY, size=(1, 1))
        self.button_applyparameters = wx.Button(self, wx.ID_ANY, "Apply parameters")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.grid.EVT_GRID_CMD_CELL_CHANGED, self.onCellChange, self.grid_parameters)
        self.Bind(wx.grid.EVT_GRID_CMD_CELL_LEFT_CLICK, self.onCellLeftClick, self.grid_parameters)
        self.Bind(wx.grid.EVT_GRID_CMD_CELL_RIGHT_CLICK, self.onCellRightClick, self.grid_parameters)
        self.Bind(wx.grid.EVT_GRID_CMD_EDITOR_SHOWN, self.onEditorShown, self.grid_parameters)
        self.Bind(wx.grid.EVT_GRID_CMD_RANGE_SELECT, self.onGridRangeSelect, self.grid_parameters)
        self.Bind(wx.EVT_BUTTON, self.onApplyParameters, self.button_applyparameters)
        # end wxGlade
        self.__customProperties()
        return


    def __set_properties(self):
        # begin wxGlade: ParametersPanel.__set_properties
        self.grid_parameters.CreateGrid(0, 3)
        self.grid_parameters.EnableDragRowSize(0)
        self.grid_parameters.SetColLabelValue(0, "Initial")
        self.grid_parameters.SetColLabelValue(1, "Fixed")
        self.grid_parameters.SetColLabelValue(2, "Refined")
        # end wxGlade

        # set the second column to display boolean values
        attr = wx.grid.GridCellAttr()
        attr.SetEditor(wx.grid.GridCellBoolEditor())
        attr.SetRenderer(wx.grid.GridCellBoolRenderer())
        self.grid_parameters.SetColAttr(1, attr)


    def __do_layout(self):
        # begin wxGlade: ParametersPanel.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.grid_parameters, 1, wx.EXPAND, 0)
        sizer_buttons.Add((20, 20), 1, 0, 0)
        sizer_buttons.Add(self.button_applyparameters, 0, wx.ALL, 5)
        sizer_1.Add(sizer_buttons, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

    ##########################################################################
    # Misc Methods

    def __customProperties(self):
        """Custom properties for the panel."""
        self._focusedText = None
        self._selectedCells = []
        self.parameters = {}
        self.fit = None
        return

    def refresh(self):
        ''' Refreshes wigets on the panel'''
#        # Update the parameters dictionary
#        self.fitting.updateParameters()

        nRows = len(self.parameters)

        ### update the grid
        #remove all rows and create new ones
        self.grid_parameters.BeginBatch()
        gridrows = self.grid_parameters.GetNumberRows()
        if gridrows != 0:
            self.grid_parameters.DeleteRows( numRows = gridrows )
        self.grid_parameters.InsertRows( numRows = nRows )
        #self.grid_parameters.SetColFormatBool(1)

        i = 0
        keys = sorted(self.parameters.keys())
        for key in keys:
            # parameter index
            self.grid_parameters.SetRowLabelValue(i, str(self.parameters[key].idx))
            # initial value
            self.grid_parameters.SetCellValue(i,0, str(self.parameters[key].initialStr()) )
            # flag "fixed"
            #NOTE: for bool type of cells use '0' or '1' as False and True
            self.grid_parameters.SetCellValue(i,1, str(int(self.parameters[key].fixed))   )
            # refined value
            self.grid_parameters.SetReadOnly(i,2)
            if self.parameters[key].refined is None:
                self.grid_parameters.SetCellValue(i,2, "" )
            else:
                self.grid_parameters.SetCellValue(i,2, str(self.parameters[key].refined)  )
            i += 1

        self.grid_parameters.AutosizeLabels()
        self.grid_parameters.AutoSizeColumns()
        self.grid_parameters.EndBatch()


    def onCellLeftClick(self, event): # wxGlade: ParametersPanel.<event_handler>
        """Toggle a fix/free cell when clicked."""
        r = event.GetRow()
        c = event.GetCol()
        # Only proceed if there is no selection and
        # this click has no keyboard modifiers.
        ignorethis = (c != 1 or self.grid_parameters.IsSelection() or
                      event.ShiftDown() or event.ControlDown())
        if ignorethis:
            # do standard click event handling
            event.Skip()
            return
        # We consume the event here.  This prevents focusing the clicked
        # cell after a click, but that is not necessary for a checkbox.
        state = int(self.grid_parameters.GetCellValue(r, c) or 0)
        self.applyCellChange(r, c, not state)
        return


    def onGridRangeSelect(self, event): # wxGlade: ParametersPanel.<event_handler>
        """Handle range selections.

        This is needed to properly handle simple left-clicking of fix/free
        cells. It serves no other purpose.
        """
        event.Skip()
        return

    def onCellRightClick(self, event): # wxGlade: ParametersPanel.<event_handler>
        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        r = event.GetRow()
        c = event.GetCol()
        # If the right-clicked node is not part of a group, then make sure that
        # it is the only selected cell.
        append = False
        if self.grid_parameters.IsInSelection(r,c):
            append = True
        self.grid_parameters.SelectBlock(r,c,r,c,append)
        self.popupMenu(self.grid_parameters, event.GetPosition().x,
                event.GetPosition().y)
        event.Skip()
        return

    def onEditorShown(self, event): # wxGlade: ParametersPanel.<event_handler>
        i = event.GetRow()
        j = event.GetCol()
        self._focusedText = self.grid_parameters.GetCellValue(i,j)
        self._selectedCells = gridutils.getSelectedCells(self.grid_parameters)
        event.Skip()
        return

    def onCellChange(self, event): # wxGlade: ParametersPanel.<event_handler>
        # NOTE: be careful with refresh() => recursion! operations on grid will
        # call onCellChange
        # Note that this method does not get called when a fix/free cell is
        # selected.
        i = event.GetRow()
        j = event.GetCol()

        if self._focusedText is None: return
        self._focusedText = None

        value = self.grid_parameters.GetCellValue(i,j)
        # Verify the value. This is done here since if it is allowed to be done
        # in fillCells, then an error dialog will be thrown for each point
        # in the loop.
        try:
            # Check that the value is valid
            if j == 0:
                converted = value
                try:
                    converted = int(value)
                except ValueError:
                    pass
                key = int(self.grid_parameters.GetRowLabelValue(i))
                temp = self.parameters[key].initialValue()
                if temp != converted:
                    self.parameters[key].setInitial(converted)
                    self.mainFrame.needsSave()

            # If we made it this far, then we can continue.
            self.fillCells(self._selectedCells, value)
            self.grid_parameters.AutoSizeColumns(0)
        finally:
            #self.refresh()
            event.Skip()

        return

    def applyCellChange(self, row, col, value):
        """Update parameters dictionary according to a change in a cell.

        This also updates the cell, if possible, but not the grid. Changes to
        the cell that may affect the grid, such as inserting text that is wider
        than the column width, must be handled elsewhere.

        row     --  row
        col     --  column
        value   --  new value

        """
        key = int(self.grid_parameters.GetRowLabelValue(row))
        if col == 0:  # initial value
            temp = self.parameters[key].initialValue()
            if temp != value:
                self.parameters[key].setInitial(value)
                self.grid_parameters.SetCellValue(row,0,str(float(value)))
                self.mainFrame.needsSave()

        elif col == 1:  # flag "fixed"
            temp = bool(self.parameters[key].fixed)
            value = bool(int(value))
            if temp is not value:
                self.parameters[key].fixed = value
                self.grid_parameters.SetCellValue(row,1,str(int(value)))
                self.mainFrame.needsSave()

        return


    def popupMenu(self, window, x, y):
        """Opens a popup menu

        window  --  window, where to popup a menu
        x       --  x coordinate
        y       --  y coordinate
        """
        # only do this part the first time so the events are only bound once
        if not hasattr(self, "did_popupIDs"):
            self.did_popupIDs = True
            self.popupID1 = wx12.NewIdRef()
            self.popupID2 = wx12.NewIdRef()
            self.popupID3 = wx12.NewIdRef()

            self.Bind(wx.EVT_MENU, self.onPopupFixFree,  id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.onPopupCopyRefinedToInitial,  id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.onPopupRenameParameters,  id=self.popupID3)

        # make a menu
        menu = wx.Menu()

        # add some other items
        menu.Append(self.popupID1, "Fix / Free")
        menu.Append(self.popupID2, "Copy Refined To Initial")
        menu.Append(self.popupID3, "Rename Parameters")

        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        window.PopupMenu(menu, wx.Point(x,y))
        menu.Destroy()
        return

    ##### Popup menu events  ##################################################
    def onPopupFill(self, event):
        '''Fills cells selected in the grid with a new value'''

        # NOTE: GetSelectedCells returns only SINGLE selected cells, not blocks or row/columns !
        if self.grid_parameters.IsSelection():
            dlg = wx.TextEntryDialog(self, 'New value:','Fill Selected Cells', '')

            if dlg.ShowModal() == wx.ID_OK:
                value = dlg.GetValue()

                rows = self.grid_parameters.GetNumberRows()
                cols = self.grid_parameters.GetNumberCols()

                for i in range(rows):
                    for j in range(cols):
                        inSelection  = self.grid_parameters.IsInSelection(i,j)
                        valueChanged = (value != self.grid_parameters.GetCellValue(i,j))
                        if inSelection and valueChanged:
                            self.applyCellChange(i, j, value)

                #self.refresh()

            dlg.Destroy()
        event.Skip()

    def onPopupFixFree(self, event):
        '''Fixes parameters with selected cells'''
        # NOTE: GetSelectedCells returns only SINGLE selected cells, not blocks
        # or row/columns !
        seldict = {}
        if self.grid_parameters.IsSelection():

            indices = self.getSelectedParameters()
            for row in indices:
                state = self.grid_parameters.GetCellValue(row,1)
                state = bool(int(state.strip() or "0"))
                seldict[row] = state

            # Find the majority state
            nfixed = sum(1 for st in seldict.values() if st)
            nfree = len(seldict) - nfixed
            newstate = True # fixed
            if nfree < nfixed:
                # free all parameters
                newstate = False

            for row in seldict:
                self.applyCellChange(row, 1, newstate)
        event.Skip()
        return

    def onPopupCopyRefinedToInitial(self, event):
        """Copy refined parameter to initial value.
        """
        if not self.grid_parameters.IsSelection():
            event.Skip()
            return
        for row in self.getSelectedParameters():
            refined = self.grid_parameters.GetCellValue(row, 2)
            if refined == "": continue
            self.applyCellChange(row, 0, refined)
        # Resize the first column
        self.grid_parameters.AutoSizeColumn(0)
        event.Skip()
        return

    def onPopupRenameParameters(self, event):
        """Rename parameters."""

        if self.grid_parameters.IsSelection():
            dlg = wx.TextEntryDialog(self, 'New index:',
                    'Rename Selected Parameters', '')

            value = None
            if dlg.ShowModal() == wx.ID_OK:
                value = dlg.GetValue()
            dlg.Destroy()
            try:
                value = int(value)
            except (ValueError, TypeError):
                return

            rows = self.grid_parameters.GetNumberRows()
            cols = self.grid_parameters.GetNumberCols()

            selpars = []
            # Get the selected parameters
            for i in range(rows):
                key = int(self.grid_parameters.GetRowLabelValue(i))
                for j in range(cols):
                    if self.grid_parameters.IsInSelection(i,j):
                        selpars.append(key)
                        break


            for key in selpars:
                if key != value:
                    self.fit.changeParameterIndex(key, value)
                    self.mainFrame.needsSave()

            self.fit.updateParameters()
            self.refresh()

        event.Skip()
        return


    ##### end of Popup menu events  ###########################################

    def onApplyParameters(self, event): # wxGlade: ParametersPanel.<event_handler>
        print("parameters applied")
        self.fit.applyParameters()
        self.mainFrame.needsSave()
        event.Skip()

    # Required by event handlers

    def getSelectedParameters(self):
        """Get list of row values of selected cells."""
        rows = self.grid_parameters.GetNumberRows()
        cols = self.grid_parameters.GetNumberCols()
        selection = []

        for i in range(rows):
            for j in range(cols):
                if self.grid_parameters.IsInSelection(i,j):
                    selection.append(i)
                    break

        return selection

    def fillCells(self, indices, value):
        """Fill cells with a given value.

        indices    --  list of (i,j) tuples representing cell coordinates
        value       --  string value to place into cells
        """
        for i, j in indices:
            if j != 1 and not self.grid_parameters.IsReadOnly(i, j):
                self.applyCellChange(i, j, value)
        return

# end of class ParametersPanel

##### testing code ############################################################
if __name__ == "__main__":
    class MyFrame(wx.Frame):
        def __init__(self, *args, **kwds):
            kwds["style"] = wx.DEFAULT_FRAME_STYLE
            wx.Frame.__init__(self, *args, **kwds)
            self.window = ParametersPanel(self, -1)
            self.SetTitle("testing")
            # choke, mainframe.needsSave() emulation
            self.window.mainFrame = self.window
            self.window.mainFrame.needsSave = self.dummy

            self.test()

        def dummy(self):
            pass

        def test(self):
            '''Testing code goes here'''
            from diffpy.pdfgui.control.parameter import Parameter

            self.window.parameters = {3:Parameter(3), 17:Parameter(17), 11:Parameter(11)}
            self.window.parameters[3].setInitial(1)
            self.window.parameters[17].setInitial(0.55)
            self.window.parameters[11].setInitial(5.532)

            self.window.refresh()


    class MyApp(wx.App):
        def onInit(self):
            frame_1 = MyFrame(None, -1, "")
            self.SetTopWindow(frame_1)
            frame_1.Show()
            return 1

    app = MyApp(0)
    app.MainLoop()
##### end of testing code #####################################################
