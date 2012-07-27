#!/usr/bin/env python
from org.noora.io.Readable import Readable
from xml.etree.ElementTree import ElementTree

class XmlFileReader(Readable):
  def __init__(self, file=None):
    Readable.__init__(self)
    self.__file = file
    pathName = file.getPath() + file.getName()
    self.__handle = ElementTree()
    
  def read(self):
    handle = self.__handle
    file = self.__file
    stream = handle.parse(file.getPath()+file.getName())
    return stream
  
  def getFile(self):
    return self.__file
    
  def close(self):
    handle = self.__handle
    handle.close()
    

       


