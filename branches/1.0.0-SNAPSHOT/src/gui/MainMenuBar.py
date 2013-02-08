import wx
import Settings as Settings

class MainMenuBar(wx.MenuBar):

    def __init__(self):        
        wx.MenuBar.__init__(self)
        menu = wx.Menu()
        menu.Append(Settings.ID_NEW_PROJECT, "&New Project\tAlt-N", "Create a new project")
        menu.Append(Settings.ID_OPEN_PROJECT, "&Open Project\tAlt-O", "Open an existing project")      
        menu.AppendSeparator()
        menu.Append(wx.ID_EXIT, "E&xit", "Exit the application");
        self.Append(menu, "&File")

        menu = wx.Menu()
        menu.Append(Settings.ID_EDIT_PROJECT, "&project.conf...\tAlt-p","View the project configuration file")
        self.Append(menu, "&View")  
        
        menu = wx.Menu()
        showViewMenu = wx.Menu()
        showViewMenu.Append(Settings.ID_SHOW_ACTION_VIEW, "&Action\tAlt-a","Show the action view")
        showViewMenu.Append(Settings.ID_SHOW_CONSOLE_VIEW, "&Console\tAlt-c","Show the console view")
        menu.AppendSubMenu(showViewMenu, "Show View")
        self.Append(menu, "&Window")        
        
        
        
        menu = wx.Menu()
        menu.Append(wx.ID_ABOUT, "&About\tAlt-A","About")
        self.Append(menu, "&Help")
        