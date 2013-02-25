#!/usr/bin/env python

from org.noora.io.Readable import Readable
from xml.etree import ElementInclude
from xml.etree.ElementTree import ElementTree

class XmlFileReader(Readable):
  def __init__(self, filename=None):
    Readable.__init__(self)
    self.__file = filename
    self.__treeroot = ElementTree()
   
  def read(self):
    handle = self.__treeroot
    handle.parse(self.__file.getPathName())
    root = handle.getroot()
    ElementInclude.include(root)
    return handle
  
  def getFile(self):
    return self.__file
    
  def getHandle(self):
    return self.__treeroot
  
  def close(self):
    pass
