#!/usr/bin/env python
import os
from org.noora.plugin.Plugin import Plugin
from org.noora.helper.PropertyHelper import PropertyHelper
from org.noora.io.File import File
from org.noora.cl.OptionFactory import OptionFactory
from org.noora.plugin.ConnectionExecutor import ConnectionExecutor
from org.noora.connector.ExecuteFactory import ExecuteFactory
from org.noora.connector.ConnectorFactory import ConnectorFactory



class CreatePlugin(Plugin):
  
  __revision__ = "$Revision: 325 $"
  
  def __init__(self):
    Plugin.__init__(self, "CREATE", ConnectorFactory.newPostgresqlConnector())
    
  def getDescription(self):
    return "executes the defined baseline scripts in the create folder."
  
  def getCreateDir(self):
    return os.path.abspath('.')+os.sep+'create'

  def getOptions(self, properties):
    options = Plugin.getOptions(self)
    options.addOption("-?", "--help", False, False,  "display help")
    
    option = OptionFactory.newOption("-h", "--host", True, True, "hostname of the postgresql-server.")
    option.setValues(properties.getPropertyValues('POSTGRESQL_HOSTS'))
    options.add(option)

    option = OptionFactory.newOption("-p", "--port", True, True, "port number of the postgresql database.")
    option.setValues(properties.getPropertyValues('POSTGRESQL_HOSTS'))
    options.add(option)
    
    option = OptionFactory.newOption("-d", "--database", True, False, "database in the postgresql-server.")
    option.setValues(properties.getPropertyValues('DATABASES'))
    options.add(option)
    
    option = OptionFactory.newOption("-e", "--environment", True, False, "environment descriptor of the postgresql-server.")
    option.setValues(properties.getPropertyValues('ENVIRONMENTS'))
    options.add(option)
    
    options.addOption("-i", "--ignore-errors", True, False, "ignore errors.")          
    return options

  def execute(self, commandLine, properties):
    ignoreErrors = commandLine.getOptionValue('--ignore-errors', False)
   
    host = commandLine.getOptionValue('-h')  
    port = commandLine.getOptionValue('-p')  
    defaultDatabases = properties.getPropertyValues('DATABASES')
    databases = commandLine.getOptionValues('-d', defaultDatabases)
    defaultEnvironment = properties.getPropertyValues('DEFAULT_ENVIRONMENT')
    environment = commandLine.getOptionValue('-e', defaultEnvironment)
    objects = properties.getPropertyValues('CREATE_OBJECTS')
    
    connector = self.getConnector()    

    for database in databases:
      print "creating database '"+database+"' on host '"+host+":"+port+"' using environment '"+environment+"'"
      
      users= properties.getPropertyValues('POSTGRESQL_USERS')
      user = PropertyHelper.getPostgresqlUser(users, host, port, database)
      # password is fetched from ~/.pgpass by the psql executable itself
      #passwd = PropertyHelper.getPostgresqlPasswd(users, host, database)

      executor = ExecuteFactory.newPostgresqlExecute()
      executor.setHost(host)
      executor.setPort(port)
      executor.setDatabase(database)
      executor.setIgnoreErrors(ignoreErrors)
      executor.setPassword(passwd)
      executor.setUsername(user)        
      
      for object in objects:  

        # global ddl objects
        folder=File(self.getCreateDir()+os.sep+database+os.sep+'ddl'+os.sep+object)
        ConnectionExecutor.execute(connector, executor, properties, folder)

        # environment specific ddl objects
        folder=File(self.getCreateDir()+os.sep+database+os.sep+'ddl'+os.sep+object+os.sep+environment)
        ConnectionExecutor.execute(connector, executor, properties, folder)

      # global dat objects
      folder=File(self.getCreateDir()+os.sep+database+os.sep+'dat')
      ConnectionExecutor.execute(connector, executor, properties, folder)

      # environment specific dat objects
      folder=File(self.getCreateDir()+os.sep+database+os.sep+'dat'+os.sep+environment)
      ConnectionExecutor.execute(connector, executor, properties, folder)

      print "database '"+database+"' created."


