#!/usr/bin/env python

from org.noora.io.NoOraError import NoOraError
from org.noora.io.Readable import Readable
from xml.etree import ElementInclude
from xml.etree.ElementTree import ElementTree

class XmlFileReader(Readable):
  
#---------------------------------------------------------
  def __init__(self, file):
    """
      Initializes specified xml File
      @param aFile File object
      @throws NoOraError(parameter) invalid parameter 'file'
    """
    if file == None:
      raise NoOraError("parameter", "file").addReason('detail', "invalid parameter")
    
    Readable.__init__(self)
    self.__file = file
    self.__treeroot = ElementTree()
   
#---------------------------------------------------------
  def read(self):
    """
      Reads and parses the contained xml file.
      Note that any include statements in the xml file are processed here as well
      @return tree root of built DOM
    """
    
    try:
      handle = self.__treeroot
      handle.parse(self.__file.getPathName())
      root = handle.getroot()
      ElementInclude.include(root)
      return handle
    except Exception as e:
      raise NoOraError('detail', "Error parsing xml file {0} or one of its included files".format(self.getFile().getPathName())).addReason('parse-error', e)
  
#---------------------------------------------------------
  def getFile(self):
    return self.__file
    
#---------------------------------------------------------
  def getHandle(self):
    return self.__treeroot
  
#---------------------------------------------------------
  def close(self):
    pass
