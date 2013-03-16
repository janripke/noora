
import os

from org.noora.config.Config import Config
from org.noora.io.File import File
from org.noora.io.NoOraError import NoOraError
from org.noora.app.Params import Params
from org.noora.classloader.ClassLoader import ClassLoader
from org.noora.classloader.ClassLoaderException import ClassLoaderException

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

#---------------------------------------------------------  
  def terminate(self):
    pass

#--------------------------------------------------------- 
  def run(self):
    pass
  
#---------------------------------------------------------
  def getDirectory(self,name):
    return self.__directories[name]

#---------------------------------------------------------
  def __initLog(self):
    pass

#--------------------------------------------------------- 
  def __parseParameters(self):
    pass

#---------------------------------------------------------  
  def __readConfig(self):
    """
      reads the config file (pushes on config stack). First it attempts 'project-config.xml' and if that file does not exist it will try 'project.conf'.
      It raises a NoOraError when none of the two config files is found.

      @throws NoOraError('usermsg')
    """
    
    # first read noora 'system config'
    curdir = os.getcwd()
    os.chdir(self.__directories['NOORA_DIR'] + "/data")
    sysconfig = "{0}/data/noora-config.xml".format(self.__directories['NOORA_DIR'])
    xmlconfig = File(sysconfig)
    if xmlconfig.exists():
      self.__config.pushConfig(sysconfig)
    os.chdir(curdir)
    
    xmlconfig = File("project-config.xml")
    if xmlconfig.exists():
      self.__config.pushConfig("project-config.xml")
      return
    
    propconf = File("project.conf")
    if propconf.exists():
      self.__config.pushConfig("project.conf")
      return
    
    raise NoOraError('usermsg', 'no configuration file found in project dir (project-config.xml or project.conf)')

#---------------------------------------------------------

  def __loadPlugins(self):
    loader = ClassLoader()
    
    try:
      plugins = self.__parameters.getPluginParams()
      for plugin in plugins:
        className = self.__config.getProperty("plugins/plugin[@name='{0}']/class".format(plugin.getName()))
        if not className:
          raise NoOraError('usermsg', "unknown command {0}".format(plugin.getName()))
        self.__plugins.append(loader.findByPattern(className))
        
    except ClassLoaderException as e:
      raise NoOraError('detail', e.getMessage())
      