#!/usr/bin/env python

import sys
import os
import core.ConfigReader    as ConfigReader
import core.PluginManager   as PluginManager
import core.ParameterHelper as ParameterHelper
import core.NooraException  as NooraException
import core.ClassLoader     as ClassLoader
import logging.handlers
from org.noora.app.NoOraApp import NoOraApp

__revision__ = "$Revision$"
__version__  = "1.0.0-SNAPSHOT"

NOORA_DIR    = os.path.abspath(os.path.dirname(sys.argv[0]))
BASE_DIR     = os.path.abspath('.') 
PLUGIN_DIR   = NOORA_DIR+os.sep+'plugins'
sys.path.append(PLUGIN_DIR)



def getRevision(app):  
  print "noora version '" + app.getVersion() + "'"
  print "noora runtime (build " + app.getVersion()  + "_" + app.getRevision().split(":")[1].rstrip("$").strip() + ")"

def findTemplateFile(filename):
  url=BASE_DIR+os.sep+filename
  if os.path.isfile(url):
    return url
  url=NOORA_DIR+os.sep+filename
  if os.path.isfile(url):
    return url
  return None

def failOnPluginNotFound(message):
  raise NooraException.NooraException(message)


if __name__ == "__main__":

  try:
    
    logger = logging.getLogger('NoOraLogger')
    handler = logging.handlers.RotatingFileHandler('noora.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)         
    handler.doRollover()        
    logger.setLevel(logging.INFO)
    
    app = NoOraApp()
    
    parameterHelper=ParameterHelper.ParameterHelper()      
    if parameterHelper.hasParameter('-r'):
      getRevision(app)
      exit(1)
 
    config = ConfigReader.ConfigReader(findTemplateFile('project.conf'))
    
    classLoader = ClassLoader.ClassLoader()
    pluginManager = PluginManager.PluginManager()

    config.failOnConfigNotLoaded()


    parameters=parameterHelper.getParameters()

    helpPlugin = classLoader.findByPattern('static.help.HelpPlugin.HelpPlugin')
    pluginManager.registerPlugin(helpPlugin)

    plugins = config.getValue('PLUGINS')
    for plugin in plugins:
      pluginClass=classLoader.findByPattern(plugin)
      pluginManager.registerPlugin(pluginClass)

    
    if parameterHelper.hasParameter('-h'):
      helpPlugin.execute(app, parameterHelper, pluginManager.getPlugins())
      exit(1)    
            
    for plugin in pluginManager.getPlugins():
      for parameter in parameters:
        if parameter.upper() == plugin.getType():       
          plugin.execute(app,parameterHelper,pluginManager.getPlugins())
          exit(0)

    helpPlugin.execute(app, parameterHelper, pluginManager.getPlugins())
    failOnPluginNotFound('no plugin found')
    
  
  except NooraException.NooraException as e:
    print e.getMessage()
    exit(1)
  
