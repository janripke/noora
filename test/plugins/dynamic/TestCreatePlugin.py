#!/usr/bin/env python
   
import unittest
import os
import sys

BASE_DIR    = os.path.abspath('.')
NOORA_DIR   = BASE_DIR.split('test')[0]+"src"
PLUGIN_DIR   = NOORA_DIR+os.sep+'plugins'


sys.path.append(NOORA_DIR)
sys.path.append(PLUGIN_DIR)

from plugins.dynamic.create.CreatePlugin import CreatePlugin
from core.ParameterHelper import ParameterHelper
from core.ConfigReader import ConfigReader
from connectors.OracleConnectorStub import OracleConnectorStub
from connectors.SqlLoaderConnectorStub import SqlLoaderConnectorStub

M_LF         = chr(10)

class TestBase(unittest.TestCase):
    
  def testCreatePass(self):
    parameterHelper = ParameterHelper()
    parameterHelper.setParameters(['-s=orcl'])
    
    configReader = ConfigReader('project.conf')
    connector = OracleConnectorStub()
  
    sqlLoaderConnector = SqlLoaderConnectorStub()
    createPlugin = CreatePlugin()
    createPlugin.setConfigReader(configReader)
    createPlugin.setConnector(connector)
    createPlugin.setSqlLoaderConnector(sqlLoaderConnector)
    
    
    
    createPlugin.execute(parameterHelper)
    

       

if __name__=='__main__':
    unittest.main()