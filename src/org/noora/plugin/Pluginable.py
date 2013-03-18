
from org.noora.plugin.PluginException import PluginException
from org.noora.io.NoOraError import NoOraError

class Pluginable:
  
  def __init__(self):
    pass

  def initialize(self, inputObject, outputObject):
    raise NoOraError('detail', "method not implemented")
  
  def terminate(self):
    raise NoOraError('detail', "method not implemented")

  def execute(self):
    raise NoOraError('detail', "method not implemented")
    

  # pre 1.0.0 stuff
  
  #def __init__(self, type, connectable):
  #  pass
  #def execute(self, parameters, properties):
  #  raise PluginException("method not implemented") 
    
  def setConnector(self, connector):
    raise PluginException("method not implemented")

  def getConnector(self):
    raise PluginException("method not implemented")

  def setExecutor(self, executor):
    raise PluginException("method not implemented")

  def getExecutor(self):
    raise PluginException("method not implemented")


  def getUsage(self):
    raise PluginException("method not implemented")
  
  def getDescription(self):
    raise PluginException("method not implemented")

  def setType(self, type):
    raise PluginException("method not implemented")

  def getType(self):
    raise PluginException("method not implemented")

  def getRevision(self):
    raise PluginException("method not implemented")
