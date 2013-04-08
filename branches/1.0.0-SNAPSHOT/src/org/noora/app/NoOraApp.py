
from org.noora.app.Params import Params
from org.noora.classloader.ClassLoader import ClassLoader
from org.noora.classloader.ClassLoaderException import ClassLoaderException
from org.noora.config.Config import Config
from org.noora.input.FileSystemInput import FileSystemInput
from org.noora.io.Directory import Directory
from org.noora.io.File import File
from org.noora.io.NoOraError import NoOraError
from org.noora.output.ConsoleOutput import ConsoleOutput

import os
from org.noora.plugin.Pluginable import PER_EXIT



class NoOraApp(object):

#---------------------------------------------------------
  def __init__(self, params):
    self.__parameters = Params(params[1:])
    self.__directories = { 'NOORA_DIR': os.path.abspath(os.path.dirname(params[0])),
                           'PROJECT_DIR': os.path.abspath(".")
                         }
    self.__config = Config()
    self.__plugins = []

#---------------------------------------------------------
  def initialize(self):
    self.__initLog()
    self.__readConfig()
    self.__loadPlugins()
    self.__parseParameters()
    
    for plugin in self.__plugins:
      plugin.initialize()

#---------------------------------------------------------  
  def terminate(self):
    for plugin in self.__plugins:
      plugin.terminate()

#--------------------------------------------------------- 
  def run(self):
    for plugin in self.__plugins:
      if plugin.execute() == PER_EXIT:
        break
  
#---------------------------------------------------------
  def getDirectory(self,name):
    return self.__directories[name]
  
#---------------------------------------------------------
  def getPlugins(self):
    return self.__plugins
  
#---------------------------------------------------------
  def getConfig(self):
    return self.__config

#---------------------------------------------------------
# Private methods
#---------------------------------------------------------
  def __initLog(self):
    pass

#--------------------------------------------------------- 
  def __parseParameters(self):
    # 1. get generic + plugin options
    # 2. get options from params
    # 3. check required options
    # 4. check options that will not be used (not define in 1.)
    # 5. store param-options for later use (self.__options)
    
    for plugin in self.__plugins:
      try:
        options = plugin.getOptions()
        options.setOptionValues(self.__parameters)
        options.checkRequiredOptions()
      except NoOraError as e:
        raise e.addReason('plugin', plugin.getName())
        
      
#---------------------------------------------------------  
  def __readConfig(self):
    """
      reads the config file (pushes on config stack). First it attempts 'project-config.xml' and if that file does not exist it will try 'project.conf'.
      It raises a NoOraError when none of the two config files is found.

      @throws NoOraError('usermsg')
    """
    
    hasNoOraConfig = False
    
    # first read noora 'system config'
    directory = Directory()
    directory.pushDir(self.__directories['NOORA_DIR'] + "/data")

    sysconfig = "{0}/data/noora-config.xml".format(self.__directories['NOORA_DIR'])
    xmlconfig = File(sysconfig)
    if xmlconfig.exists():
      self.__config.pushConfig(sysconfig)
      hasNoOraConfig = True
    
    directory.popDir()
    
    # now read project config
    
    xmlconfig = File("project-config.xml")
    if xmlconfig.exists():
      self.__config.pushConfig("project-config.xml")
      return
    
    propconf = File("project.conf")
    if propconf.exists():
      self.__config.pushConfig("project.conf")
      return
    
    if not hasNoOraConfig:
      raise NoOraError('usermsg', 'no configuration file found in project dir (project-config.xml or project.conf)')

#---------------------------------------------------------
 
  def __loadPlugins(self):
    loader = ClassLoader()
    
    try:
      plugins = self.__parameters.getPluginParams()
      for plugin in plugins:
        pluginConfig = self.__config.getElement("plugins/plugin[@name='{0}']".format(plugin.getName()))
        if not pluginConfig or len(pluginConfig) < 1:
          raise NoOraError('usermsg', "unknown command {0}".format(plugin.getName()))
        
        className = pluginConfig[0].findtext('class')       
        if not className:
          raise NoOraError('detail', "invalid plugin config for {0}, no 'class' tag present".format(plugin.getName()))
        
        inp = self.__getDefaultInput()
        outp = self.__getDefaultOutput()
        plugin = loader.findByPattern(className, [ plugin.getName(), self, inp, outp] )
        
        execPrio = pluginConfig[0].findtext("priority")
        if execPrio:
          plugin.setExecutionPriority(execPrio)
        
        self.__plugins.append(plugin)
        
      # now sort them by priority
      self.__plugins.sort(key=lambda x: x.getExecutionPriority(), reverse=False)
        
    except ClassLoaderException as e:
      raise NoOraError('detail', e.getMessage())
      
#---------------------------------------------------------
  def getOptionsInContext(self):

    plugins = self.__parameters.getPluginParams()
    for plugin in plugins:
      options = plugin.getOptions();

#---------------------------------------------------------

  def __getDefaultInput(self):
    return FileSystemInput()
  
#---------------------------------------------------------
  def __getDefaultOutput(self):
    return ConsoleOutput()