from org.noora.plugin.Plugin import Plugin
from org.noora.output.ConsoleOutput import ConsoleOutput

class VersionPlugin(Plugin):

  def __init__(self, inputObject, outputObject):
    Plugin.__init__(self, inputObject, outputObject)
    
  def initialize(self):
    # overrule current output with console output
    self.setOutput(ConsoleOutput())
  
  def execute(self):
    msg = "version 1.0.0"
    self.getOutput().processOutput(msg)
