#!/usr/bin/env python

from org.noora.io.NoOraError import NoOraError
from org.noora.plugin.Pluginable import Pluginable
import logging

__revision__ = "$Revision: $"

class Plugin(Pluginable):
  
  def initialize(self):
    pass
  
  def terminate(self):
    pass

  def execute(self):
    raise NoOraError('detail', "method not implemented")
  
  # pre 1.0.0 stuff
  
  CREATE = "CREATE"
  logger = logging.getLogger("NoOraLogger")
  
  #def __init__(self, type, connectable):
  #  Pluginable.__init__(self, type, connectable)
  #  self.__options = Options()
  #  self.setType(type)
  #  self.setConnector(connectable)    

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
  

    
