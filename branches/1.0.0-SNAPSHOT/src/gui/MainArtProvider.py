import wx
import os
import sys
import Settings as Settings


NOORA_DIR    = os.path.abspath(os.path.dirname(sys.argv[0]))

class MainArtProvider(wx.ArtProvider):

  def __init__(self):        
    wx.ArtProvider.__init__(self)
    self.setNooraDir(NOORA_DIR)
 
  def CreateBitmap(self, artid, client, size):
    bmp = wx.NullBitmap
    if artid == wx.ART_FILE_OPEN:
      bmp=wx.Image(self.getResourceDir()+os.sep+'importdir_wiz.gif', wx.BITMAP_TYPE_GIF).ConvertToBitmap()
    if artid == wx.ART_NEW:
      bmp=wx.Image(self.getResourceDir()+os.sep+'new_project.gif', wx.BITMAP_TYPE_GIF).ConvertToBitmap()
    if artid == wx.ART_GO_FORWARD:
      bmp=wx.Image(self.getResourceDir()+os.sep+'run.gif', wx.BITMAP_TYPE_GIF).ConvertToBitmap()
    if artid == wx.ART_UNDO:
      bmp=wx.Image(self.getResourceDir()+os.sep+'clear_console.gif', wx.BITMAP_TYPE_GIF).ConvertToBitmap()
    if artid == Settings.ART_CONSOLE:
      bmp=wx.Image(self.getResourceDir()+os.sep+'console_view.gif', wx.BITMAP_TYPE_GIF).ConvertToBitmap()
    if artid == Settings.ART_ACTION:
      bmp=wx.Image(self.getResourceDir()+os.sep+'throbber.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    return bmp
  
  def setNooraDir(self, path):
    self.__nooraDir=path
    
  def getNooraDir(self):
    return self.__nooraDir

  def getResourceDir(self):
    return self.getNooraDir()+os.sep+'resources'
        