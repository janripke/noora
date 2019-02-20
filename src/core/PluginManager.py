#!/usr/bin/env python

class PluginManager:
  
  def __init__(self):
    self.__plugins=[]

  def registerPlugin(self,plugin):
    self.__plugins.append(plugin)

  def getPlugins(self):
    return self.__plugins
  
  def findPlugin(self, type):
    plugins=self.getPlugins()
    for plugin in plugins:
      if plugin.getType().lower()==type.lower():
        return plugin
    return None
    
