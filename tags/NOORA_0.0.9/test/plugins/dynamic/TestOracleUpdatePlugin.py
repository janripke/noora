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
import connectors.OracleConnectorStub as OracleConnectorStub

M_LF         = chr(10)

class TestBase(unittest.TestCase):
    
  def getClassLoader(self):
    classLoader=ClassLoader.ClassLoader()
    return classLoader  
  
  def getParameterHelper(self):
    parameterHelper=ParameterHelper.ParameterHelper()
    return parameterHelper
  
  def getConfigReader(self, filename):
    configReader=ConfigReader.ConfigReader(filename)
    return configReader
  
  def getProjectHelper(self, configReader):
    projectHelper=ProjectHelper.ProjectHelper(configReader)
    return projectHelper
  
  def getOracleConnectorSub(self):
    oracleConnectorStub=OracleConnectorStub.OracleConnectorStub()
    return oracleConnectorStub
  
  def setPluginClass(self,pattern):
    classLoader=self.getClassLoader()
    self.__pluginClass=classLoader.findByPattern(pattern)
    
  def getPluginClass(self):
    return self.__pluginClass      
        
    
  def setUp(self):
    self.setPluginClass("dynamic.update.UpdatePlugin.UpdatePlugin")
  
  def tearDown(self):
    pass
        
  def testNoParametersFail(self):  
    pluginClass=self.getPluginClass()
    parameterHelper=self.getParameterHelper()    
    try:
      pluginClass.execute(parameterHelper)  
    except NooraException.NooraException as e:
      self.assertEquals(e.getMessage(),"no oracle sid was given.")
            
        
  def testInvalidOracleSidFail(self):
    pluginClass=self.getPluginClass()
    parameterHelper=self.getParameterHelper()
    parameterHelper.setParameters(['-s=test'])
    configReader=self.getConfigReader('project.conf')
    lines=[]
    lines.append("ORACLE_SIDS=['orcl']")
    stream = M_LF.join(lines)
 
    configReader.loadFromStream(stream)
    pluginClass.setConfigReader(configReader)
    try:
      pluginClass.execute(parameterHelper)  
    except NooraException.NooraException as e:
      self.assertEquals(e.getMessage(),"the given oracle sid is not valid for this project.")


  def testInvalidSchemeFail(self):    
    pluginClass=self.getPluginClass()
    parameterHelper=self.getParameterHelper()
    parameterHelper.setParameters(['-s=orcl','-u=test'])
    
    configReader=self.getConfigReader('project.conf')
    lines=[]
    lines.append("ORACLE_SIDS=['orcl']")
    lines.append("SCHEMES=['apps']")
    stream = M_LF.join(lines)
    configReader.loadFromStream(stream)
    pluginClass.setConfigReader(configReader)
    try:
      pluginClass.execute(parameterHelper)  
    except NooraException.NooraException as e:
      self.assertEquals(e.getMessage(),"the given scheme is not valid for this project.")

 
  def testInvalidEnvironmentFail(self):    
    pluginClass=self.getPluginClass()
    parameterHelper=self.getParameterHelper()
    parameterHelper.setParameters(['-s=orcl','-e=uat'])
    
    configReader=self.getConfigReader('project.conf')
    lines=[]
    lines.append("ORACLE_SIDS=['orcl']")
    lines.append("SCHEMES=['apps']")
    lines.append("DEFAULT_ENVIRONMENT=['dev']")
    lines.append("ENVIRONMENTS=['dev']")
    stream = M_LF.join(lines)
    configReader.loadFromStream(stream)
    pluginClass.setConfigReader(configReader)
    try:
      pluginClass.execute(parameterHelper)  
    except NooraException.NooraException as e:
      self.assertEquals(e.getMessage(),"the given environment is not valid for this project.")
  

  def testInvalidVersionFail(self):    
    pluginClass=self.getPluginClass()
    parameterHelper=self.getParameterHelper()
    parameterHelper.setParameters(['-s=orcl','-e=dev','-v=1.0.0'])
    
    configReader=self.getConfigReader('project.conf')
    lines=[]
    lines.append("ORACLE_SIDS=['orcl']")
    lines.append("SCHEMES=['apps']")
    lines.append("DEFAULT_ENVIRONMENT=['dev']")
    lines.append("ENVIRONMENTS=['dev']")
    lines.append("ORACLE_USERS=[['orcl','apps','apps','apps']]")
    lines.append("CREATE_OBJECTS=['usr','dbl','lib','dir','scm','seq','syn','tab','cst','fct','prc','pkg','jar','vw','trg','idx','gra']")
    lines.append("EXCLUDED_FILES=['install.sql']")
    lines.append("EXCLUDED_EXTENSIONS=['bak','~','pyc','log']")
    lines.append("DEFAULT_VERSION='1.0.0'")
    stream = M_LF.join(lines)
    configReader.loadFromStream(stream)
    
    projectHelper=self.getProjectHelper(configReader)
    projectHelper.setNooraDir(NOORA_DIR)
    pluginClass.setConfigReader(configReader)
    pluginClass.setProjectHelper(projectHelper)
    pluginClass.setNooraDir(NOORA_DIR)
    
    oracleConnectorStub=self.getOracleConnectorSub()
    pluginClass.setConnector(oracleConnectorStub)
        
    try:
      pluginClass.execute(parameterHelper)  
    except NooraException.NooraException as e:
      self.assertEquals(e.getMessage(),"the given version is not valid for this project.")

       

if __name__=='__main__':
    unittest.main()