import wx
import AbstractPanel as AbstractPanel
import gui.Settings      as Settings

class CancelFinishPanel(AbstractPanel.AbstractPanel):

  def getCancelButton(self):
    return self.__cancelButton
  
  def getFinishButton(self):
    return self.__finishButton

  def __init__(self, parent, id):
    AbstractPanel.AbstractPanel.__init__(self, parent, id)
    
    sizer=wx.BoxSizer(wx.HORIZONTAL)        
    self.__cancelButton=wx.Button(self, Settings.ID_CANCEL,"Cancel") 
    self.__finishButton = wx.Button(self, Settings.ID_FINISH,"Finish")  
    sizer.Add(self.__cancelButton,0,wx.EXPAND)
    sizer.Add(self.__finishButton,0,wx.EXPAND)
    self.SetSizer(sizer)    
    self.Layout()
