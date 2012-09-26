#!/usr/bin/env python
from org.noora.connector.Connectable import Connectable
from org.noora.connector.ConnectorException import ConnectorException

__revision__ = "$Revision: $"

class Connector(Connectable):

  def __init__(self):
    Connectable.__init__(self)
    
  def execute(self, executable):
    raise ConnectorException("method not implemented")

    
