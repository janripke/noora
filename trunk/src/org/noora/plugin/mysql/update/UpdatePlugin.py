#!/usr/bin/env python
import os
from org.noora.plugin.Plugin import Plugin
from org.noora.helper.PropertyHelper import PropertyHelper
from org.noora.io.File import File
from org.noora.cl.OptionFactory import OptionFactory
from org.noora.plugin.ConnectionExecutor import ConnectionExecutor
from org.noora.connector.ExecuteFactory import ExecuteFactory
from org.noora.connector.ConnectorFactory import ConnectorFactory
from org.noora.plugin.mysql.update.UnknownVersionException import UnknownVersionException
from org.noora.plugin.mysql.update.InvalidEnvironmentException import InvalidEnvironmentException
from org.noora.version.Version import Version
from org.noora.version.Versions import Versions
from org.noora.version.VersionLoader import VersionLoader

class UpdatePlugin(Plugin):
  
  __revision__ = "$Revision: 249 $"
  
  def __init__(self):
    Plugin.__init__(self, "UPDATE", ConnectorFactory.newMysqlConnector())
    
  def getDescription(self):
    return "install the given update part of a database project in the database."
  
  def getAlterDir(self):
    return os.path.abspath('.')+os.sep+'alter'

  def getOptions(self, properties):
    options = Plugin.getOptions(self)
    options.addOption("-?", "--help", False, False,  "display help")
    
    option = OptionFactory.newOption("-h", "--host", True, True, "hostname of the mysql-server.")
    option.setValues(properties.getPropertyValues('MYSQL_HOSTS'))
    options.add(option)
    
    option = OptionFactory.newOption("-d", "--database", True, False, "database in the mysql-server.")
    option.setValues(properties.getPropertyValues('DATABASES'))
    options.add(option)
    
    option = OptionFactory.newOption("-e", "--environment", True, False, "environment descriptor of the mysql-server.")
    option.setValues(properties.getPropertyValues('ENVIRONMENTS'))
    options.add(option)
    
    option = OptionFactory.newOption("-v", "--version", True, True, "version folder to install.")
    #option.setValues(properties.getPropertyValues('ENVIRONMENTS'))
    options.add(option)
    
    
    options.addOption("-i", "--ignore-errors", True, False, "ignore errors.")          
    return options
  
  def checkVersionFolder(self, version, properties):
    versionFolder = File(self.getAlterDir()+os.sep+version)
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
      raise InvalidEnvironmentException("invalid version",previous) 



  def execute(self, commandLine, properties):
    ignoreErrors = commandLine.getOptionValue('--ignore-errors', False)
   
    host = commandLine.getOptionValue('-h')  
    version = commandLine.getOptionValue('-v')
    
    defaultDatabases = properties.getPropertyValues('DATABASES')
    databases = commandLine.getOptionValues('-d', defaultDatabases)
    defaultEnvironment = properties.getPropertyValues('DEFAULT_ENVIRONMENT')
    environment = commandLine.getOptionValue('-e', defaultEnvironment)
    objects = properties.getPropertyValues('CREATE_OBJECTS')
    
    self.checkVersionFolder(version, properties)
    
    
    connector = self.getConnector()    

    for database in databases:
      print "updating database '"+database+"' on host '"+host+"' using environment '"+environment+"'"
      
      users= properties.getPropertyValues('MYSQL_USERS')
      user = PropertyHelper.getMysqlUser(users, host, database)
      passwd = PropertyHelper.getMysqlPasswd(users, host, database)

      executor = ExecuteFactory.newMysqlExecute()
      executor.setHost(host)
      executor.setDatabase(database)
      executor.setIgnoreErrors(ignoreErrors)
      executor.setPassword(passwd)
      executor.setUsername(user)        
      
      self.checkEnvironment(connector, executor, environment, properties)
      self.checkVersion( connector, executor, version, properties)
      
      for object in objects:  

        # global ddl objects
        folder=File(self.getAlterDir()+os.sep+version+os.sep+database+os.sep+'ddl'+os.sep+object)
        ConnectionExecutor.execute(connector, executor, properties, folder)

        # environment specific ddl objects
        folder=File(self.getAlterDir()+os.sep+version+os.sep+database+os.sep+'ddl'+os.sep+object+os.sep+environment)
        ConnectionExecutor.execute(connector, executor, properties, folder)

      # global dat objects
      folder=File(self.getAlterDir()+os.sep+version+os.sep+database+os.sep+'dat')
      ConnectionExecutor.execute(connector, executor, properties, folder)

      # environment specific dat objects
      folder=File(self.getAlterDir()+os.sep+version+os.sep+database+os.sep+'dat'+os.sep+environment)
      ConnectionExecutor.execute(connector, executor, properties, folder)

      print "database '"+database+"' updated."


