#!/usr/bin/env python
import os
from org.noora.plugin.Plugin import Plugin
from org.noora.helper.PropertyHelper import PropertyHelper
from org.noora.io.File import File
from org.noora.io.Path import Path
from org.noora.plugin.ConnectionExecutor import ConnectionExecutor
from org.noora.connector.ExecuteFactory import ExecuteFactory
from org.noora.plugin.mysql.update.UnknownVersionException import UnknownVersionException
from org.noora.plugin.mysql.update.InvalidEnvironmentException import InvalidEnvironmentException
from org.noora.plugin.mysql.update.InvalidVersionException import InvalidVersionException
from org.noora.version.Version import Version
from org.noora.version.Versions import Versions
from org.noora.version.VersionLoader import VersionLoader
from core.Property import FileReader
from org.noora.io.FileWriter import FileWriter
from org.noora.io.Properties import Properties
from org.noora.io.PropertyLoader import PropertyLoader

class GeneratePlugin(Plugin):
  
  __revision__ = "$Revision$"
  
  def __init__(self):
    Plugin.__init__(self, "GENERATE", None)
    
  def getDescription(self):
    return "initiates a new database project, or a new release of an existing database project."
  
  def getOptions(self, properties):
        
    options = Plugin.getOptions(self)
    options.addOption("-?", "--help", False, False,  "display help")
    
    options.addOption("-pr", "--project", False, False, "name of the database project.")
    options.addOption("-h", "--host", False, False, "hostname of the mysql-server.")
    options.addOption("-d", "--database", False, False,  "database in the mysql-server.")
    options.addOption("-u", "--username", False, False,  "username in the mysql-server.")
    options.addOption("-p", "--password", False, False,  "password in the mysql-server.")
    options.addOption("-v", "--version", False, False,  "version of the database project.")
    
    return options
  
  def checkVersionFolder(self, version, properties):
    alterDir = properties.getPropertyValue('alter.dir')
    versionFolder = File(alterDir+os.sep+version)
    if versionFolder.notExists():
      raise UnknownVersionException("unknown version folder", version)

  def checkEnvironment(self, connector, executor, environment, properties):
    pluginFolder = properties.getPropertyValue('plugin.dir')
    properties.setProperty('environment',environment)
    script = File(pluginFolder+os.sep+'mysql'+os.sep+'update'+os.sep+'checkenvironment.sql')
    executor.setScript(script)      
    connector.execute(executor, properties)
    if "(Code 1329)" in connector.getProcessorResult().getResult():
      raise InvalidEnvironmentException("invalid environment",environment) 

  def checkVersion(self, connector, executor, version, properties):
    pluginFolder = properties.getPropertyValue('plugin.dir')
    
    versions = Versions()
    versionLoader = VersionLoader(versions)
    versionLoader.load(properties)
    versions.sort()
    #versions.sort()
    #print "versions",versions.getVersions()
    v = Version(version)
    previous = versions.previous(v).getValue()
    
    
    properties.setProperty('previous',previous)
    script = File(pluginFolder+os.sep+'mysql'+os.sep+'update'+os.sep+'checkversion.sql')
    executor.setScript(script)      
    connector.execute(executor, properties)
    if "(Code 1329)" in connector.getProcessorResult().getResult():
      raise InvalidVersionException("invalid version",previous) 



  def execute(self, commandLine, properties):
    
    configFile = File(Path.path(properties.getPropertyValue('current.dir'),properties.getPropertyValue('project.file')))
    if configFile.exists()==False:      
      project = commandLine.getOptionValue('-pr')
      host = commandLine.getOptionValue('-h')
      database = commandLine.getOptionValue('-d')
      username = commandLine.getOptionValue('-u')
      password = commandLine.getOptionValue('-p')
      version = commandLine.getOptionValue('-v')
      
      # create the project folder
      os.makedirs(project)
      

      #create project.conf
      templateFile = File(Path.path(properties.getPropertyValue('plugin.dir'),'mysql','generate','templates',properties.getPropertyValue('project.file')))
      reader = FileReader(templateFile)
      stream = reader.read()
      stream=stream.replace('{host}',host)
      stream=stream.replace('{database}',database)
      stream=stream.replace('{username}',username)
      stream=stream.replace('{password}',password)
      stream=stream.replace('{version}',version)
      
      configFile = File(Path.path(properties.getPropertyValue('current.dir'),project,properties.getPropertyValue('project.file')))      
      writer = FileWriter(configFile)
      writer.write(stream)
      writer.close()
    
    alterDir = properties.getPropertyValue('alter.dir')
    createDir = properties.getPropertyValue('create.dir')
    
      
    # load project.conf
    properties = Properties()        
    propertyLoader = PropertyLoader(properties)    
    fileReader = FileReader(configFile) 
    propertyLoader.load(fileReader)
    
    properties.setProperty("alter.dir",alterDir)  
    properties.setProperty("create.dir",createDir)
    
    
    # resolve the version folder
    # create the version folder
    
    
    versions = Versions()
    versionLoader = VersionLoader(versions)
    versionLoader.load(properties)
    versions.sort()  
    #print versions.list()
    
      