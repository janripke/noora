#!/usr/bin/env python
   
import unittest
import os
import sys

BASE_DIR    = os.path.abspath('.')
NOORA_DIR   = BASE_DIR.split('test')[0]+"src"

sys.path.append(NOORA_DIR)

from org.noora.io.Properties import Properties
from org.noora.io.PropertyLoader import PropertyLoader
from org.noora.io.File import File
from org.noora.io.FileReader import FileReader
from org.noora.plugin.mysql.create.CreatePlugin import CreatePlugin
from org.noora.cl.Parser import Parser
from org.noora.connector.MysqlConnectorStub import MysqlConnectorStub
from org.noora.connector.MysqlConnector import MysqlConnector
from org.noora.connector.ExecuteFactory import ExecuteFactory

class TestBase(unittest.TestCase): 
    
  def setUp(self):
    pass
  
  def tearDown(self):
    pass
        

  def testCreatePass(self):    

    properties = Properties()        
    propertyLoader = PropertyLoader(properties)        
    file = File("project.conf")
    fileReader = FileReader(file) 
    propertyLoader.load(fileReader)
    
    properties.setProperty("noora.dir", NOORA_DIR)

    connectable=MysqlConnector()
    createPlugin = CreatePlugin(connectable)
    print createPlugin.getRevision()
    options = createPlugin.getOptions(properties)

    arguments = ['-h=192.168.1.13','-e=dev']
    parser = Parser()
    commandLine = parser.parse(options,arguments)
    parser.checkRequiredOptions()
    parser.checkRequiredArguments()
    createPlugin.execute(commandLine, properties)
    
    
       

if __name__=='__main__':
    unittest.main()