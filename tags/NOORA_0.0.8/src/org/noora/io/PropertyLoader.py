#!/usr/bin/env python
from org.noora.io.Loadable import Loadable 


class PropertyLoader(Loadable):
  def __init__(self, properties):
    Loadable.__init__(self)
    self.__properties = properties

  def getProperties(self):
    return self.__properties
    
    
  def load(self, fileReader = None):
    properties = self.getProperties()
    
    lines = fileReader.read()
    lines = lines.split(chr(10))
    buffer=[]
    for line  in lines:
      if len(line)!=0 and line.startswith("#")==False:
        buffer.append(line)

    property = None
    for line in buffer:
      pairs=line.split("=",1)
      
      if len(pairs)==2:
        key = pairs[0]
        value  = pairs[1].strip()
        property = properties.setProperty(key, value)
      if len(pairs)==1:
        key = property.getKey()
        value = property.getValue() + pairs[0].strip()
        property = properties.setProperty(key, value)
    return properties
  

       


