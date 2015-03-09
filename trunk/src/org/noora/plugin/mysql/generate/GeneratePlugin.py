#!/usr/bin/env python
import os
from org.noora.plugin.Plugin import Plugin
from org.noora.io.File import File
from org.noora.io.Files import Files
from org.noora.io.Path import Path
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
from org.noora.version.VersionGuesser import VersionGuesser

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
    
    project = commandLine.getOptionValue('-pr')
    version = commandLine.getOptionValue('-v')
    
    
    configFile = File(Path.path(properties.getPropertyValue('current.dir'),properties.getPropertyValue('project.file')))
    if configFile.exists()==False:      
      #project = commandLine.getOptionValue('-pr')
      host = commandLine.getOptionValue('-h')
      database = commandLine.getOptionValue('-d')
      username = commandLine.getOptionValue('-u')
      password = commandLine.getOptionValue('-p')
      #version = commandLine.getOptionValue('-v')
      
      # create the project folder
      os.makedirs(project)
      

      #create project.conf
      templateFolder = Path.path(properties.getPropertyValue('plugin.dir'),'mysql','generate','templates')
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
    
    alterDir = Path.path(properties.getPropertyValue('current.dir'),project,'alter')
    createDir = Path.path(properties.getPropertyValue('current.dir'),project,'create')
   
      
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
    versionGuesser=VersionGuesser(properties, versions)
    nextVersion = versionGuesser.guess(version).toString()
    versionFolder = versionGuesser.toFolder(nextVersion)
    
    databases = properties.getPropertyValues('DATABASES')
    versionDatabase = properties.getPropertyValues('VERSION_DATABASE')
    defaultVersion = properties.getPropertyValues('DEFAULT_VERSION')
    environments = properties.getPropertyValues('ENVIRONMENTS')
    objects= properties.getPropertyValues('CREATE_OBJECTS')
    
    # create the version folder
    os.makedirs(versionFolder)
    
  
    for database in databases:

      # create the scheme folder
      databaseFolder=versionFolder+os.sep+database
      os.mkdir(databaseFolder)

      # create the dat folder
      datFolder=Path.path(databaseFolder,'dat')
      os.mkdir(datFolder)

      # create the version script in the dat folder
      if database==versionDatabase:
        versionFile = File(Path.path(datFolder,"version.sql"))
        versionFileWriter = FileWriter(versionFile)
        
        if nextVersion == defaultVersion:
          stream = properties.getPropertyValues('VERSION_INSERT_STATEMENT')          
        else:
          stream = properties.getPropertyValues('VERSION_UPDATE_STATEMENT')
        
        stream=stream.replace('<version>',nextVersion)               
        
        versionFileWriter.write(stream)
        versionFileWriter.close()
        
        #sqlScript=self.getSqlVersionStatement(versions, version)
        #projectHelper.writeFile(datFolder+os.sep+'version.sql', sqlScript)

      # create the environment folders in the dat folder
      for environment in environments:
        
        os.mkdir(Path.path(datFolder,environment))

        # create the environment script in the dat folder.
        if database==versionDatabase and nextVersion == defaultVersion:
          environmentFile=File(Path.path(datFolder,environment,'environment.sql'))
          environmentFileWriter = FileWriter(environmentFile)
          stream = properties.getPropertyValues('ENVIRONMENT_INSERT_STATEMENT')
          stream=stream.replace('<environment>',environment)

          environmentFileWriter.write(stream)
          environmentFileWriter.close()
          
          #sqlScript=self.getSqlEnvironmentStatement(environment)
          #projectHelper.writeFile(datFolder+os.sep+environment+os.sep+'environment.sql', sqlScript)
                

      # create the ddl folder
      ddlFolder=Path.path(databaseFolder,'ddl')
      os.mkdir(ddlFolder)

      # create the object folders in the ddl folder
      for object in objects:
        os.mkdir(Path.path(ddlFolder,object))
      
      # create the template code on create.
      if database==versionDatabase and nextVersion == defaultVersion:
        for object in objects:
          objectFolder = Path.path(templateFolder,object)
          objectFile = File(objectFolder)
          if objectFile.exists():
            files = Files.list(objectFile)
            for file in files:
              fileReader = FileReader(file)
              stream = fileReader.read()
              fileReader.close()
              
              target = File(Path.path(ddlFolder,object,file.getName()))
              targetWriter = FileWriter(target)
              targetWriter.write(stream)
              targetWriter.close()
              
    print "version "+nextVersion+" created."
    