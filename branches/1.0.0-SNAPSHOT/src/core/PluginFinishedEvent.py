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

  def __init__(self, id, directory, filename):
    event_type = Settings.EVT_PLUGIN_FINISHED
    #wx.PyEvent.__init__(self, id=id, eventType=self.__eventType)
    wx.PyEvent.__init__(self, id, event_type)
    self.__directory = directory
    self.__filename = filename 