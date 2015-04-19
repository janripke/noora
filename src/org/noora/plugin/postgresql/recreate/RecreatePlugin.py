#!/usr/bin/env python
from org.noora.plugin.Plugin import Plugin
from org.noora.cl.OptionFactory import OptionFactory
from org.noora.plugin.mysql.drop.DropPlugin import DropPlugin
from org.noora.plugin.mysql.create.CreatePlugin import CreatePlugin
from org.noora.plugin.mysql.update.UpdatePlugin import UpdatePlugin
from org.noora.cl.Parser import Parser
from org.noora.version.Versions import Versions
from org.noora.version.VersionLoader import VersionLoader
from org.noora.cl.Option import Option
from org.noora.cl.ArgumentBuilder import ArgumentBuilder


class RecreatePlugin(Plugin):
  
  __revision__ = "$Revision: 334 $"
  
  def __init__(self):
    Plugin.__init__(self, "RECREATE", None)
    
  def getDescription(self):
    return "recreates the database project in the given database."
  
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

    option = OptionFactory.newOption("-v", "--version", False, False, "version folder to install.")
    #option.setValues(properties.getPropertyValues('ENVIRONMENTS'))
    options.add(option)

    
#    options.addOption("--no-compile", True, False, "disable the compilation of database objects.")
    options.addOption("-i", "--ignore-errors", True, False, "ignore errors.")


    
    return options
  


  def execute(self, commandLine, properties):
        
    host = commandLine.getOption('-h')
    database = commandLine.getOption('-d')    
    environment = commandLine.getOption('-e')
    
    # drop section
    arguments = ArgumentBuilder.build(host, database, environment)
            
    dropPlugin = DropPlugin()
    options = dropPlugin.getOptions(properties)
    parser = Parser()
    dropLine = parser.parse(options, arguments)
    parser.checkRequiredOptions()
    parser.checkRequiredArguments()
    dropPlugin.execute(dropLine, properties)
    
    # create section
    createPlugin = CreatePlugin()    
    options = createPlugin.getOptions(properties)
    parser = Parser()
    createLine = parser.parse(options, arguments)
    parser.checkRequiredOptions()
    parser.checkRequiredArguments()
    createPlugin.execute(createLine, properties)
    
    
    # update section
    versions = Versions()
    versionLoader = VersionLoader(versions)
    versionLoader.load(properties)
    versions.sort()
    
    lastVersion = versions.last().toString()
    targetVersion = commandLine.getOptionValue('-v', lastVersion)
    print "targetVersion",targetVersion
    for version in versions.list()[1:]:
     
      targetOption= Option('-v',"--version", True, True, "version folder to install.")
      targetOption.setValues([version.toString()])
        
      arguments = ArgumentBuilder.build(host, database, environment, targetOption)
            
      updatePlugin = UpdatePlugin()
      options = updatePlugin.getOptions(properties)
      parser = Parser()
      updateLine = parser.parse(options, arguments)
      parser.checkRequiredOptions()
      parser.checkRequiredArguments()
      updatePlugin.execute(updateLine, properties)
      
      if version.toString()==targetVersion:
        break
    
    
    




    #arguments = ['-h=localhost','-e=dev','-v=1.0.1']
    