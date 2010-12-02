import wx
import wx.stc
import os
import sys
import AbstractFrame as AbstractFrame
import panels.BrowsePanel as BrowsePanel
import panels.TextPanel as TextPanel
import panels.ComboBoxPanel as ComboBoxPanel
import core.ConfigReader as ConfigReader
import core.ClassLoader     as ClassLoader
import core.ParameterHelper as ParameterHelper
import core.Redirect as Redirect
import core.NooraException as NooraException
import subprocess

NOORA_DIR    = os.path.abspath(os.path.dirname(sys.argv[0]))
PLUGIN_DIR   = NOORA_DIR+os.sep+'plugins'
sys.path.append(PLUGIN_DIR)


class MainFrame(AbstractFrame.AbstractFrame):

  def getParameterHelper(self):
    parameterHelper=ParameterHelper.ParameterHelper()
    return parameterHelper
		
  def getBrowsePanel(self):
    return self.__browsePanel    
  
  def getConsole(self):
    return self.__console
  
  def getDatabaseControl(self):
    return self.__databaseControl

  def getSchemeControl(self):
    return self.__schemeControl
  
  def getEnvironmentControl(self):
    return self.__environmentControl
  
  def getCommandControl(self):
    return self.__commandControl
  
  def setConfigReader(self, configReader):
    self.__configReader=configReader
    
  def getConfigReader(self):
    return self.__configReader
    
  def __init__(self, parent, title):

    AbstractFrame.AbstractFrame.__init__(self, parent, title)		
    
    
    sizer=wx.BoxSizer(wx.VERTICAL)
    actionPanel = wx.Panel(self,-1, style=wx.SUNKEN_BORDER)
    self.__browsePanel = BrowsePanel.BrowsePanel(actionPanel,-1)
    self.__commandControl = ComboBoxPanel.ComboBoxPanel(actionPanel,-1,"Command",['drop','generate'])
    self.__databaseControl = ComboBoxPanel.ComboBoxPanel(actionPanel,-1,"Database",[])
    self.__schemeControl = ComboBoxPanel.ComboBoxPanel(actionPanel,-1,"Scheme",[])
    self.__environmentControl = ComboBoxPanel.ComboBoxPanel(actionPanel,-1,"Environment",[])
    self.__executeButton = wx.Button(actionPanel,12000,"Execute")
    self.__clearButton = wx.Button(actionPanel,12001,"Clear")
    self.__console = wx.TextCtrl(actionPanel,-1,style=wx.TE_MULTILINE)
    self.__console.SetEditable(False)
    redirect=Redirect.Redirect(self.__console)
    sys.stdout=redirect
    sys.stderr=redirect
    
    


    #sizer.Add(projectGroup,0,wx.EXPAND)
    sizer.Add(self.__browsePanel,1,wx.EXPAND)
    sizer.Add(self.__commandControl,1,wx.EXPAND)
    sizer.Add(self.__databaseControl,1,wx.EXPAND)
    sizer.Add(self.__schemeControl,1,wx.EXPAND)
    sizer.Add(self.__environmentControl,1,wx.EXPAND)
    sizer.Add(self.__executeButton,0)
    sizer.Add(self.__clearButton,0)
    sizer.Add(self.__console,1,wx.EXPAND)
    
    actionPanel.SetSizer(sizer)
    
    self.Bind(wx.EVT_BUTTON, self.OnOpen, id=wx.ID_OPEN) 
    self.Bind(wx.EVT_BUTTON, self.OnExecute, id=12000)   
    self.Bind(wx.EVT_BUTTON, self.OnClear, id=12001)
    self.Bind(wx.EVT_MENU, self.OnOpen, id=wx.ID_OPEN)

  def OnOpen(self, evt): 
    openDialog = wx.FileDialog(self, "Choose a NoOra project file", "", "", "NoOra project files (project.conf)|project.conf", wx.OPEN+wx.FD_MULTIPLE)  
    if openDialog.ShowModal() == wx.ID_OK:
      browsePanel=self.getBrowsePanel()
      filenames=openDialog.GetFilenames()
      dirname=openDialog.GetDirectory()
      for filename in filenames:
        browsePanel.setValue(dirname+os.sep+filename)
        os.chdir(dirname)
        configReader=ConfigReader.ConfigReader(dirname+os.sep+filename)
        self.setConfigReader(configReader)
        commandControl=self.getCommandControl()
        commandControl.clear()        
        plugins = configReader.getValue('PLUGINS')
        console=self.getConsole()
        classLoader = ClassLoader.ClassLoader()
        for plugin in plugins:
          pluginClass=classLoader.findByPattern(plugin)
          commandControl.append(pluginClass.getType())
          
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
      console=self.getConsole()
      databaseControl=self.getDatabaseControl()
      classLoader = ClassLoader.ClassLoader()
      configReader=self.getConfigReader()
      plugins = configReader.getValue('PLUGINS')
      for plugin in plugins:
        pluginClass=classLoader.findByPattern(plugin)
        if pluginClass.getType()==self.getCommandControl().getValue():
          parameterHelper=self.getParameterHelper()
          
          
          
          parameterHelper.setParameters(['-s=orcl','-e=dev'])
          pluginClass.execute(parameterHelper)
    except NooraException.NooraException as e:
      print e.getMessage()

  def OnClear(self, evt):
    console=self.getConsole()
    console.Clear()    
