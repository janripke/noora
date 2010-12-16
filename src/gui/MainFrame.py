import wx
import wx.stc
import os
import sys
import AbstractFrame        as AbstractFrame
import panels.BrowsePanel   as BrowsePanel
import panels.ComboBoxPanel as ComboBoxPanel
import panels.ExecutePanel  as ExecutePanel
import panels.ActionPanel   as ActionPanel
import core.ConfigReader    as ConfigReader
import core.ClassLoader     as ClassLoader
import core.ParameterHelper as ParameterHelper
import core.Redirect        as Redirect
import core.NooraException  as NooraException
import MainMenuBar          as MainMenuBar
import Settings             as Settings
import NewProjectDialog     as NewProjectDialog

NOORA_DIR    = os.path.abspath(os.path.dirname(sys.argv[0]))
PLUGIN_DIR   = NOORA_DIR+os.sep+'plugins'
sys.path.append(PLUGIN_DIR)


class MainFrame(AbstractFrame.AbstractFrame):

  def getParameterHelper(self):
    parameterHelper=ParameterHelper.ParameterHelper()
    return parameterHelper

  def getBrowseControl(self):
    return self.__browseControl  
  
  def getActionControl(self):
    return self.__actionControl  
  
  def getConsole(self):
    return self.__console
  
  def getDatabaseControl(self):
    actionControl=self.getActionControl()
    return actionControl.getDatabaseControl()

  def getSchemeControl(self):
    actionControl=self.getActionControl()
    return actionControl.getSchemeControl()
  
  def getEnvironmentControl(self):
    actionControl=self.getActionControl()
    return actionControl.getEnvironmentControl()

  def getCommandControl(self):
    actionControl=self.getActionControl()
    return actionControl.getCommandControl()
  
  def setConfigReader(self, configReader):
    self.__configReader=configReader
    
  def getConfigReader(self):
    return self.__configReader
    
  def __init__(self, parent, title):

    AbstractFrame.AbstractFrame.__init__(self, parent, title)		
    
    mainMenuBar=MainMenuBar.MainMenuBar()
    self.SetMenuBar(mainMenuBar)
    
    sizer=wx.BoxSizer(wx.VERTICAL)
    actionPanel = wx.Panel(self,-1, style=wx.SUNKEN_BORDER)
    self.__browseControl = BrowsePanel.BrowsePanel(actionPanel,-1,"Direcory")
    self.__actionControl = ActionPanel.ActionPanel(actionPanel,-1)
    self.__executeControl=ExecutePanel.ExecutePanel(actionPanel,-1)
    self.__console = wx.TextCtrl(actionPanel,-1,style=wx.TE_MULTILINE)
    self.__console.SetEditable(False)
    redirect=Redirect.Redirect(self.__console)
    sys.stdout=redirect
    sys.stderr=redirect
    
    #sizer.Add(projectGroup,0,wx.EXPAND)
    sizer.Add(self.__browseControl,0,wx.EXPAND)
    sizer.Add(self.__actionControl,0,wx.EXPAND)
    sizer.Add(self.__executeControl,0,wx.EXPAND)
    sizer.Add(self.__console,1,wx.EXPAND)
    
    actionPanel.SetSizer(sizer)
    
    self.Bind(wx.EVT_BUTTON, self.OnOpenProject, id=Settings.ID_OPEN_PROJECT) 
    self.Bind(wx.EVT_BUTTON, self.OnExecute, id=12000)   
    self.Bind(wx.EVT_BUTTON, self.OnClear, id=12001)
    self.Bind(wx.EVT_MENU, self.OnOpenProject, id=Settings.ID_OPEN_PROJECT)
    self.Bind(wx.EVT_MENU, self.OnNewProject, id=Settings.ID_NEW_PROJECT)
    
    self.__statusBar = self.CreateStatusBar();
    self.__statusBar.SetStatusText("To generate a new project, click on New Project in the Project menu, select a project directory and click on execute")


  def OnNewProject(self, evt): 
    newProjectDialog = NewProjectDialog.NewProjectDialog(self, -1, 'New Project')
    result = newProjectDialog.ShowModal()
    if result == Settings.ID_FINISH:
      configReader=ConfigReader.ConfigReader(NOORA_DIR+os.sep+"project.conf")
      self.setConfigReader(configReader)
      print "finished"
    newProjectDialog.Destroy()


  def OnOpenProject(self, evt): 
    openDialog = wx.FileDialog(self, "Choose a NoOra project file", "", "", "NoOra project files (project.conf)|project.conf", wx.OPEN)  
    if openDialog.ShowModal() == wx.ID_OK:
      browseControl=self.getBrowseControl()
      filename=openDialog.GetFilenames()[0]
      dirname=openDialog.GetDirectory()
      
      browseControl.setValue(dirname+os.sep+filename)
      os.chdir(dirname)
      
      configReader=ConfigReader.ConfigReader(dirname+os.sep+filename)
      self.setConfigReader(configReader)
      
      commandControl=self.getCommandControl()
      commandControl.clear()        
      
      plugins = configReader.getValue('PLUGINS')
      classLoader = ClassLoader.ClassLoader()
      for plugin in plugins:
        pluginClass=classLoader.findByPattern(plugin)
        commandControl.append(pluginClass.getType().lower())
        
      databases = configReader.getValue('ORACLE_SIDS')
      databaseControl=self.getDatabaseControl()
      databaseControl.clear()
      for database in databases:
        databaseControl.append(database)
      
      schemes = configReader.getValue('SCHEMES')
      schemeControl=self.getSchemeControl()
      schemeControl.clear()
      for scheme in schemes:
        schemeControl.append(scheme)
          
      environments = configReader.getValue('ENVIRONMENTS')
      defaultEnvironment = configReader.getValue('DEFAULT_ENVIRONMENT')
      environmentControl=self.getEnvironmentControl()
      environmentControl.clear()
      for environment in environments:
        environmentControl.append(environment)
      environmentControl.setValue(defaultEnvironment)          
    
    openDialog.Destroy()

  def OnExecute(self, evt):
    try:
      databaseControl=self.getDatabaseControl()
      environmentControl=self.getEnvironmentControl()
      classLoader = ClassLoader.ClassLoader()
      configReader=self.getConfigReader()
      plugins = configReader.getValue('PLUGINS')
      for plugin in plugins:
        pluginClass=classLoader.findByPattern(plugin)
        if pluginClass.getType().lower()==self.getCommandControl().getValue():
          parameterHelper=self.getParameterHelper()
          
          parameters=[]
          if databaseControl.getValue():
            parameters.append("-s="+databaseControl.getValue())
            
          if environmentControl.getValue():
            parameters.append("-e="+environmentControl.getValue())
          
          parameterHelper.setParameters(parameters)
          pluginClass.execute(parameterHelper)
    except NooraException.NooraException as e:
      print e.getMessage()
    except:
      print "unknown error"

  def OnClear(self, evt):
    console=self.getConsole()
    console.Clear()    
