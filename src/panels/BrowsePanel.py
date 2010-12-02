import wx
import AbstractPanel as AbstractPanel

class BrowsePanel(AbstractPanel.AbstractPanel):

  def getUrlTextControl(self):
    return self.__urlTextControl
  
  def getValue(self):
    urlTextControl=self.getUrlTextControl()
    return urlTextControl.GetValue()
  
  def setValue(self, value):
    urlTextControl=self.getUrlTextControl()
    urlTextControl.SetValue(value)

  def __init__(self, parent, id):
    AbstractPanel.AbstractPanel.__init__(self, parent, id)
    
    sizer=wx.BoxSizer(wx.HORIZONTAL)        
    self.__urlTextControl=wx.TextCtrl(self, id)
    self.__browseButton = wx.Button(self, wx.ID_OPEN, "Browse")  
    sizer.Add(self.__urlTextControl,1)
    sizer.Add(self.__browseButton,0)
    self.SetSizer(sizer)    
