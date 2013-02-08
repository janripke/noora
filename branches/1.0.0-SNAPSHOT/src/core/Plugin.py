#!/usr/bin/env python

import core.ProjectHelper         as ProjectHelper
import core.ConfigReader          as ConfigReader
import core.ParameterDefinition   as ParameterDefinition
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
    self.__parameterDefinitions=[]

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
  
  def getDescription(self):
    return ""

  def setType(self, type):
    self.__type = type

  def getType(self):
    return self.__type

  def getRevision(self):
    return self.__revision__

  def execute(self, parameters):
    pass
  
  def getParameterDefinitions(self):
    return self.__parameterDefinitions
  
  def addParameterDefinition(self, key, parameters):
    parameterDefinition=ParameterDefinition.ParameterDefinition(key,parameters)
    parameterDefinition.setKey(key)
    parameterDefinition.setParameters(parameters)
    
    parameterDefinitions=self.getParameterDefinitions()
    parameterDefinitions.append(parameterDefinition)
    
  def findParameterDefinition(self, key):
    parameterDefinitions=self.getParameterDefinitions()
    for parameterDefinition in parameterDefinitions:
      if parameterDefinition.getKey().lower()==key.lower():
        return parameterDefinition
    return None
    
