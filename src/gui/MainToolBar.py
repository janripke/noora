import wx
import Settings as Settings

class MainToolBar(wx.ToolBar):

    def __init__(self,parent,id,*args, **kwargs):        
        wx.ToolBar.__init__(self,parent,id,*args, **kwargs)
        self.AddLabelTool(Settings.ID_NEW_PROJECT, '', wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (16, 16)))
        self.AddLabelTool(Settings.ID_OPEN_PROJECT, '', wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (16, 16)))
        
        self.AddSeparator()
        

        self.AddLabelTool(Settings.ID_EXECUTE,'Execute', wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_TOOLBAR, (16, 16)))
        self.AddLabelTool(Settings.ID_CLEAR,'', wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, (16, 16)))
        