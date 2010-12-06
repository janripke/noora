import wx
import AbstractPanel        as AbstractPanel
import panels.ComboBoxPanel as ComboBoxPanel

class ActionPanel(AbstractPanel.AbstractPanel):

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
    self.__commandControl=ComboBoxPanel.ComboBoxPanel(self,-1,"Command",[])
    self.__databaseControl = ComboBoxPanel.ComboBoxPanel(self,-1,"Database",[])
    self.__schemeControl = ComboBoxPanel.ComboBoxPanel(self,-1,"Scheme",[])
    self.__environmentControl = ComboBoxPanel.ComboBoxPanel(self,-1,"Environment",[])
    self.__versionControl = ComboBoxPanel.ComboBoxPanel(self,-1,"Version",[])
    
    sizer.Add(self.__commandControl,0)
    sizer.Add(self.__databaseControl,0)
    sizer.Add(self.__schemeControl,0)
    sizer.Add(self.__environmentControl,0)
    sizer.Add(self.__versionControl,0)
    self.SetSizer(sizer)    
