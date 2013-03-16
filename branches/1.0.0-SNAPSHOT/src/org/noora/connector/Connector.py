#!/usr/bin/env python
from org.noora.connector.Connectable import Connectable
from org.noora.connector.ConnectorException import ConnectorException

__revision__ = "$Revision: $"

class Connector(Connectable):
  
  def __init__(self, connectorContext):
    self.__connectorContext = connectorContext
    
  def execute(self, executable, properties):
    raise ConnectorException("method not implemented")

    
