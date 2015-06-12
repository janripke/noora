import wx
import AbstractPanel as AbstractPanel

class ComboBoxPanel(AbstractPanel.AbstractPanel):

  def getComboBoxControl(self):
    return self.__comboBoxControl
  
  def getValue(self):
    comboBoxControl=self.getComboBoxControl()
    return comboBoxControl.GetValue()
  
  def setValue(self, value):
    comboBoxControl=self.getComboBoxControl()
    comboBoxControl.SetValue(value)
    
  def clear(self):
    comboBoxControl=self.getComboBoxControl()
    comboBoxControl.Clear()
    
  def append(self, choice):
    comboBoxControl=self.getComboBoxControl()
    comboBoxControl.Append(choice)
  
  def appendItems(self, choices):
    comboBoxControl=self.getComboBoxControl()
    comboBoxControl.AppendItems(choices)
  
  def setItems(self, choices):
    comboBoxControl=self.getComboBoxControl()
    comboBoxControl.SetItems(choices)
    

  def __init__(self, parent, id, label, choices):
    AbstractPanel.AbstractPanel.__init__(self, parent, id)
    
    sizer=wx.BoxSizer(wx.HORIZONTAL)  
    self.__staticText = wx.StaticText(self, id, label)  
    self.__staticText.SetMinSize((100,20))      
    self.__comboBoxControl=wx.ComboBox(self, id, choices=choices)
    #width = self.__comboBoxControl.GetSize()[0]
    
    #self.__comboBoxControl.SetMinSize((width,30))
    sizer.Add(self.__staticText,0)  
    sizer.Add(self.__comboBoxControl,1)
    self.SetSizer(sizer)    
