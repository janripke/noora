#!/usr/bin/env python

import sys
import os
import core.ConfigReader    as ConfigReader
import core.PluginManager   as PluginManager
import core.ParameterHelper as ParameterHelper
import core.NooraException  as NooraException
import core.ClassLoader     as ClassLoader

__revision__ = "$Revision$"

NOORA_DIR    = os.path.abspath(os.path.dirname(sys.argv[0]))
BASE_DIR     = os.path.abspath('.')
PLUGIN_DIR   = NOORA_DIR+os.sep+'plugins'
sys.path.append(PLUGIN_DIR)



def getRevision():  
  print "NoOra revision :" + __revision__.split(":")[1].rstrip("$")

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
    parameterHelper=ParameterHelper.ParameterHelper()      
    if parameterHelper.hasParameter('-r'):
      getRevision()
      exit(1)
 
    config = ConfigReader.ConfigReader(findTemplateFile('project.conf'))
    
    classLoader = ClassLoader.ClassLoader()
    pluginManager = PluginManager.PluginManager()

    config.failOnConfigNotLoaded()


    parameters=parameterHelper.getParameters()

    plugins = config.getValue('PLUGINS')
    for plugin in plugins:
      pluginClass=classLoader.findByPattern(plugin)
      pluginManager.registerPlugin(pluginClass)
    
        
    for plugin in pluginManager.getPlugins():
      
      for parameter in parameters:
        if parameter.upper() == plugin.getType():
          plugin.execute(parameterHelper)
          exit(0)

    failOnPluginNotFound('no plugin found.')
    
  
  except NooraException.NooraException as e:
    print e.getMessage()
    exit(1)
  
