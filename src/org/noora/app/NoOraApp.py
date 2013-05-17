#!/usr/bin/env python

from org.noora.app.Appable import Appable
from org.noora.io.File import File
import logging
import os


class NoOraApp(Appable):
  
  logger = logging.getLogger("NoOraLogger")
  
  __revision__ = "$Revision: 229 $"
  
  def __init__(self):
    Appable.__init__(self)

  def getConfigFile(self, properties):
    currentDir = properties.getPropertyValue("current.dir")
    file = File(currentDir + os.sep + "project.conf")
    if file.exists():
      return file
    
    nooraDir = properties.getPropertyValue("noora.dir")
    file = File(nooraDir + os.sep + "project.conf")
    return file


    
