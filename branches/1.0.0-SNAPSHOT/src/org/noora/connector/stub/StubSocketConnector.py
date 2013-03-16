
from org.noora.connector.Connectable import Connectable

class StubSocketConnector(Connectable):

  def __init__(self):
    Connectable.__init__(self)
        
  def getConnectorType(self):
    return Connectable.CONNECTOR_TYPE_SOCKET
  
  def initialize(self):
    # normally this would set up a socket connection
    return True
  
  def terminate(self):
    # normally this would break the socket connection to the database
    return True;
  