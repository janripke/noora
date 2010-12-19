import wx
import AbstractPanel as AbstractPanel
import gui.Settings  as Settings

class ExecutePanel(AbstractPanel.AbstractPanel):

  def getExecuteButton(self):
    return self.__executeButton
  
  def getClearButton(self):
    return self.__clearButton

  def __init__(self, parent, id):
    AbstractPanel.AbstractPanel.__init__(self, parent, id)
    
    sizer=wx.BoxSizer(wx.HORIZONTAL)        
    self.__executeButton=wx.Button(self, Settings.ID_EXECUTE,"Execute") 
    self.__clearButton = wx.Button(self, Settings.ID_CLEAR,"Clear")  
    sizer.Add(self.__executeButton,0)
    sizer.Add(self.__clearButton,0)
    self.SetSizer(sizer)    
