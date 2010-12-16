import wx
import Settings as Settings

class MainMenuBar(wx.MenuBar):

    def __init__(self):        
        wx.MenuBar.__init__(self)
        menu = wx.Menu()
        menu.Append(Settings.ID_NEW_PROJECT, "&New Project", "Create a new project")
        menu.Append(Settings.ID_OPEN_PROJECT, "&Open Project", "Open an existing project")
        menu.Append(Settings.ID_CLOSE_PROJECT, "&Close Project", "Close project that is currently opened")
        menu.AppendSeparator()
        menu.Append(wx.ID_EXIT, "E&xit", "Exit the application");
        self.Append(menu, "&File")
        
        
        menu = wx.Menu()
        menu.Append(wx.ID_ABOUT, "&About\tAlt-A","About")
        self.Append(menu, "&Help")
        