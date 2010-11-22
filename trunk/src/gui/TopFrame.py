#Boa:Frame:TopFrame

import wx
import wx.lib.filebrowsebutton
import wx.stc

def create(parent):
    return TopFrame(parent)

[wxID_TOPFRAME, wxID_TOPFRAMEACTIONGROUP, wxID_TOPFRAMECHOICE1, 
 wxID_TOPFRAMECOMMAND, wxID_TOPFRAMEDIRBROWSEBUTTON1, 
 wxID_TOPFRAMEOUTPUTPANEL, wxID_TOPFRAMEPROJECTGROUP, 
 wxID_TOPFRAMEPROJECTHOMELABEL, wxID_TOPFRAMESTYLEDTEXTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(9)]

class TopFrame(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_TOPFRAME, name='', parent=prnt,
              pos=wx.Point(380, 227), size=wx.Size(884, 542),
              style=wx.DEFAULT_FRAME_STYLE, title='TopFrame')
        self.SetClientSize(wx.Size(868, 504))

        self.OutputPanel = wx.StaticBox(id=wxID_TOPFRAMEOUTPUTPANEL,
              label='Output', name='OutputPanel', parent=self, pos=wx.Point(344,
              8), size=wx.Size(416, 480), style=0)

        self.styledTextCtrl1 = wx.stc.StyledTextCtrl(id=wxID_TOPFRAMESTYLEDTEXTCTRL1,
              name='styledTextCtrl1', parent=self, pos=wx.Point(368, 32),
              size=wx.Size(296, 440), style=0)

        self.ProjectGroup = wx.StaticBox(id=wxID_TOPFRAMEPROJECTGROUP,
              label='Project', name='ProjectGroup', parent=self, pos=wx.Point(8,
              16), size=wx.Size(320, 104), style=0)

        self.ActionGroup = wx.StaticBox(id=wxID_TOPFRAMEACTIONGROUP,
              label='Action', name='ActionGroup', parent=self, pos=wx.Point(8,
              128), size=wx.Size(320, 352), style=0)

        self.ProjectHomeLabel = wx.StaticText(id=wxID_TOPFRAMEPROJECTHOMELABEL,
              label='Project home', name='ProjectHomeLabel', parent=self,
              pos=wx.Point(16, 32), size=wx.Size(64, 13), style=0)

        self.dirBrowseButton1 = wx.lib.filebrowsebutton.DirBrowseButton(buttonText='Browse',
              dialogTitle='Choose directory', id=wxID_TOPFRAMEDIRBROWSEBUTTON1,
              labelText='Select a directory:', newDirectory=False, parent=self,
              pos=wx.Point(24, 56), size=wx.Size(296, 48), startDirectory='.',
              style=wx.TAB_TRAVERSAL,
              toolTip='Type directory name or browse to select')

        self.choice1 = wx.Choice(choices=['generate', 'recreate', 'update'], id=wxID_TOPFRAMECHOICE1,
              name='choice1', parent=self, pos=wx.Point(80, 152),
              size=wx.Size(130, 21), style=0)

        self.Command = wx.StaticText(id=wxID_TOPFRAMECOMMAND, label='Command',
              name='Command', parent=self, pos=wx.Point(24, 152),
              size=wx.Size(48, 13), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)
