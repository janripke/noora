#!/usr/bin/env python

from org.noora.plugin.Plugin import Plugin
from org.noora.helper.PropertyHelper import PropertyHelper
from org.noora.io.File import File
from org.noora.cl.OptionFactory import OptionFactory
from org.noora.plugin.ConnectionExecutor import ConnectionExecutor
from org.noora.connector.ExecuteFactory import ExecuteFactory
from org.noora.connector.ConnectorFactory import ConnectorFactory
from org.noora.plugin.mysql.drop.BlockedHostException import BlockedHostException
import os

class DropPlugin(Plugin):
  
  __revision__ = "$Revision$"
  
  def __init__(self):    
    Plugin.__init__(self, "DROP", ConnectorFactory.newMysqlConnector())
    
    #self.addParameterDefinition('database',['-s','-si','--sid'])
    #self.addParameterDefinition('scheme',['-u','-sc','--scheme'])

  def getDescription(self):
    return "drops database objects in mysql-servers."


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
    
#    options.addOption("--no-compile", True, False, "disable the compilation of database objects.")
    options.addOption("-i", "--ignore-errors", True, False, "ignore errors.")
    return options


  def getDropDir(self, properties):
    #print "noora.dir", os.path.abspath(os.path.dirname(sys.argv[0]))
    return properties.getPropertyValue('noora.dir')+os.sep+'org'+os.sep+'noora'+os.sep+'plugin'+os.sep+'mysql'+os.sep+'drop'
    #return self.getNooraDir()+os.sep+'plugins'+os.sep+'static'+os.sep+'drop'

  def checkBlockedHosts(self, host, properties):
    blockedHosts = properties.getPropertyValues('BLOCKED_HOSTS')
    if host in blockedHosts:
      raise BlockedHostException("blocked host", host)

  def execute(self, commandLine, properties):
    #if parameterHelper.hasParameter('-h'):
    #  self.getUsage()
    #  exit(1)

    ignoreErrors = commandLine.getOptionValue('--ignore-errors', False)

    host = commandLine.getOptionValue('-h')  
    self.checkBlockedHosts(host, properties)

    defaultDatabases = properties.getPropertyValues('DATABASES')
    databases = commandLine.getOptionValues('-d', defaultDatabases)

    defaultEnvironment = properties.getProperty('DEFAULT_ENVIRONMENT')
    environment = commandLine.getOptionValue('-e', defaultEnvironment)

    objects = properties.getPropertyValues('DROP_OBJECTS')


    for database in databases:
      print "dropping database '"+database+"' on host '"+host+"' using environment '"+environment+"'"
      
      users= properties.getPropertyValues('MYSQL_USERS')
      user = PropertyHelper.getUser(users, host, database)
      passwd = PropertyHelper.getPasswd(users, host, database)
      
      connector = self.getConnector()
           
      executor = ExecuteFactory.newMysqlExecute()
      executor.setHost(host)
      executor.setDatabase(database)
      executor.setIgnoreErrors(ignoreErrors)
      executor.setPassword(passwd)
      executor.setUsername(user)      

      for object in objects:      
        folder=File(self.getDropDir(properties)+os.sep+object)
        
        ConnectionExecutor.execute(connector, executor, properties, folder)
      
      print "database '"+database+"' dropped."    



