import wx
import os
import core.ClassLoader      as ClassLoader
import core.NooraException   as NooraException
import core.ParameterHelper  as ParameterHelper
import core.PluginFinishedEvent as PluginFinishedEvent
from threading import Thread


class ExecuteThread(Thread):

  def __init__(self, pluginClass, parameterHelper, parent):
    Thread.__init__(self)
    self.__pluginClass=pluginClass
    self.__parameterHelper=parameterHelper
    self.__parent=parent
    self.start()
 
  def run(self):
    try:
      self.__pluginClass.execute(self.__parameterHelper)
      filename=self.__pluginClass.getConfigReader().getFilename()
      wx.PostEvent(self.__parent, PluginFinishedEvent.PluginFinishedEvent(os.path.abspath('.'), filename))
    except NooraException.NooraException as e:      
      print e.getMessage()
      exit(1)


class CommandDispatcher:
  '''
  This class will invoke the specified command. It will read the project configuration and
  use the specified arguments to dispatch the correct command.
  '''
  
  def getConfigReader(self):
    return self.__configReader

  def getParameterHelper(self):
    return self.__parameterHelper
  
  def __init__(self, configReader, type):
    self.__configReader=configReader
    self.__plugin=None
    self.__parameterHelper=ParameterHelper.ParameterHelper()
    classLoader = ClassLoader.ClassLoader()
    plugins = configReader.getValue('PLUGINS')
    for plugin in plugins:
      pluginClass=classLoader.findByPattern(plugin)
      if pluginClass.getType().lower()==type.lower():
        self.__plugin=pluginClass
        
  def getPlugin(self):
    return self.__plugin
  
  def getParameterDefinitions(self):
    plugin=self.getPlugin()
    return plugin.getParameterDefinitions()
  
  def appendParameter(self, parameter, value):
    parameters=self.getParameterHelper().getParameters()
    parameterDefinitions=self.getParameterDefinitions()
    for parameterDefinition in parameterDefinitions:
      if parameterDefinition.getKey()==parameter:
        parameters.append(parameterDefinition.getFirstParameter()+"="+value)
  
  def executePlugin(self, parent):
    plugin=self.getPlugin()
    parameterHelper=self.getParameterHelper()
    ExecuteThread(plugin, parameterHelper, parent)

            

    

        