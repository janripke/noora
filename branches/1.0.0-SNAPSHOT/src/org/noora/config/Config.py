#!/usr/bin/env python

import org.noora.io.File as File
from org.noora.config.XmlConfig import XmlConfig

class Config(object):
  def __init__(self):
    self.__configs = [];
  
  def pushConfig(self,_file):
    config = Config.createConfig(_file)
    self.__configs.append(config)
  
  def popConfig(self):
    if len(self.__configs) > 0:
      self.__configs.pop();
        
  def getProperty(self,name):
    for c in reversed(self.__configs):
      value = c.getProperty(name)
      if value != None:
        return value
    return None
  
  def setProperty(self,name, value):
    c = self.__configs[-1]
    if c != None:
      c.setProperty(name,value)
  
  @staticmethod
  def __createConfig(cls,_file):
    ext = _file.getExtension();
    if (ext == "xml"):
      return XmlConfig(_file);
    else:
      # this should return a PropertyConfig object
      return None;
  