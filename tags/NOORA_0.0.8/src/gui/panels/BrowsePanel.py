import wx
import AbstractPanel as AbstractPanel
import gui.Settings  as Settings

class BrowsePanel(AbstractPanel.AbstractPanel):

  def getUrlTextControl(self):
    return self.__urlTextControl
  
  def getValue(self):
    urlTextControl=self.getUrlTextControl()
    return urlTextControl.GetValue()
  
  def setValue(self, value):
    urlTextControl=self.getUrlTextControl()
    urlTextControl.SetValue(value)

  def __init__(self, parent, id, label):
    AbstractPanel.AbstractPanel.__init__(self, parent, id)
    
    sizer=wx.BoxSizer(wx.HORIZONTAL) 
    self.__staticText = wx.StaticText(self, id, label)        
    self.__urlTextControl=wx.TextCtrl(self, id)
    self.__browseButton = wx.Button(self, Settings.ID_OPEN, "Browse") 

    width,height=self.__urlTextControl.GetSize().Get()       
    self.__staticText.SetMinSize((100,height))  
    
    sizer.Add(self.__staticText,0)     
    sizer.Add(self.__urlTextControl,1)
    sizer.Add(self.__browseButton,0)
    self.SetSizer(sizer)    
