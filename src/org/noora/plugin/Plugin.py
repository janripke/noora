#!/usr/bin/env python

from org.noora.io.Directory import Directory
from org.noora.io.File import File
from org.noora.io.NoOraError import NoOraError
from org.noora.plugin.Pluginable import Pluginable
import logging

__revision__ = "$Revision: $"

class Plugin(Pluginable):
  """ Base for all plugins.
  
    The base is initialize,execute,terminate based.
  """
  
#---------------------------------------------------------
  def __init__(self, name, application, inputObject, outputObject, options):
    ## @var __name
    # @brief Plugin name
    self.__name              = name
    
    ## @var __application
    # @brief the NoOra application object that loaded this plugin
    self.__application       = application
    
    ## @var __input
    # @brief the input object used to read input data (files, from socket, etc...)
    self.__input             = inputObject
    
    ## @var __output
    # @brief the output object to write output files to
    self.__output            = outputObject
    
    ## @var __executionPriority
    # @brief the order in which this plugin will be executed (lower will run first, higher will run after this plugin)
    # defaults to 10000
    self.__executionPriority = 10000
    
    ## @var __options
    # @brief Options object that defines the command-line arguments that are relevant for this plugin.
    # These options will be set by the plugin's initialize method
    self.__options           = options
    self.__pluginConfig      = None

#---------------------------------------------------------
  def initialize(self):
    """ Initialize the input and output objects
    """
    if self.__input:
      self.__input.initialize()
    if self.__output:
      self.__output.initialize()
  
#---------------------------------------------------------
  def terminate(self):
    """ Terminate the input and output objects
    """
    if self.__input:
      self.__input.terminate()
    if self.__output:
      self.__output.terminate()

#---------------------------------------------------------
  def execute(self):
    raise NoOraError('detail', "method not implemented")
  
#---------------------------------------------------------
  def readConfig(self):
    """ Read plugin specific config file.
      If the config file does not exist, then silently ignore it (do not raise an error).
      The configuration will be pushed onto the config-stack.
    """
    
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
    """ Pop the plugin configuration from the config-stack
    """
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
    """
      Find the value of an option.
      The value may be a single value (OF_SINGLE_ARG) or a list of values (OF_MULTI_ARG)
      When option 'name' cannot be found, then ask the application for this option (stored as 'define')
    """
    
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

  

    
