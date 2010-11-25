#Boa:Frame:TopFrame

import gui.Action
import gui.Project
import wx
import wx.lib.filebrowsebutton
import wx.stc


[wxID_TOPFRAME, wxID_TOPFRAMEACTIONGROUP, wxID_TOPFRAMECHOICE1, 
 wxID_TOPFRAMECOMMAND, wxID_TOPFRAMEOUTPUTPANEL, wxID_TOPFRAMEPROJECTDIR, 
 wxID_TOPFRAMEPROJECTGROUP, wxID_TOPFRAMEPROJECTHOMELABEL, 
 wxID_TOPFRAMESTYLEDTEXTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(9)]

class TopFrame(wx.Frame):
    def _init_ctrls(self, prnt):

        wx.Frame.__init__(self, id=wxID_TOPFRAME, name='wxTopFrame', parent=prnt,
              pos=wx.DefaultPosition, size=wx.Size(884, 542),
              style=wx.DEFAULT_FRAME_STYLE, title='TopFrame')
        self.SetClientSize(wx.Size(868, 504))

        self.projectGroup = gui.Project.Project(self)
        self.actionGroup = gui.Action.Action(self)

        self.OutputPanel = wx.StaticBox(id=wxID_TOPFRAMEOUTPUTPANEL,
              label='Output', name='OutputPanel', parent=self, pos=wx.Point(344,
              8), size=wx.Size(416, 480), style=0)

        self.styledTextCtrl1 = wx.stc.StyledTextCtrl(id=wxID_TOPFRAMESTYLEDTEXTCTRL1,
              name='styledTextCtrl1', parent=self, pos=wx.Point(368, 32),
              size=wx.Size(296, 440), style=0)





    def __init__(self, parent):
        self._init_ctrls(parent)
