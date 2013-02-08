import wx
import os
import core.ClassLoader         as ClassLoader
import core.NooraException      as NooraException
import core.ParameterHelper     as ParameterHelper
import core.PluginFinishedEvent as PluginFinishedEvent
import core.PluginManager       as PluginManager
from threading import Thread

class PluginExecutionContext:
  
  def __init__(self, parent, id, plugin):
    self.__command = plugin.getType() 
    self.__plugin = plugin
    self.__parent = parent
    self.__id = id
    self.__parameterHelper=ParameterHelper.ParameterHelper()
    
  def getParameterHelper(self):
    return self.__parameterHelper
  
  def getPlugin(self):
    return self.__plugin
  
  def getParent(self):
    return self.__parent
  
  def getId(self):
    return self.__id
  
  def addExecutionParameter(self, parameter, value):
    if value:
      parameters=self.getParameterHelper().getParameters()
      parameterDefinitions=self.getPlugin().getParameterDefinitions()
      for parameterDefinition in parameterDefinitions:
        if parameterDefinition.getKey()==parameter:
          parameters.append(parameterDefinition.getFirstParameter()+"="+value)

class ExecuteThread(Thread):

  def __init__(self, executionContext):
    Thread.__init__(self)
    self.__executionContext=executionContext
    self.start()
    
  def getExecutionContext(self):
    return self.__executionContext
 
  def run(self):
    try:
      executionContext=self.getExecutionContext()
      plugin=executionContext.getPlugin()
      parameterHelper=executionContext.getParameterHelper()
      id=executionContext.getId()
      plugin.execute(parameterHelper)
      filename=plugin.getConfigReader().getFilename()
      wx.PostEvent(None, PluginFinishedEvent.PluginFinishedEvent(id, os.path.abspath('.'), filename))
    except NooraException.NooraException as e:      
      print e.getMessage()
      exit(1)


class CommandDispatcher:
  '''
  This class will invoke the specified command. It will read the project configuration and
  use the specified arguments to execute the correct plugin.
  '''
  def __init__(self, configReader):
    self.__pluginManager=PluginManager.PluginManager()
    self.setConfigReader(configReader)
    self.__parameterHelper=ParameterHelper.ParameterHelper()
  
  def getConfigReader(self):
    return self.__configReader

  def setConfigReader(self, configReader):
    self.__configReader=configReader
    self.loadPluginDefinitionsFromConfigReader()
    self.registerPlugins()

  def getParameterHelper(self):
    return self.__parameterHelper
  
  def setPluginManager(self, pluginManager):
    self.__pluginManager=pluginManager
    
  def getPluginManager(self):
    return self.__pluginManager
  
  def setPluginDefinitions(self, pluginDefinitions):
    ''' Sets the list of plugin definitions.
    '''
    self.__pluginDefinitions = pluginDefinitions  
  
  def getPluginDefinitions(self):
    return self.__pluginDefinitions
  
  def loadPluginDefinitionsFromConfigReader(self):
    ''' retrieves the plugin definitions using the ConfigReader.
    '''
    configReader=self.getConfigReader()
    self.setPluginDefinitions(configReader.getValue('PLUGINS'))
  
  def registerPlugins(self):
    classLoader = ClassLoader.ClassLoader()
    pluginManager = self.getPluginManager()
    pluginDefinitions = self.getPluginDefinitions()
    for pluginDefinition in pluginDefinitions:
      plugin=classLoader.findByPattern(pluginDefinition)
      pluginManager.registerPlugin(plugin)

  def getPluginTypes(self):
    pluginTypes=[]
    pluginManager = self.getPluginManager()
    plugins = pluginManager.getPlugins()
    for plugin in plugins:
      pluginTypes.append(plugin.getType().lower())
    return pluginTypes
        
  def getPlugin(self, type):
    pluginManager=self.getPluginManager()
    return pluginManager.findPlugin(type)

  def getPluginParameterDefinitions(self, type):
    plugin=self.getPlugin(type)
    return plugin.getParameterDefinitions()
        
  def createExecutionContext(self, parent, id, command):  
    plugin = self.getPlugin(command)  
    executionContext = PluginExecutionContext(parent, id, plugin)
    return executionContext
  
  def execute(self, executionContext):
    ExecuteThread(executionContext)
  

            

    

        