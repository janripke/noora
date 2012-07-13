import wx
import Settings as Settings
import MainArtProvider as MainArtProvider

class MainToolBar(wx.ToolBar):

  def __init__(self,parent,id,*args, **kwargs):        
    wx.ToolBar.__init__(self,parent,id,*args, **kwargs)
    mainArtProvider=MainArtProvider.MainArtProvider()
    wx.ArtProvider.Push(mainArtProvider)
    self.AddLabelTool(Settings.ID_NEW_PROJECT, '', MainArtProvider.MainArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (16, 16)),wx.NullBitmap,0,'Create a new project','Create a new project')
    self.AddLabelTool(Settings.ID_OPEN_PROJECT, '', MainArtProvider.MainArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (16, 16)),wx.NullBitmap,0,'Open an existing project','Open an existing project')
    
    self.AddSeparator()
    

    self.AddLabelTool(Settings.ID_EXECUTE,'Execute', wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_TOOLBAR, (16, 16)),wx.NullBitmap,0,'Execute command','Execute command')
    self.AddLabelTool(Settings.ID_CLEAR,'', wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_TOOLBAR, (16, 16)),wx.NullBitmap,0,'Clear console output','Clear console output')