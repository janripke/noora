#!/usr/bin/env python
from org.noora.connector.ConnectorException import ConnectorException

__revision__ = "$Revision: $"


class Connectable:

  def __init__(self):
    pass
    
  def execute(self, executable):
    raise ConnectorException("method not implemented")

