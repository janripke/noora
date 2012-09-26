#!/usr/bin/env python

from org.noora.plugin.Plugin import Plugin
from org.noora.helper.PropertyHelper import PropertyHelper
from org.noora.io.File import File
from org.noora.cl.OptionFactory import OptionFactory
from org.noora.plugin.ConnectionExecutor import ConnectionExecutor
import os

class DropPlugin(Plugin):
  def __init__(self, connectable):
    Plugin.__init__(self, "DROP", connectable)

  def getDescription(self):
    return "drops database objects in oracle databases."

  def getDropDir(self, properties):
    return properties.getPropertyValue('noora.dir')+os.sep+'org'+os.sep+'noora'+os.sep+'plugin'+os.sep+'mysql'+os.sep+'drop'

  def getOptions(self, properties):
    options = Plugin.getOptions(self)
    
    options.addOption("-?", "--help", False, False,  "display help")      
    
    option = OptionFactory.newOption("-s", "--sid", True, True, "tns name of the oracle database.")
    option.setValues(properties.getPropertyValues('ORACLE_SIDS'))
    options.add(option)
    
    option = OptionFactory.newOption("-u", "--user", True, False, "user in the oracle database.")
    option.setValues(properties.getPropertyValues('SCHEMES'))
    options.add(option)
    
    option = OptionFactory.newOption("-e", "--environment", True, False, "environment descriptor of the oracle database.")
    option.setValues(properties.getPropertyValues('ENVIRONMENTS'))
    options.add(option)
    
#    options.addOption("--no-compile", True, False, "disable the compilation of database objects.")
    options.addOption("-i", "--ignore-errors", True, False, "ignore errors.")
    return options
  

  def execute(self, commandLine, properties):

    ignoreErrors = commandLine.getOptionValue('--igoore-errors', False)
    host = commandLine.getOptionValue('-s')

    defaultSchemes = properties.getPropertyValues('SCHEMES')
    schemes = commandLine.getOptionValues('-u', defaultSchemes)

    defaultEnvironment = properties.getProperty('DEFAULT_ENVIRONMENT')
    environment = commandLine.getOptionValue('-e', defaultEnvironment)

    objects = properties.getPropertyValues('DROP_OBJECTS')

    connector=self.getConnector()

    for scheme in schemes:
      print "dropping scheme '"+scheme+"' in database '" + host +"' using environment '"+environment+"'"      
      users= properties.getPropertyValues('ORACLE_USERS')
      user = PropertyHelper.getUser(users, host, scheme)
      passwd = PropertyHelper.getPasswd(users, host, scheme)      
      
      for object in objects:
        
        folder=File(self.getDropDir(properties)+os.sep+object)        
        ConnectionExecutor.execute(connector, folder, host, scheme, ignoreErrors, user, passwd)

      print "scheme '"+scheme+"' dropped."


