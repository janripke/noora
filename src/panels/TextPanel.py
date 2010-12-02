import wx
import AbstractPanel as AbstractPanel

class TextPanel(AbstractPanel.AbstractPanel):

  def getTextControl(self):
    return self.__textControl
  
  def getValue(self):
    textControl=self.getTextControl()
    return textControl.GetValue()
  
  def setValue(self, value):
    textControl=self.getTextControl()
    textControl.SetValue(value)

  def __init__(self, parent, id, label):
    AbstractPanel.AbstractPanel.__init__(self, parent, id)
    
    sizer=wx.BoxSizer(wx.HORIZONTAL)  
    self.__staticText = wx.StaticText(self, id, label)  
    self.__staticText.SetMinSize((100,20))      
    self.__textControl=wx.TextCtrl(self, id)
    sizer.Add(self.__staticText,0)  
    sizer.Add(self.__textControl,1)
    self.SetSizer(sizer)    
