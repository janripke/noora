#!/usr/bin/env python
from org.noora.plugin.oracle.drop.DropPlugin import DropPlugin as OracleDropPlugin
from org.noora.plugin.mysql.drop.DropPlugin import DropPlugin as MySqlDropPlugin

class PluginFactory:
  def __init__(self):
    pass
  
  @staticmethod
  def newOracleDropPlugin(connectable):
    return OracleDropPlugin(connectable)
  
  @staticmethod
  def newMySqlDropPlugin(connectable):
    return MySqlDropPlugin(connectable)
