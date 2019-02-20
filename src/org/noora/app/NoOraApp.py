#!/usr/bin/env python

from org.noora.app.Appable import Appable
from org.noora.io.File import File
import logging
import os


class NoOraApp(Appable):
  
  logger = logging.getLogger("NoOraLogger")
  
  __revision__ = "$Revision$"
  __version__  = "1.0.2"
  __name__     = "noora"
  
  def __init__(self):
    Appable.__init__(self)

  def getRevision(self):  
    return self.__revision__

  def getVersion(self):
    return self.__version__
  
  def getName(self):
    return self.__name__

  def getConfigFile(self, properties):
    currentDir = properties.getPropertyValue("current.dir")
    projectFile = properties.getPropertyValue("project.file")
    
    file = File(currentDir + os.sep + projectFile)
    if file.exists():
      return file
    
    nooraDir = properties.getPropertyValue("noora.dir")
    file = File(nooraDir + os.sep + projectFile)
    return file


    
