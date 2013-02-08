#!/usr/bin/env python

import core.ProjectHelper as ProjectHelper
import core.ConfigReader  as ConfigReader
import os
import sys

__revision__ = "$Revision: $"

class Connector:

  def __init__(self):
    configReader=ConfigReader.ConfigReader('project.conf')
    self.setConfigReader(configReader)
    self.setProjectHelper(ProjectHelper.ProjectHelper(configReader))    
    self.setNooraDir(os.path.abspath(os.path.dirname(sys.argv[0])))

  def setConfigReader(self, configReader):
    self.__configReader=configReader

  def getConfigReader(self):
    return self.__configReader
  
  def setProjectHelper(self, projectHelper):
    self.__projectHelper=projectHelper

  def getProjectHelper(self):
    return self.__projectHelper

  def setNooraDir(self, path):
    self.__nooraDir=path
    
  def getNooraDir(self):
    return self.__nooraDir
  
  def getDatabases(self):
    return []
  
  def execute(self, oracleSid, oracleUser, oraclePasswd, oracleScript, paramA, paramB):
    pass
    
