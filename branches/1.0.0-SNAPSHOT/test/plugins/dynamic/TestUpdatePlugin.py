#!/usr/bin/env python
   
import unittest
import os
import sys

BASE_DIR    = os.path.abspath('.')
NOORA_DIR   = BASE_DIR.split('test')[0]+"src"
PLUGIN_DIR   = NOORA_DIR+os.sep+'plugins'


sys.path.append(NOORA_DIR)
sys.path.append(PLUGIN_DIR)

from plugins.dynamic.update.UpdatePlugin import UpdatePlugin
from core.ParameterHelper import ParameterHelper
from core.ConfigReader import ConfigReader
from connectors.OracleConnectorStub import OracleConnectorStub
from connectors.SqlLoaderConnectorStub import SqlLoaderConnectorStub

M_LF         = chr(10)

class TestBase(unittest.TestCase):
    
  def testUpdatePass(self):
    parameterHelper = ParameterHelper()
    parameterHelper.setParameters(['-s=orcl','-e=dev','-v=1.0.1'])
    
    configReader = ConfigReader('project.conf')
    connector = OracleConnectorStub()
  
    sqlLoaderConnector = SqlLoaderConnectorStub()
    updatePlugin = UpdatePlugin()
    updatePlugin.setConfigReader(configReader)
    updatePlugin.setConnector(connector)
    updatePlugin.setSqlLoaderConnector(sqlLoaderConnector)
    
    updatePlugin.execute(parameterHelper)
    

       

if __name__=='__main__':
    unittest.main()