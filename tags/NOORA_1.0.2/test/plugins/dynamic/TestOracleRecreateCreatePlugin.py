#!/usr/bin/env python
   
import unittest
import os
import sys

BASE_DIR    = os.path.abspath('.')
NOORA_DIR   = BASE_DIR.split('test')[0]+"src"
PLUGIN_DIR   = NOORA_DIR+os.sep+'plugins'


sys.path.append(NOORA_DIR)
sys.path.append(PLUGIN_DIR)
import core.ClassLoader     as ClassLoader 
import core.ParameterHelper as ParameterHelper
import core.NooraException  as NooraException
import core.ConfigReader    as ConfigReader
import core.ProjectHelper   as ProjectHelper
from core.ConfigReader import ConfigReader
from connectors.OracleConnectorStub import OracleConnectorStub
from connectors.SqlLoaderConnectorStub import SqlLoaderConnectorStub
from connectors.LoadJavaConnectorStub import LoadJavaConnectorStub

M_LF         = chr(10)

class TestBase(unittest.TestCase):
    
  def getClassLoader(self):
    classLoader=ClassLoader.ClassLoader()
    return classLoader  
  
  def getParameterHelper(self):
    parameterHelper=ParameterHelper.ParameterHelper()
    return parameterHelper
  
  def getConfigReader(self, filename):
    configReader=ConfigReader(filename)
    return configReader
  
  def getProjectHelper(self, configReader):
    projectHelper=ProjectHelper.ProjectHelper(configReader)
    return projectHelper
  
  def getOracleConnectorStub(self):
    oracleConnectorStub=OracleConnectorStub()
    return oracleConnectorStub
  
  def getSqlLoaderConnectorStub(self):
    sqlLoaderConnectorStub=SqlLoaderConnectorStub()
    return sqlLoaderConnectorStub
  
  def getLoadJavaConnectorStub(self):
    loadJavaConnectorStub = LoadJavaConnectorStub()
    return loadJavaConnectorStub
  
  def setPluginClass(self,pattern):
    classLoader=self.getClassLoader()
    self.__pluginClass=classLoader.findByPattern(pattern)
    
  def getPluginClass(self):
    return self.__pluginClass      
        
    
  def setUp(self):
    self.setPluginClass("dynamic.recreate.RecreatePlugin.RecreatePlugin")
  
  def tearDown(self):
    pass                   
        
  def testRecreateSchemaPass(self):
    recreateClass=self.getPluginClass()
    parameterHelper=self.getParameterHelper()
    parameterHelper.setParameters(['-s=orcl','-u=apps'])
    configReader=ConfigReader('project.conf')    
    
    recreateClass.setConfigReader(configReader)
    oracleConnectorStub=self.getOracleConnectorStub()
    sqlLoaderConnectorStub=self.getSqlLoaderConnectorStub()
    loadJavaConnectorStub=self.getLoadJavaConnectorStub()
    recreateClass.setConnector(oracleConnectorStub)
    recreateClass.setLoadJavaConnector(loadJavaConnectorStub)
    recreateClass.setSqlLoaderConnector(sqlLoaderConnectorStub)  
    recreateClass.execute(parameterHelper)  

  def testRecreateVersionPass(self):
    recreateClass=self.getPluginClass()
    parameterHelper=self.getParameterHelper()
    parameterHelper.setParameters(['-s=orcl','-v=1.0.0'])
    configReader=ConfigReader('project.conf')    
    
    recreateClass.setConfigReader(configReader)
    oracleConnectorStub=self.getOracleConnectorStub()
    sqlLoaderConnectorStub=self.getSqlLoaderConnectorStub()
    loadJavaConnectorStub=self.getLoadJavaConnectorStub()
    recreateClass.setConnector(oracleConnectorStub)
    recreateClass.setLoadJavaConnector(loadJavaConnectorStub)
    recreateClass.setSqlLoaderConnector(sqlLoaderConnectorStub)  
    recreateClass.execute(parameterHelper)      

if __name__=='__main__':
  unittest.main()