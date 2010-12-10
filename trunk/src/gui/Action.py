import core.CommandDispatcher
import gui.LabelText
import gui.Project
import wx;

__revision__ = "$Revision$"

[wxID_ACTIONGROUP,
 wxID_COMMANDLABEL,
 wxID_COMMANDCHOICE,
 wxID_DATABASELABEL,
 wxID_DATABASETEXT,
 wxID_EXECUTE
] = [wx.NewId() for _init_ctrls in range(6)]

class Action:

    def _init_controls(self, parent):
        
        self.__parent = parent

        # not all wx implementations (e.g. wxGTK) will support children _inside_ the static box so
        # we make them siblings of the static box instead.

        self.actionGroup = wx.StaticBox(id=wxID_ACTIONGROUP, label='Action',
                                        name='action_group', parent=parent,
                                        pos=wx.Point(8, 128), size=wx.Size(320, 352),
                                        style=0)

        self.commandLabel = wx.StaticText(id=wxID_COMMANDLABEL, label='command',
              name='command', parent=parent, pos=wx.Point(20, 156),
              size=wx.Size(48, 13), style=0)

        self.commandChoice = wx.Choice(choices=['drop', 'clean', 'build', 'create', 'generate', 'recreate', 'update'],
                                 id=wxID_COMMANDCHOICE, name='command_choice', parent=parent,
                                 pos=wx.Point(88, 152), size=wx.Size(130, 25),
                                 style=0)

        self.database = gui.LabelText.LabelText(parent=parent, pos=wx.Point(20, 176),
                                                labelWidth=64, textWidth=100, label='database', value='')
        self.environment = gui.LabelText.LabelText(parent=parent, pos=wx.Point(20, 200),
                                                   labelWidth=64, textWidth=100, label='environment', value='')
        self.schema = gui.LabelText.LabelText(parent=parent, pos=wx.Point(20, 224),
                                              labelWidth=64, textWidth=100, label='schema', value='')

        self.execute = wx.Button(id=wxID_EXECUTE, label='execute',
              name='execute', parent=parent, pos=wx.Point(232, 440),
              size=wx.Size(75, 23), style=0)
        self.execute.Bind(wx.EVT_BUTTON, self.onExecute,
              id=wxID_EXECUTE)


    def onExecute(self, event):
        projectDir = self.__parent.projectGroup.projectDir.GetValue();
        command = self.commandChoice.GetStringSelection()
        self.__dispatcher = core.CommandDispatcher.CommandDispatcher(projectDir, command)

        arguments = []
        if command == 'generate':
            # get values for generate
            arguments.append(command);
            arguments.append('-si=' + self.database.text.GetValue())
            arguments.append('-sc=' + self.schema.text.GetValue())

        self.__dispatcher.setParameters(arguments)
        self.__dispatcher.execute()

    def __init__(self, parent):
        self._init_controls(parent)
