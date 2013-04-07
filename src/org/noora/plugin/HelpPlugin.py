from org.noora.cl.Builder import Builder
from org.noora.config.Config import Config
from org.noora.output.ConsoleOutput import ConsoleOutput
from org.noora.plugin.Plugin import Plugin
from org.noora.plugin.Pluginable import PER_EXIT

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
      
    return PER_EXIT
  
#---------------------------------------------------------
  def __showCmdUsage(self):
    usage = "NoOra v1.0.0 (c) 2013\nUsage: noora.py <generic-options> <plugin> <plugin-options>"
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
    result = []
    
    # remove first occurence of 'help'
    for i in range(len(plugins)):
      if plugins[i].getName() == self.__PLUGIN_NAME:
        del plugins[i]
        break
    
    config = self.getApplication().getConfig()
    for i in range(len(plugins)):
      pluginName = plugins[i].getName()
      options = plugins[i].getOptions()
      
      result.append("  plugin {0}:".format(pluginName))
      
      description = config.getProperty("plugins/plugin[@name='{0}']/description".format(pluginName))
      if description:
        result.append("    {0}\n    plugin-options:".format(description))
        
      # add command line options that are defined for this plugin
      if options.getOptions():
        descriptions = Builder.getHelpDescriptions(options.getOptions())
        for desc in descriptions:
          result.append("    {0}".format(desc))
       
    return "\n".join(result)
    