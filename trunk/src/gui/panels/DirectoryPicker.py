import wx
import gui.panels.AbstractPanel as AbstractPanel

class DirectoryPicker(AbstractPanel.AbstractPanel):

    def getDirectory(self):
        return self.__directory
  
    def getValue(self):
        return self.__directory.GetValue();
  
    def setValue(self, value):
        self.__directory.SetValue(value);

    def onBrowse(self, event):
        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dlg.ShowModal() == wx.ID_OK:
            self.setValue(dlg.GetPath())
        dlg.Destroy()

    def __init__(self, parent, id):
        AbstractPanel.AbstractPanel.__init__(self, parent, wx.NewId())
    
        sizer=wx.BoxSizer(wx.HORIZONTAL)        
        self.__directory=wx.TextCtrl(self, id)
        self.__browseButton = wx.Button(self, wx.NewId(), "Browse")  
        sizer.Add(wx.StaticText(self,wx.NewId(),"Choose directory"))
        sizer.Add(self.__directory,1)
        sizer.Add(self.__browseButton,0)
        self.SetSizer(sizer)
      
        wx.EVT_BUTTON(self, self.__browseButton.GetId(), self.onBrowse)  
