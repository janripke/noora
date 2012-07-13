#!/usr/bin/env python
from org.noora.io.Property import Property
  
class Properties:

  def __init__(self):
    self.__properties = []

  def clear(self):
    self.__properties = []
    


  def containsProperty(self, key):
    result = True
    property = self.getProperty(key)
    if property == None:
      result = False
    return result
    

  def setProperty(self, key, value):
    properties = self.__properties
    if self.containsProperty(key):
      property = self.getProperty(key)
      properties.remove(property)          
    property = Property(key, value)
    properties.append(property)
    return property

  def size(self):
    properties=self.__properties
    return len(properties)
  
  def list(self):
    return self.__properties
  
  def getProperty(self, key):
    result = None
    properties = self.__properties
    for property in properties:
      if property.getKey() == key:
        result = property
    return result
       


