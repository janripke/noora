import wx
import AbstractPanel        as AbstractPanel
import gui.panels.ComboBoxPanel as ComboBoxPanel
import gui.panels.TextPanel     as TextPanel
import gui.Settings             as Settings

class ActionPanel(AbstractPanel.AbstractPanel):

  def getDesciptionControl(self):
    return self.__descriptionControl

  def getCommandControl(self):
    return self.__commandControl
  
  def getDatabaseControl(self):
    return self.__databaseControl

  def getSchemeControl(self):
    return self.__schemeControl

  def getEnvironmentControl(self):
    return self.__environmentControl
  
  def getVersionControl(self):
    return self.__versionControl

  def __init__(self, parent, id):
    AbstractPanel.AbstractPanel.__init__(self, parent, id)
    
    sizer=wx.BoxSizer(wx.VERTICAL)
    self.__descriptionControl=wx.StaticText(self, -1, "")        
    self.__commandControl=ComboBoxPanel.ComboBoxPanel(self,Settings.ID_COMMAND,"Command",[])
    self.__commandControl.Enable(False)
    self.__databaseControl = ComboBoxPanel.ComboBoxPanel(self,-1,"Database",[])
    self.__databaseControl.Enable(False)
    self.__schemeControl = ComboBoxPanel.ComboBoxPanel(self,-1,"Scheme",[])
    self.__schemeControl.Enable(False)
    self.__environmentControl = ComboBoxPanel.ComboBoxPanel(self,-1,"Environment",[])
    self.__environmentControl.Enable(False)
    self.__versionControl = ComboBoxPanel.ComboBoxPanel(self,-1,"Version",[])
    self.__versionControl.Enable(False)
    
    sizer.Add(self.__descriptionControl,0,wx.ALL,5)
    sizer.Add(self.__commandControl,0,wx.ALL,5)
    sizer.Add(self.__databaseControl,0,wx.ALL,5)
    sizer.Add(self.__schemeControl,0,wx.ALL,5)
    sizer.Add(self.__environmentControl,0,wx.ALL,5)
    sizer.Add(self.__versionControl,0,wx.ALL,5)
    self.SetSizer(sizer)    
