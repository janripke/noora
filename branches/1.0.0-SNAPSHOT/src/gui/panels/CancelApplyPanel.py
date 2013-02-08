import wx
import AbstractPanel as AbstractPanel
import gui.Settings      as Settings

class CancelApplyPanel(AbstractPanel.AbstractPanel):

  def getCancelButton(self):
    return self.__cancelButton
  
  def getApplyButton(self):
    return self.__applyButton

  def __init__(self, parent, id):
    AbstractPanel.AbstractPanel.__init__(self, parent, id)
    
    sizer=wx.BoxSizer(wx.HORIZONTAL)        
    self.__cancelButton=wx.Button(self, Settings.ID_CANCEL,"Cancel") 
    self.__applyButton = wx.Button(self, Settings.ID_APPLY,"Apply")  
    sizer.Add(self.__cancelButton,0,wx.EXPAND)
    sizer.Add(self.__applyButton,0,wx.EXPAND)
    self.SetSizer(sizer)    
    self.Layout()
