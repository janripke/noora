import wx
import AbstractPanel as AbstractPanel

class HeaderPanel(AbstractPanel.AbstractPanel):

  def getDescriptionControl(self):
    return self.__descriptionStaticText

  def __init__(self, parent, id, name, description):
    AbstractPanel.AbstractPanel.__init__(self, parent, id)
    
    sizer=wx.BoxSizer(wx.VERTICAL)  
    self.__nameStaticText = wx.StaticText(self, id, name)      
    font=wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
    self.__nameStaticText.SetFont(font)
    
    self.__descriptionStaticText = wx.StaticText(self, id, description,style=wx.BOLD)
    
    
    sizer.Add(self.__nameStaticText,1,wx.ALL,10)  
    sizer.Add(self.__descriptionStaticText,1,wx.ALL,10)
    self.SetSizer(sizer)    
    self.SetBackgroundColour('WHITE')
