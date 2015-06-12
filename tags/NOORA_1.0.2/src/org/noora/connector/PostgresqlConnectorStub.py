#!/usr/bin/env python
from org.noora.connector.Connector import Connector

class PostgresqlConnectorStub(Connector):
  
  def __init__(self):
    Connector.__init__(self)
  
  def execute(self, executable, properties):
    pass


      




