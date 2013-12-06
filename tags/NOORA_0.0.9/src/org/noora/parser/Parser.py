#!/usr/bin/env python
from org.noora.parser.Parsable import Parsable

class Parser(Parsable):
  def __init__(self, readable=None, properties=None):
    Parsable.__init__(self)
    self.__readable = readable
    self.__properties = properties
    
  def getReadable(self):
    return self.__readable
  
  def getProperties(self):
    return self.__properties    
  
  def parse(self):
    readable = self.getReadable()
    properties = self.getProperties()
    
    stream= readable.read()    
    for property in properties.list():
      if property.getValue():
        stream = stream.replace("{" + property.getKey() + "}",property.getValue())    
    return stream
    

