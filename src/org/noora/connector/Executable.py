from org.noora.connector.ConnectorException import ConnectorException

__revision__ = "$Revision: $"


class Executable(object):
  def setIgnoreErrors(self, ignoreErrors):
    raise ConnectorException("method not implemented")        

  def getIgnoreErrors(self):
    raise ConnectorException("method not implemented")        
    
  def setScript(self, script):
    raise ConnectorException("method not implemented")

  def getScript(self):
    raise ConnectorException("method not implemented")
