import wx
import os
import sys
import AbstractFrame           as AbstractFrame
import panels.ActionPanel      as ActionPanel
import panels.HeaderPanel      as HeaderPanel
import core.ConfigReader       as ConfigReader
import core.ClassLoader        as ClassLoader
import core.ParameterHelper    as ParameterHelper
import core.Redirect           as Redirect
import core.NooraException     as NooraException
import core.CommandDispatcher  as CommandDispatcher
import core.PluginFinishedEvent as PluginFinishedEvent
import MainMenuBar             as MainMenuBar
import MainToolBar             as MainToolBar
import Settings                as Settings
import NewProjectDialog        as NewProjectDialog
import EditProjectDialog       as EditProjectDialog
import wx.lib.agw.flatnotebook as FlatNoteBook
import MainArtProvider         as MainArtProvider
import traceback

NOORA_DIR    = os.path.abspath(os.path.dirname(sys.argv[0]))
PLUGIN_DIR   = NOORA_DIR+os.sep+'plugins'
sys.path.append(PLUGIN_DIR)


class MainFrame(AbstractFrame.AbstractFrame):

  def getParameterHelper(self):
    parameterHelper=ParameterHelper.ParameterHelper()
    return parameterHelper
  
  def getActionControl(self):
    return self.__actionControl  
  
  def getConsole(self):
    return self.__console
  
  def getHeaderControl(self):
    return self.__headerControl

  def getDescriptionControl(self):
    actionControl=self.getActionControl()
    return actionControl.getDesciptionControl()
  
  def getDatabaseControl(self):
    actionControl=self.getActionControl()
    return actionControl.getDatabaseControl()

  def getSchemeControl(self):
    actionControl=self.getActionControl()
    return actionControl.getSchemeControl()
  
  def getEnvironmentControl(self):
    actionControl=self.getActionControl()
    return actionControl.getEnvironmentControl()

  def getVersionControl(self):
    actionControl=self.getActionControl()
    return actionControl.getVersionControl()

  def getCommandControl(self):
    actionControl=self.getActionControl()
    return actionControl.getCommandControl()
  
  def setConfigReader(self, configReader):
    self.__configReader=configReader
    
  def getConfigReader(self):
    return self.__configReader
      
  def getCommandDispatcher(self):
    return self.__commandDispatcher
  
  def setCommandDispatcher(self, commandDispatcher):
    self.__commandDispatcher=commandDispatcher
    
  def __init__(self, parent, title):

    AbstractFrame.AbstractFrame.__init__(self, parent, title)		
    
    mainMenuBar=MainMenuBar.MainMenuBar()
    self.SetMenuBar(mainMenuBar)
    mainToolBar=MainToolBar.MainToolBar(self,-1)
    self.SetToolBar(mainToolBar)
    mainToolBar.Realize()
    sizer=wx.BoxSizer(wx.VERTICAL)
    actionPanel = wx.Panel(self,-1)
    
    self.__headerControl = HeaderPanel.HeaderPanel(actionPanel, -1,"NoOra Project","")
    notebook = FlatNoteBook.FlatNotebook(actionPanel,-1,style=FlatNoteBook.FNB_FF2)
    style=notebook.GetWindowStyleFlag()
    style|=FlatNoteBook.FNB_VC8
    notebook.SetAGWWindowStyleFlag(style)
    images=wx.ImageList(16, 16)

    image=MainArtProvider.MainArtProvider.GetBitmap(Settings.ART_CONSOLE, wx.ART_TOOLBAR, (16, 16))
    images.Add(image)
    
    image=MainArtProvider.MainArtProvider.GetBitmap(Settings.ART_ACTION, wx.ART_TOOLBAR, (16, 16))
    images.Add(image)
    
    
    notebook.SetImageList(images)
    self.__actionControl = ActionPanel.ActionPanel(notebook,-1)
    self.__console = wx.TextCtrl(notebook,-1,style=wx.TE_MULTILINE)
    self.__console.SetEditable(False)
    
    notebook.AddPage(self.__actionControl,'Action',True,1)
    notebook.AddPage(self.__console,'Console',True,0)
    
    
    redirect=Redirect.Redirect(self.__console)
    sys.stdout=redirect
    sys.stderr=redirect
    
    sizer.Add(self.__headerControl,0,wx.EXPAND)
    sizer.Add(notebook,1,wx.EXPAND)
    
    actionPanel.SetSizer(sizer)
    
    self.Bind(wx.EVT_BUTTON, self.onOpenProject, id=Settings.ID_OPEN_PROJECT) 
    self.Bind(wx.EVT_MENU, self.onOpenProject, id=Settings.ID_OPEN_PROJECT)
    self.Bind(wx.EVT_MENU, self.onNewProject, id=Settings.ID_NEW_PROJECT)
    self.Bind(wx.EVT_MENU, self.onAbout, id=wx.ID_ABOUT)
    self.Bind(wx.EVT_MENU, self.onExit, id=wx.ID_EXIT)
    self.Bind(wx.EVT_MENU, self.onEditProject, id=Settings.ID_EDIT_PROJECT)

    self.Bind(wx.EVT_TOOL, self.onOpenProject, id=Settings.ID_OPEN_PROJECT)
    self.Bind(wx.EVT_TOOL, self.onNewProject, id=Settings.ID_NEW_PROJECT)
    self.Bind(wx.EVT_TOOL, self.onExecute, id=Settings.ID_EXECUTE)   
    self.Bind(wx.EVT_TOOL, self.onClear, id=Settings.ID_CLEAR)

    
    self.Connect(Settings.ID_OPEN_PROJECT, -1, Settings.EVT_PLUGIN_FINISHED, self.openProject)
    self.Bind(wx.EVT_COMBOBOX, self.onCommandChanged, id=Settings.ID_COMMAND)
    #self.Bind(Settings.EVT_PLUGIN_FINISHED, self.openProject, id=Settings.ID_OPEN_PROJECT)
    
    self.__statusBar = self.CreateStatusBar();
    self.__statusBar.SetStatusText("To create a new project, click on New Project in the Project menu")
    

  def onNewProject(self, evt): 
    try:
      newProjectDialog = NewProjectDialog.NewProjectDialog(self, -1, 'New Project')
      result = newProjectDialog.ShowModal()
      if result == Settings.ID_FINISH:
        configReader=ConfigReader.ConfigReader(NOORA_DIR+os.sep+"project.conf")
        self.setConfigReader(configReader)
        
        commandDispatcher=CommandDispatcher.CommandDispatcher(configReader, "generate")     
        os.chdir(newProjectDialog.getDirectory())
      
        if newProjectDialog.getProject():
          commandDispatcher.appendParameter("project", newProjectDialog.getDirectory()+os.sep+newProjectDialog.getProject())
      
        if newProjectDialog.getDatabase():
          commandDispatcher.appendParameter("database", newProjectDialog.getDatabase())

        if newProjectDialog.getScheme():
          commandDispatcher.appendParameter("scheme", newProjectDialog.getScheme())

        if newProjectDialog.getUsername():
          commandDispatcher.appendParameter("username", newProjectDialog.getUsername())

        if newProjectDialog.getPassword():
          commandDispatcher.appendParameter("password", newProjectDialog.getPassword())
      
        if newProjectDialog.getVersion():
          commandDispatcher.appendParameter("version", newProjectDialog.getVersion())

        commandDispatcher.executePlugin(Settings.ID_OPEN_PROJECT, self)
             
      newProjectDialog.Destroy()
    except NooraException.NooraException as e: 
      newProjectDialog.Destroy()     
      print e.getMessage()
    except:
      newProjectDialog.Destroy()
      print traceback.print_exc()


  def openProject(self, evt):  
    directory=evt.getDirectory()
    filename=evt.getFilename()

    headerControl=self.getHeaderControl()
    headerControl.getDescriptionControl().SetLabel(directory)
      
    os.chdir(directory)
    
    configReader=ConfigReader.ConfigReader(directory+os.sep+filename)
    self.setConfigReader(configReader)
      
    commandControl=self.getCommandControl()
    commandControl.clear()
    commandControl.setValue("")  
    commandControl.Enable(True)      
      
    plugins = configReader.getValue('PLUGINS')
    classLoader = ClassLoader.ClassLoader()
    for plugin in plugins:
      pluginClass=classLoader.findByPattern(plugin)
      if pluginClass.getType().lower()!="generate":
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
        

  def onOpenProject(self, evt): 
    openDialog = wx.FileDialog(self, "Choose a NoOra project file", "", "", "NoOra project files (project.conf)|project.conf", wx.OPEN)  
    if openDialog.ShowModal() == wx.ID_OK:
      filename=openDialog.GetFilenames()[0]
      directory=openDialog.GetDirectory()
      wx.PostEvent(self, PluginFinishedEvent.PluginFinishedEvent(Settings.ID_OPEN_PROJECT,directory, filename))   
    openDialog.Destroy()

    
  def onEditProject(self, evt):
    headerControl=self.getHeaderControl()
    directory=headerControl.getDescriptionControl().GetLabel()
    url=directory + os.sep + 'project.conf'
    
    editProjectDialog = EditProjectDialog.EditProjectDialog(self, -1, 'Edit project.conf', url)
    result = editProjectDialog.ShowModal()
    if result == Settings.ID_FINISH:
      pass

  def onExecute(self, evt):
    try:
      configReader=self.getConfigReader()
      commandDispatcher=CommandDispatcher.CommandDispatcher(configReader,self.getCommandControl().getValue())

      databaseControl=self.getDatabaseControl()
      if databaseControl.getValue():
        commandDispatcher.appendParameter("database", databaseControl.getValue())
          
      schemeControl=self.getSchemeControl()
      if schemeControl.getValue():
        commandDispatcher.appendParameter("scheme", schemeControl.getValue())

      environmentControl=self.getEnvironmentControl()
      if environmentControl.getValue():
        commandDispatcher.appendParameter("environment", environmentControl.getValue())

      versionControl=self.getVersionControl()
      if versionControl.getValue():
        commandDispatcher.appendParameter("version", versionControl.getValue())        

      commandDispatcher.executePlugin(Settings.ID_EXECUTE, self)
          
    except NooraException.NooraException as e:      
      print e.getMessage()
    except:
      print traceback.print_exc()

  def onClear(self, evt):
    console=self.getConsole()
    console.Clear()  
    
  def onAbout(self, evt):
    info = wx.AboutDialogInfo()
    info.Name = "NoOra Gui"
    info.Version = "0.0.7"
    info.Description ="NoOra is an attempt to apply a pattern to installing/updating Oracle database projects\r\nin order to promote portability and productivity. "
    info.Copyright = "(L) 2010, 2011 NoOra"
    info.WebSite = ("https://sourceforge.net/apps/trac/noora/", "NoOra home page")
    info.Developers = [ "Jan Ripke","Peter Kist","Gerry Duinkerken" ]
    wx.AboutBox(info)
    
  def onExit(self, evt):
    self.Close(True);    

  def onCommandChanged(self, evt):
    classLoader = ClassLoader.ClassLoader()
    configReader=self.getConfigReader()
    plugins = configReader.getValue('PLUGINS')
    for plugin in plugins:
      pluginClass=classLoader.findByPattern(plugin)
      if pluginClass.getType().lower()==self.getCommandControl().getValue():
        descriptionControl=self.getDescriptionControl()
        descriptionControl.SetLabel(pluginClass.getDescription())
        parameterDefinition=pluginClass.findParameterDefinition('database')
        if parameterDefinition:
          self.getDatabaseControl().Enable(True)
        else:
          self.getDatabaseControl().Enable(False)
          
        parameterDefinition=pluginClass.findParameterDefinition('scheme')
        if parameterDefinition:
          self.getSchemeControl().Enable(True)
        else:
          self.getSchemeControl().Enable(False)
        
        parameterDefinition=pluginClass.findParameterDefinition('environment')
        if parameterDefinition:
          self.getEnvironmentControl().Enable(True)
        else:
          self.getEnvironmentControl().Enable(False)
          
        parameterDefinition=pluginClass.findParameterDefinition('version')
        if parameterDefinition:
          versionControl=self.getVersionControl()
          versionControl.Enable(True)
          defaultVersion=pluginClass.getDefaultVersion()
          
          versionControl.clear()
          versions=pluginClass.getVersions(defaultVersion)
          for version in versions:
            if version!=defaultVersion:
              versionControl.append(version)
            
          versionControl.setValue(versions[len(versions)-1])
        else:
          self.getVersionControl().Enable(False)
        
    
      