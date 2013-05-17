#!/usr/bin/env python
from org.noora.connector.Connector import Connector

class MysqlConnectorStub(Connector):
  
  def __init__(self):
    Connector.__init__(self)
  
  def execute(self, executable, properties):
    pass


      




