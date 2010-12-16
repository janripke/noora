import wx
import panels.BrowsePanel           as BrowsePanel
import panels.TextPanel             as TextPanel
import panels.CancelFinishPanel     as CancelFinishPanel
import gui.Settings                 as Settings

class NewProjectDialog(wx.Dialog):

    def getProjectControl(self):
      return self.__projectControl
    
    def getBrowseControl(self):
      return self.__browseControl
    
    def getProject(self):
      projectControl=self.getProjectControl()
      return projectControl.getValue()
    
    def getDirectory(self):
      browseControl=self.getBrowseControl()
      return browseControl.getValue()
        
    def __init__(self, parent, id, title):
        
        wx.Dialog.__init__(self, parent, id, title, style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.__headerPanel = wx.Panel(self,-1)
        self.__projectControl=TextPanel.TextPanel(self,-1,"Project")
        self.__browseControl = BrowsePanel.BrowsePanel(self,-1,"Directory")
        self.__spacerPanel = wx.Panel(self,-1)
        self.__cancelFinishControl=CancelFinishPanel.CancelFinishPanel(self,-1)
        sizer.Add(self.__headerPanel,0,wx.EXPAND)   
        sizer.Add(self.__projectControl,0,wx.EXPAND)
        sizer.Add(self.__browseControl,0,wx.EXPAND)
        sizer.Add(self.__spacerPanel,1,wx.EXPAND)
        sizer.Add(self.__cancelFinishControl,0,wx.ALIGN_RIGHT)
                
        self.SetSizer(sizer)
        
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=Settings.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.OnFinish, id=Settings.ID_FINISH)
        self.Bind(wx.EVT_BUTTON, self.OnOpen, id=Settings.ID_OPEN)

    def OnCancel(self, evt):
      self.EndModal(Settings.ID_CANCEL)
      self.Close() 
      
    def OnFinish(self, evt): 
      self.EndModal(Settings.ID_FINISH)          
      self.Close() 

    def OnOpen(self, evt): 
      dirDialog = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)  
      if dirDialog.ShowModal() == wx.ID_OK:
        dirname=dirDialog.GetPath()
        self.__browseControl.setValue(dirname)    