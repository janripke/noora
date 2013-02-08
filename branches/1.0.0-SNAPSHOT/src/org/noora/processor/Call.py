#!/usr/bin/env python

from org.noora.processor.Callable import Callable
from org.noora.processor.Processor import Processor

class Call(Callable):
  
  def __init__(self, properties=None):
    Callable.__init__(self)
    self.__properties = properties

  def getProperties(self):
    return self.__properties

  def getProperty(self, key):
    properties = self.getProperties()
    return properties.getPropertyValue(key)
      
    




