#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##############################################################################
#
# PDFgui            by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2006 trustees of the Michigan State University.
#                   All rights reserved.
#
# File coded by:    Beric Bearnson
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################
import wx
import wx.grid
from diffpy.pdfgui.gui.phasepanelutils import float2str
from diffpy.pdfgui.gui.wxextensions.autowidthlabelsgrid import \
        AutoWidthLabelsGrid
import numpy as np


class AdvancedFrame(wx.Frame):
    def __init__(self, title, mags, struc, *args, **kwds):
        self.structure = struc
        self.magnetic_atoms = mags
        # begin wxGlade: MyFrame.__init__
        #kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, parent=None, title="Advanced Configuration Settings", size=(800,600))
        self.SetSize((800, 630))
        self.SetTitle("Advnaced Configuration Settings")

        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        self.panel_1.SetMinSize((800, 600))

        sizer_1 = wx.StaticBoxSizer(wx.StaticBox(self.panel_1, wx.ID_ANY, ""), wx.VERTICAL)

        sizer_2 = wx.StaticBoxSizer(wx.StaticBox(self.panel_1, wx.ID_ANY, ""), wx.HORIZONTAL)
        sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)

        self.gridAtoms = AutoWidthLabelsGrid(self.panel_1, wx.ID_ANY, size=(1, 1))
        self.gridAtoms.CreateGrid(0, 7)
        self.gridAtoms.EnableDragRowSize(0)
        self.gridAtoms.SetRowLabelSize(23)
        self.gridAtoms.SetColLabelValue(0, "elem(x,y,z)")
        self.gridAtoms.SetColSize(0, 225)
        self.gridAtoms.SetColLabelValue(1, "gs")
        self.gridAtoms.SetColSize(1, 29)
        self.gridAtoms.SetColLabelValue(2, "gi")
        self.gridAtoms.SetColSize(2, 31)
        self.gridAtoms.SetColLabelValue(3, "Q grid(min,max,step)")
        self.gridAtoms.SetColSize(3, 152)
        self.gridAtoms.SetColLabelValue(4, "custom FF")
        self.gridAtoms.SetColLabelValue(5, "colFiveName")
        self.gridAtoms.SetColSize(5, 93)
        self.gridAtoms.SetColLabelValue(6, "damping pwr")
        self.gridAtoms.SetColSize(6, 97)
        self.gridAtoms.SetMinSize((796, 460))
        sizer_2.Add(self.gridAtoms, 1, wx.EXPAND, 0)

        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_3, 1, wx.ALIGN_RIGHT | wx.ALL, 33)

        self.btn1 = wx.Button(self.panel_1, wx.ID_ANY, "Cancel")
        sizer_3.Add(self.btn1, 0, wx.RIGHT, 10)

        self.btn2 = wx.Button(self.panel_1, wx.ID_ANY, "Ok")
        sizer_3.Add(self.btn2, 0, 0, 0)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.destroy, self.btn1)
        self.Bind(wx.EVT_BUTTON, self.destroy, self.btn2)
        # end wxGlade
        self.refresh()
        self.Show()

    def destroy(self, event):
        self.Close()

    def arrayToStr(self, arr):
        """returns basis and kvec numpy arrays in str format
        Ex. [[1 2 3],[4 5 6]] -> (1, 2, 3),(4, 5, 6)"""
        if arr is None or type(arr) != np.ndarray:
            return
        ret = str(arr.astype(float).tolist())[1:-1]
        ret = ret.replace("[","(")
        ret = ret.replace("]",")")
        return ret

    def refresh(self):
        """Refresh wigets on the panel."""
        if self.structure is None:
            raise ValueError("structure is not defined.")

        ### update the grid ###
        nmagatoms = 0
        for m in self.structure.magnetic_atoms:
            if m[0] == 1:
                nmagatoms += 1
        nrows = self.gridAtoms.GetNumberRows()
        self.gridAtoms.BeginBatch()
        # make sure grid has correct number of rows
        if nmagatoms > nrows:
            self.gridAtoms.InsertRows(numRows = nmagatoms - nrows)
        elif nmagatoms < nrows:
            self.gridAtoms.DeleteRows(numRows = nrows - nmagatoms)

        # start with clean grid
        self.gridAtoms.ClearGrid()

        # fill the first 'elem' column with element symbols and x, y, z values if magnetic
        count = 0
        for row, atom in zip(range(len(self.structure)), self.structure):
            if self.structure.magnetic_atoms[row][0] == 1:
                self.gridAtoms.SetRowLabelValue(count, str(row+1))
                atom_info = atom.element + " (" + float2str(atom.xyz[0]) + "," + float2str(atom.xyz[1]) + "," + float2str(atom.xyz[2]) + ")"
                self.gridAtoms.SetCellValue(count, 0, atom_info)

                magSpecies = self.structure.magStructure.species[self.structure.magnetic_atoms[row][1]]
                gS = '0.0' if magSpecies.gL is None else str(magSpecies.gS)
                self.gridAtoms.SetCellValue(count, 1, gS)
                gL = '0.0' if magSpecies.gS is None else str(magSpecies.gL)
                self.gridAtoms.SetCellValue(count, 2, gL)
                ffkey = 'None' if magSpecies.ffparamkey is None else magSpecies.ffparamkey
                self.gridAtoms.SetCellValue(count, 3, ffkey)
                count += 1


        self.gridAtoms.AutosizeLabels()
        self.gridAtoms.AutoSizeColumns()

        return
