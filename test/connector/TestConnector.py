#!/usr/bin/env python

import unittest
import os
import sys

BASE_DIR = os.path.abspath('.')
NOORA_DIR = BASE_DIR.split('test')[0] + "src"

sys.path.append(NOORA_DIR)

from org.noora.connector.OracleConnector import OracleConnector
from org.noora.connector.ExecuteFactory import ExecuteFactory
from org.noora.io.File import File
from org.noora.io.Properties import Properties
from org.noora.io.PropertyLoader import PropertyLoader
from org.noora.io.FileReader import FileReader


class TestConnector(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testOracleConnector(self):
      
      properties = Properties()        
      propertyLoader = PropertyLoader(properties)        
      file = File("project.conf")
      fileReader = FileReader(file) 
      propertyLoader.load(fileReader)
    
      properties.setProperty("noora.dir", NOORA_DIR)
      properties.setProperty("noora.script.dir", NOORA_DIR + os.sep + 'scripts')
      
      connector = OracleConnector()
      execute = ExecuteFactory.newOracleExecute()
      execute.setHost('orcl')
      execute.setUsername('apps')
      execute.setPassword('apps')
      file = File('application_properties.sql')
      execute.setScript(file)
      
      connector.execute(execute, properties)
 

if __name__ == '__main__':
    unittest.main()
