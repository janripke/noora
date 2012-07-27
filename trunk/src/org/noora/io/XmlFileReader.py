#!/usr/bin/env python
from org.noora.io.Readable import Readable
from xml.etree.ElementTree import ElementTree

class XmlFileReader(Readable):
  def __init__(self, file=None):
    Readable.__init__(self)
    self.__file = file
    pathName = file.getPath() + file.getName()
    self.__handle = open(pathName,'rb')
    
  def read(self):
    handle = self.__handle
    stream = ElementTree()
    stream.
    stream = handle.read()
    stream = stream.replace(chr(13)+chr(10),chr(10))
    stream = stream.replace(chr(13),chr(10)) 
    return stream
  
  def getFile(self):
    return self.__file
    
  def close(self):
    handle = self.__handle
    handle.close()
    

       


