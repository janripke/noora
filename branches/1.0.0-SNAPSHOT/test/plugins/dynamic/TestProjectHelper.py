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
from core.ProjectHelper import ProjectHelper

M_LF         = chr(10)

class TestBase(unittest.TestCase):
    
  def testExtractFilePass(self):
    configReader = ConfigReader('project.conf')
    ph = ProjectHelper(configReader)
    ph.extractFile('create'+os.sep+'apps'+os.sep+'sqlldr'+os.sep+'gasregio'+os.sep+'gasregio.zip','gasregio')
    

       

if __name__=='__main__':
    unittest.main()