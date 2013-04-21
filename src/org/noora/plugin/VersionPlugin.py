from org.noora.cl.Options import Options
from org.noora.output.ConsoleOutput import ConsoleOutput
from org.noora.plugin.Plugin import Plugin
from org.noora.plugin.Pluginable import PER_CONTINUE

class VersionPlugin(Plugin):

  def __init__(self, name, application, inputObject, outputObject):
    Plugin.__init__(self, name, application, inputObject, outputObject, Options())
        
    # do not check required options for any plugins (they will not be executed anyway)
    Options.performRequiredOptionCheck = False
    
  def initialize(self):
    # overrule current output with console output
    self.setOutput(ConsoleOutput())
  
  def execute(self):
    msg = "version 1.0.0"
    self.getOutput().processOutput(None, msg)
    
    return PER_CONTINUE
