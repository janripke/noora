import wx
import panels.BrowsePanel           as BrowsePanel
import panels.TextPanel             as TextPanel
import panels.CancelFinishPanel     as CancelFinishPanel
import panels.HeaderPanel           as HeaderPanel
import gui.Settings                 as Settings

class NewProjectDialog(wx.Dialog):

    def getProjectControl(self):
      return self.__projectControl
    
    def getBrowseControl(self):
      return self.__browseControl
    
    def getDatabaseControl(self):
      return self.__databaseControl
    
    def getSchemeControl(self):
      return self.__schemeControl
    
    def getUsernameControl(self):
      return self.__usernameControl
    
    def getPasswordControl(self):
      return self.__passwordControl

    def getVersionControl(self):
      return self.__versionControl
    
    def getProject(self):
      projectControl=self.getProjectControl()
      return projectControl.getValue()
    
    def getDirectory(self):
      browseControl=self.getBrowseControl()
      return browseControl.getValue()

    def getDatabase(self):
      databaseControl=self.getDatabaseControl()
      return databaseControl.getValue()

    def getScheme(self):
      schemeControl=self.getSchemeControl()
      return schemeControl.getValue()

    def getUsername(self):
      usernameControl=self.getUsernameControl()
      return usernameControl.getValue()

    def getPassword(self):
      passwordControl=self.getPasswordControl()
      return passwordControl.getValue()

    def getVersion(self):
      versionControl=self.getVersionControl()
      return versionControl.getValue()



        
    def __init__(self, parent, id, title):
        
        wx.Dialog.__init__(self, parent, id, title, style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.__headerPanel = HeaderPanel.HeaderPanel(self, -1,"NoOra Project","Create a new NoOra Project")
        self.__projectControl=TextPanel.TextPanel(self,-1,"Project name:")
        self.__browseControl = BrowsePanel.BrowsePanel(self,-1,"Directory")
        self.__databaseControl = TextPanel.TextPanel(self,-1,"Database")
        self.__schemeControl = TextPanel.TextPanel(self,-1,"Scheme")
        self.__usernameControl = TextPanel.TextPanel(self,-1,"Username")
        self.__passwordControl = TextPanel.TextPanel(self,-1,"Password")
        self.__versionControl = TextPanel.TextPanel(self,-1,"Version")
        self.__cancelFinishControl=CancelFinishPanel.CancelFinishPanel(self,-1)
        
        sizer.Add(self.__headerPanel,0,wx.EXPAND)   
        sizer.Add(self.__projectControl,0,wx.ALL|wx.EXPAND,5)
        sizer.Add(self.__browseControl,0,wx.ALL|wx.EXPAND,5)
        sizer.Add(self.__databaseControl,0,wx.ALL|wx.EXPAND,5)
        sizer.Add(self.__schemeControl,0,wx.ALL|wx.EXPAND,5)
        sizer.Add(self.__usernameControl,0,wx.ALL|wx.EXPAND,5)
        sizer.Add(self.__passwordControl,0,wx.ALL|wx.EXPAND,5)
        sizer.Add(self.__versionControl,0,wx.ALL|wx.EXPAND,5)
        
        sizer.Add(self.__cancelFinishControl,0,wx.ALIGN_RIGHT|wx.ALL,5)

                
        self.SetSizer(sizer)
        self.SetMinSize((460,380))

        
        self.Bind(wx.EVT_BUTTON, self.onCancel, id=Settings.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.onFinish, id=Settings.ID_FINISH)
        self.Bind(wx.EVT_BUTTON, self.onOpen, id=Settings.ID_OPEN)
        
        self.__versionControl.setValue("1.0.0")

    def onCancel(self, evt):
      self.EndModal(Settings.ID_CANCEL)
            
    def onFinish(self, evt): 
      self.EndModal(Settings.ID_FINISH)
 

    def onOpen(self, evt): 
      dirDialog = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)  
      if dirDialog.ShowModal() == wx.ID_OK:
        dirname=dirDialog.GetPath()
        self.__browseControl.setValue(dirname)    