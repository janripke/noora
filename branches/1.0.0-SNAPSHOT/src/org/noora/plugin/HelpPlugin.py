from org.noora.app.NoOraApp import NoOraApp
from org.noora.config.Config import Config
from org.noora.io.NoOraError import NoOraError
from org.noora.output.ConsoleOutput import ConsoleOutput
from org.noora.plugin.Plugin import Plugin
from xml.etree.ElementTree import Element

class HelpPlugin(Plugin):
  
  __PLUGIN_NAME = "help"

#---------------------------------------------------------
  def __init__(self, name, application, inputObject, outputObject):
    Plugin.__init__(self, name, application, inputObject, outputObject)
    
#---------------------------------------------------------
  def initialize(self):
    # overrule current output with console output
    self.setOutput(ConsoleOutput())
  
#---------------------------------------------------------
  def execute(self):
    output = self.getOutput()
    
    output.processOutput(None, self.__showCmdUsage())
    
    plugins = self.getApplication().getPlugins();
    if len(plugins) == 1:
      output.processOutput(None, self.__showAvailablePlugins())
    else:
      output.processOutput(None, self.__showPluginHelp(plugins))

#---------------------------------------------------------
  def __showCmdUsage(self):
    usage = "Usage: noora.py <plugin> <plugin-options> <generic-options>"
    return usage

#---------------------------------------------------------
  def __showAvailablePlugins(self):
    names = []
    
    config = self.getApplication().getConfig()
    plugins = config.getElement("plugins/plugin", Config.GET_MODE_MERGE)
    for plugin in plugins:
      names.append(plugin.get('name'))
    return "Available plugins: \n  " + "\n  ".join(sorted(names))
    
#---------------------------------------------------------
  def __showPluginHelp(self, plugins):
    # remove first occurence of 'help'
    try:
      plugins.remove('help')
    except ValueError:
      raise NoOraError('detail', "plugin 'help' not found in pluginlist (by commandline arguments)")
    
    return ""