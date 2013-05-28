import wx
import AbstractPanel as AbstractPanel

class ChoicePanel(AbstractPanel.AbstractPanel):

  def getChoiceControl(self):
    return self.__choiceControl
  
  def getValue(self):
    choiceControl=self.getChoiceControl()
    return choiceControl.GetValue()
  
  def setValue(self, value):
    choiceControl=self.getChoiceControl()
    choiceControl.SetValue(value)
    
  def clear(self):
    choiceControl=self.getChoiceControl()
    choiceControl.Clear()
    
  def append(self, choice):
    choiceControl=self.getChoiceControl()
    choiceControl.Append(choice)
  

  def __init__(self, parent, id, label, choices):
    AbstractPanel.AbstractPanel.__init__(self, parent, id)
    
    sizer=wx.BoxSizer(wx.HORIZONTAL)  
    self.__staticText = wx.StaticText(self, id, label)  
    self.__staticText.SetMinSize((100,20))      
    self.__choiceControl=wx.Choice(self, id, choices=choices)
    sizer.Add(self.__staticText,0)  
    sizer.Add(self.__choiceControl,1)
    self.SetSizer(sizer)    
