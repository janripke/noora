#!/usr/bin/env python
from org.noora.plugin.PluginException import PluginException
__revision__ = "$Revision: $"

class Pluginable:

  def __init__(self, type, connectable):
    pass
  
  def execute(self, parameters, properties):
    raise PluginException("method not implemented") 
    
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
