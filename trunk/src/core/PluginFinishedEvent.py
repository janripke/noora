import wx
import gui.Settings as Settings

class PluginFinishedEvent(wx.PyEvent):
  """
    Open project event.
  """
  
  def getDirectory(self):
    return self.__directory
  
  def getFilename(self):
    return self.__filename

  def __init__(self, directory, filename):
    self.__eventType = Settings.EVT_PLUGIN_FINISHED
    wx.PyEvent.__init__(self, eventType=self.__eventType)
    self.__directory = directory
    self.__filename = filename 