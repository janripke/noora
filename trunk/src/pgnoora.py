#!/usr/bin/env python

import logging.handlers
import os
import sys


from org.noora.app.NoOraApp import NoOraApp
from org.noora.cl.Options import Options
from org.noora.cl.Parser import Parser
from org.noora.classloader.ClassLoader import ClassLoader
from org.noora.io.FileReader import FileReader
from org.noora.io.Files import Files
from org.noora.io.Properties import Properties
from org.noora.io.PropertyLoader import PropertyLoader

import core.ParameterHelper as ParameterHelper


__revision__ = "$Revision: 336 $"
__version__  = "1.0.0-SNAPSHOT"

NOORA_DIR    = os.path.abspath(os.path.dirname(sys.argv[0]))
CURRENT_DIR  = os.path.abspath('.') 

class PluginManager():
  
  def __init__(self, classLoadable, options):
    self.__classLoadable = classLoadable
    self.__options = options
    self.__plugins = []
    
  def setClassLoadable(self, classLoadable):
    self.__classLoadable=classLoadable
    
  def getClassLoadable(self):
    return self.__classLoadable
  
  def setOptions(self, options):
    self.__options=options
  
  def getOptions(self):
    return self.__options
  
  def getPlugins(self):
    return self.__plugins
  
  def registerPlugin(self, pluginable):
    plugins = self.getPlugins()
    plugins.append(pluginable)
    
  def registerOption(self, pluginable):
    options=self.getOptions()
    options.addOption(pluginable.getType().lower(), pluginable.getType().lower(), True, False,  "plugin")    
  
  def load(self, property):    
    plugins = eval(property.getValue())
    classLoader = self.getClassLoadable()
    for plugin in plugins:      
      pluginClass=classLoader.findByPattern(plugin)
      self.registerPlugin(pluginClass)
      self.registerOption(pluginClass)      
  
  def findByType(self, type):
    plugins=self.getPlugins()
    for plugin in plugins:
      if plugin.getType().lower()==type.lower():
        return plugin

def getRevision(app):  
  print "noora version '" + app.getVersion() + "'"
  print "noora runtime (build " + app.getVersion()  + "_" + app.getRevision().split(":")[1].rstrip("$").strip() + ")"





if __name__ == "__main__":

    properties = Properties()        
    propertyLoader = PropertyLoader(properties)        
    properties.setProperty("noora.dir", NOORA_DIR)
    properties.setProperty("current.dir", CURRENT_DIR)
    properties.setProperty("plugin.dir", NOORA_DIR + os.sep + 'org' + os.sep + 'noora' + os.sep + 'plugin')
    properties.setProperty("project.file", "pgproject.conf")
    properties.setProperty("alter.dir",properties.getPropertyValue("current.dir")+os.sep+"alter")
    properties.setProperty("create.dir",properties.getPropertyValue("current.dir")+os.sep+"create")
    
    
    app = NoOraApp()
    file = app.getConfigFile(properties)
    fileReader = FileReader(file) 
    propertyLoader.load(fileReader)
    
    
    classLoader = ClassLoader() 
    options = Options() 
    pluginManager = PluginManager(classLoader, options)
    pluginsProperty = properties.getProperty('PLUGINS')
    pluginManager.load(pluginsProperty)
    options = pluginManager.getOptions()
    
    
    #arguments = ['drop','create','update','-h=localhost','-d=orcl','-e=dev','-v=1.0.1']
    arguments = sys.argv[1:]
   
    parser = Parser()       
    commands = parser.parse(options, arguments)
    
    for command in commands.getOptions().getOptions():
      
      plugin = pluginManager.findByType(command.getType())
      
      options=plugin.getOptions(properties)
      commandLine = parser.parse(options,arguments)
      parser.checkRequiredOptions()
      parser.checkRequiredArguments()
      
      plugin.execute(commandLine, properties)
 
