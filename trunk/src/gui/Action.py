
import gui.LabelText
import wx;

__revision__ = "$Revision$"

[wxID_ACTIONGROUP,
 wxID_COMMANDLABEL,
 wxID_COMMANDCHOICE,
 wxID_DATABASELABEL,
 wxID_DATABASETEXT,
] = [wx.NewId() for _init_ctrls in range(5)]

class Action:

    def _init_controls(self, parent):
        
        # not all wx implementations (e.g. wxGTK) will support children _inside_ the static box so
        # we make them siblings of the static box instead.

        self.actionGroup = wx.StaticBox(id=wxID_ACTIONGROUP, label='Action', 
                                        name='action_group', parent=parent, 
                                        pos=wx.Point(8, 128), size=wx.Size(320, 352),
                                        style=0)
        
        self.commandLabel = wx.StaticText(id=wxID_COMMANDLABEL, label='command',
              name='command', parent=parent, pos=wx.Point(20, 156),
              size=wx.Size(48, 13), style=0)
                
        self.commandChoice = wx.Choice(choices=['drop','clean','build','create','generate', 'recreate', 'update'],
                                 id=wxID_COMMANDCHOICE, name='command_choice', parent=parent,
                                 pos=wx.Point(88, 152), size=wx.Size(130, 21),
                                 style=0)
                
        self.database = gui.LabelText.LabelText(parent=parent,pos=wx.Point(20,176),
                                                labelWidth=64, textWidth=100, name='database', value='')
        self.environment = gui.LabelText.LabelText(parent=parent,pos=wx.Point(20,200),
                                                   labelWidth=64, textWidth=100, name='environment', value='')


    def __init__(self, parent):
        self._init_controls(parent)
