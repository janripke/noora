import core.ClassLoader      as ClassLoader
import core.NooraException   as NooraException
from threading import Thread


class ExecuteThread(Thread):

  def __init__(self, pluginClass, parameterHelper):
    Thread.__init__(self)
    self.__pluginClass=pluginClass
    self.__parameterHelper=parameterHelper
    self.start()
 
  def run(self):
    try:
      self.__pluginClass.execute(self.__parameterHelper)
    except NooraException.NooraException as e:      
      print e.getMessage()
      exit(1)


class CommandDispatcher:
  '''
  This class will invoke the specified command. It will read the project configuration and
  use the specified arguments to dispatch the correct command.
  '''
  
  def __init__(self, configReader, type):
    self.__plugin=None
    classLoader = ClassLoader.ClassLoader()
    plugins = configReader.getValue('PLUGINS')
    for plugin in plugins:
      pluginClass=classLoader.findByPattern(plugin)
      if pluginClass.getType().lower()==type.lower():
        self.__plugin=pluginClass
        
  def getPlugin(self):
    return self.__plugin
  
  def executePlugin(self, parameterHelper):
    plugin=self.getPlugin()
    ExecuteThread(plugin, parameterHelper)

            

    

        