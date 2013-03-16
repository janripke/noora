#!/usr/bin/env python
from org.noora.connector.ConnectorException import ConnectorException

__revision__ = "$Revision: $"


class Connectable:
  
  CONNECTOR_TYPE_CMD    = 1;
  CONNECTOR_TYPE_SOCKET = 2;

  def __init__(self):
    raise ConnectorException("cannot create instance of Connectable interface")
  
  def getConnectorType(self):
    """
      Returns the connector type. Possible values:
      CONNECTOR_TYPE_CMD - connection to database is based on invokation of a command (executable).
      CONNECTOR_TYPE_SOCKET - connection to database is based on direct communication over a socket.
    """
    raise ConnectorException("method not implemented")
  
  def initialize(self):
    """
    Initializes the connection. Usually SOCKET type connectors make a connection to the database here.
    CMD type connectors normally do nothing here.
    """
    return True;
  
  def terminate(self):
    """
    Terminates the connection. Usually SOCKET type connectors disconnect from the database here.
    CMD type connectors normally do nothing here.
    """
    return True;
        
  def execute(self, executable, connectorContext = None):
    raise ConnectorException("method not implemented")

