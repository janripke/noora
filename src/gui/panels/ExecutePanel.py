import wx
import AbstractPanel as AbstractPanel

class ExecutePanel(AbstractPanel.AbstractPanel):

  def getExecuteButton(self):
    return self.__executeButton
  
  def getClearButton(self):
    return self.__clearButton

  def __init__(self, parent, id):
    AbstractPanel.AbstractPanel.__init__(self, parent, id)
    
    sizer=wx.BoxSizer(wx.HORIZONTAL)        
    self.__executeButton=wx.Button(self, 12000,"Execute") 
    self.__clearButton = wx.Button(self, 12001,"Clear")  
    sizer.Add(self.__executeButton,0)
    sizer.Add(self.__clearButton,0)
    self.SetSizer(sizer)    
