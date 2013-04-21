#!/usr/bin/env python

from org.noora.io.Directory import Directory
from org.noora.io.File import File
from org.noora.io.NoOraError import NoOraError
from org.noora.plugin.Pluginable import Pluginable
import logging

__revision__ = "$Revision: $"

class Plugin(Pluginable):
  
#---------------------------------------------------------
  def __init__(self, name, application, inputObject, outputObject, options):
    self.__name              = name
    self.__application       = application
    self.__input             = inputObject
    self.__output            = outputObject
    self.__executionPriority = 10000
    self.__options           = options
    self.__pluginConfig      = None

#---------------------------------------------------------
  def initialize(self):
    if self.__input:
      self.__input.initialize()
    if self.__output:
      self.__output.initialize()
  
#---------------------------------------------------------
  def terminate(self):
    if self.__input:
      self.__input.terminate()
    if self.__output:
      self.__output.terminate()

#---------------------------------------------------------
  def execute(self):
    raise NoOraError('detail', "method not implemented")
  
#---------------------------------------------------------
  def readConfig(self):
    workdir = Directory()
    workdir.pushDir(self.__application.getDirectory('RESOURCE_DIR'))
    
    try:
      config = self.__application.getConfig()
      configElem = config.getFirstElement("plugins/plugin[@name='{0}']/config".format(self.__name))
      if configElem is not None:
      
        configFile = configElem.text
        if File(configFile).exists():
          self.__pluginConfig = config.pushConfig(configFile)
        else:
          errmsg = "corrupt NoOra installation, {0} is missing".format(configFile)
          raise NoOraError('usermsg', errmsg).addReason('detail', "generate.xml not found")
      
    except NoOraError as e:
      raise e.addReason('plugin', self.__name)
    finally:
      workdir.popDir()

#---------------------------------------------------------
  def popConfig(self):
    if self.__pluginConfig is not None:
      config = self.__application.getConfig()
      config.popConfig()
      
#---------------------------------------------------------
  def getName(self):
    return self.__name
  
#---------------------------------------------------------
  def findOption(self, name):
    return self.__options.getOption(name)

#---------------------------------------------------------
  def getOptionValue(self,name):
    
    # assume the long name
    optionname = "--" + name;
    value = self.__options.getOption(optionname, True)
    if value:
      return value;
      
    # not found, delegate to application to find either define (-D arg) or env-var
    return self.getApplication().getOptionValue(name)
  
#---------------------------------------------------------
# accessors
#---------------------------------------------------------
  def getInput(self):
    return self.__input
  
#---------------------------------------------------------
  def setInput(self, inputObject):
    self.__input = inputObject
  
#---------------------------------------------------------
  def getOutput(self):
    return self.__output
  
#---------------------------------------------------------
  def setOutput(self, outputObject):
    self.__output = outputObject
    
#---------------------------------------------------------
  def getApplication(self):
    return self.__application
  
#---------------------------------------------------------
  def getExecutionPriority(self):
    return self.__executionPriority
  
#---------------------------------------------------------
  def setExecutionPriority(self, prio):
    self.__executionPriority = prio
    
#---------------------------------------------------------
  def getOptions(self):
    return self.__options

#---------------------------------------------------------
#---------------------------------------------------------
#---------------------------------------------------------
  
  # pre 1.0.0 stuff
  
  CREATE = "CREATE"
  logger = logging.getLogger("NoOraLogger")
  
  #def __init__(self, type, connectable):
  #  Pluginable.__init__(self, type, connectable)
  #  self.__options = Options()
  #  self.setType(type)
  #  self.setConnector(connectable)    

  def setConnector(self, connectable):
    self.__connectable=connectable

  def getConnector(self):
    return self.__connectable
  
  def setExecutor(self, executable):
    self.__executable=executable

  def getExecutor(self):
    return self.__executable

  def setType(self, type):
    self.__type = type

  def getType(self):
    return self.__type

  def getRevision(self):
    return self.__revision__

#  def getOptions(self):
#    return self.__options
  

    
