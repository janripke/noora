#!/usr/bin/env python

import core.Plugin as Plugin


class HelpPlugin(Plugin.Plugin):
  def __init__(self):
    Plugin.Plugin.__init__(self)
    self.setType("HELP")
    self.__app = None

  def getUsage(self):
    app = self.getApp()
    print "usage:",app.getName(),"command [options]"
    
  def setApp(self, app):
    self.__app = app
    
  def getApp(self):
    return self.__app

  
  def execute(self, app, parameterHelper, plugins):
    self.setApp(app)
    parameters = parameterHelper.getParameters()[2:]
    if len(parameters)!=0:
      for plugin in plugins:
        for parameter in parameters:
          if parameter.upper() == plugin.getType():
            plugin.getUsage()
            exit(1)                
    
    print app.getName() + " version '" + app.getVersion() + "'"
    self.getUsage()
    print "commands:"
    for plugin in plugins:
      print "","",plugin.getType().lower()     
    print "options:"
    print "","","-h","show this help"  
    print "","","-r","show revision"          
    
    exit(1)

  

