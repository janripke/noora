#!/usr/bin/env python

from org.noora.plugin.Pluginable import Pluginable
from org.noora.cl.Options import Options
import logging

__revision__ = "$Revision$"

class Plugin(Pluginable):
  
  CREATE = "CREATE"
  logger = logging.getLogger("NoOraLogger")
  
  def __init__(self, type, connectable):
    Pluginable.__init__(self, type, connectable)
    self.__options = Options()
    self.setType(type)
    self.setConnector(connectable)    

  def setConnector(self, connectable):
    self.__connectable=connectable

  def getConnector(self):
    return self.__connectable
  
  def setExecutor(self, executable):
    self.__executable=executable

  def getExecutor(self):
    return self.__executable

  def setType(self, type):
    self.__type = type

  def getType(self):
    return self.__type

  def getRevision(self):
    return self.__revision__

  def getOptions(self):
    return self.__options
  

    
