#Boa:Frame:TopFrame

import gui.Action
import gui.ProjectDialog
import AbstractFrame
import wx
import wx.stc


[ID_NEW_PROJECT, ID_PROJECT_DLG, 
 ID_OPEN_PROJECT, ID_CLOSE_PROJECT, ID_EXIT
] = [wx.NewId() for _init_ctrls in range(5)]
[ID_CMD_CREATE, ID_CMD_RECREATE, ID_CMD_UPDATE, ID_CMD_PREPARE
] = [wx.NewId() for _init_ctrls in range(4)]
[ID_HELP_ABOUT, ID_HELP_CONTENT
] = [wx.NewId() for _init_ctrls in range(2)]

class TopFrame(AbstractFrame.AbstractFrame):


    def __createMenuBar(self):

        projectMenu = wx.Menu();
        projectMenu.Append(ID_NEW_PROJECT, "&New Project", "Create a new project")
        projectMenu.Append(ID_OPEN_PROJECT, "&Open Project", "Open an existing project")
        projectMenu.Append(ID_CLOSE_PROJECT, "&Close Project", "Close project that is currently opened")
        projectMenu.AppendSeparator()
        projectMenu.Append(ID_EXIT, "E&xit", "Exit the application");

        commandMenu = wx.Menu()
        commandMenu.Append(ID_CMD_CREATE, "&Create", "Create a new database")
        commandMenu.Append(ID_CMD_RECREATE, "&Recreate", "Drop and recreate an existing database")
        commandMenu.Append(ID_CMD_UPDATE, "&Update", "Update a database to a new version")
        commandMenu.Append(ID_CMD_PREPARE, "&Prepare", "Create a new alter tree")

        helpMenu = wx.Menu()
        helpMenu.Append(ID_HELP_ABOUT, "&About")
        helpMenu.Append(ID_HELP_CONTENT, "&Content")
        
        menuBar = wx.MenuBar()
        menuBar.Append(projectMenu, "&Project")
        menuBar.Append(commandMenu, "&Command")
        menuBar.Append(helpMenu, "&Help")
        
        self.SetMenuBar(menuBar)

        wx.EVT_MENU(self, ID_NEW_PROJECT, self.onNewProject)
        wx.EVT_MENU(self, ID_EXIT, self.onExit)
        wx.EVT_MENU(self, ID_HELP_ABOUT, self.onAbout)
        
    def __createStatusBar(self):
        self.__statusBar = self.CreateStatusBar();
        self.__statusBar.SetStatusText("To generate a new project, click on New Project in the Project menu, select a project directory and click on execute")


    def __init__(self, parent, title):

        AbstractFrame.AbstractFrame.__init__(self, parent, title)

        self.__createMenuBar()
        self.__createStatusBar()

    def onNewProject(self,event):
        dia = gui.ProjectDialog.ProjectDialog(self, ID_PROJECT_DLG, 'New Project', gui.ProjectDialog.DIALOG_TYPE_NEW)
        dia.ShowModal()
        dia.Destroy()


    def onExit(self, event):
        self.Close(True);
        
    def onAbout(self, event):
        dlg = wx.MessageDialog(self, 'Noora GUI v0.0.6', '(c) 2010', wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


