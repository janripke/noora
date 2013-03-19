#!/usr/bin/env python

from org.noora.io.NoOraError import NoOraError
from org.noora.plugin.Pluginable import Pluginable
import logging

__revision__ = "$Revision: $"

class Plugin(Pluginable):
  
#---------------------------------------------------------
  def __init__(self, name, application, inputObject, outputObject):
    self.__name = name
    self.__application = application
    self.__input = inputObject
    self.__output = outputObject

#---------------------------------------------------------
  def initialize(self):
    if self.__input:
      self.__input.initialize()
    if self.__output:
      self.__output.initialize()
  
#---------------------------------------------------------
  def terminate(self):
    if self.__input:
      self.__input.terminate()
    if self.__output:
      self.__output.terminate()

#---------------------------------------------------------
  def execute(self):
    raise NoOraError('detail', "method not implemented")
  
#---------------------------------------------------------
  def getName(self):
    return self.__name
  
  # accessors
#---------------------------------------------------------
  def getInput(self):
    return self.__input
  
#---------------------------------------------------------
  def setInput(self, inputObject):
    self.__input = inputObject
  
#---------------------------------------------------------
  def getOutput(self):
    return self.__output
  
#---------------------------------------------------------
  def setOutput(self, outputObject):
    self.__output = outputObject
    
#---------------------------------------------------------
  def getApplication(self):
    return self.__application
  
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
  

    
