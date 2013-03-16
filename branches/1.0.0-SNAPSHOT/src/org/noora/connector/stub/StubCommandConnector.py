
from org.noora.connector.Connectable import Connectable

class StubCommandConnector(Connectable):

  def __init__(self):
    Connectable.__init__(self)
        
  def getConnectorType(self):
    return Connectable.CONNECTOR_TYPE_SOCKET
  
  def initialize(self):
    return True
  
  def terminate(self):
    return True;
  