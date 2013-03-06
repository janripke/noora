#!/usr/bin/env python

from org.noora.config.XmlConfig import XmlConfig
from org.noora.io.File import File

class Config(object):
  def __init__(self):
    self.__configs = [];
  
  def pushConfig(self, filepath):
    config = Config.createConfig(filepath)
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
  def __createConfig(cls, filepath):
    configfile = File(filepath)
    ext = configfile.getExtension();
    if (ext == "xml"):
      return XmlConfig(configfile);
    else:
      # this should return a PropertyConfig object
      return None;
  