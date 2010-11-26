#!/usr/bin/env python

import core.ProjectHelper as ProjectHelper
import core.ConfigReader  as ConfigReader
import connectors.OracleConnector as OracleConnector
import os
import sys

__revision__ = "$Revision: $"

class Plugin:

  def __init__(self):
    configReader=ConfigReader.ConfigReader('project.conf')
    self.setConfigReader(configReader)
    self.setProjectHelper(ProjectHelper.ProjectHelper(configReader))
    self.setConnector(OracleConnector.OracleConnector())
    self.setNooraDir(os.path.abspath(os.path.dirname(sys.argv[0])))
    self.setBaseDir(os.path.abspath('.'))

  def setNooraDir(self, path):
    self.__nooraDir=path
    
  def getNooraDir(self):
    return self.__nooraDir
  
  def setBaseDir(self, path):
    self.__baseDir=path
    
  def getBaseDir(self):
    return self.__baseDir
  
  def getScriptDir(self):
    return self.getNooraDir()+os.sep+'scripts'
  
  def getAlterDir(self):
    return self.getBaseDir()+os.sep+'alter'

  def setConfigReader(self, configReader):
    self.__configReader=configReader

  def getConfigReader(self):
    return self.__configReader
  
  def setProjectHelper(self, projectHelper):
    self.__projectHelper=projectHelper

  def getProjectHelper(self):
    return self.__projectHelper

  def setConnector(self, connector):
    self.__connector=connector

  def getConnector(self):
    return self.__connector

  def getUsage(self):
    pass

  def setType(self, type):
    self.__type = type

  def getType(self):
    return self.__type

  def getRevision(self):
    return self.__revision__

  def execute(self, parameters):
    pass
