#!/usr/bin/env python

__revision__ = "$Revision: $"

class ParameterDefinition:

  def __init__(self, key, parameters):
    self.__key=key
    self.__parameters=parameters

  def setKey(self, key):
    self.__key=key
    
  def getKey(self):
    return self.__key
  
  def setParameters(self, parameters):
    self.__parameters
    
  def getParameters(self):
    return self.__parameters
  
  def getFirstParameter(self):
    return self.getParameters()[0]
  
  def addParameter(self, key, parameters):
    self.setKey(key)
    self.setParameters(parameters)
    
