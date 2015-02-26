#!/usr/bin/env python
   
import unittest
import os
import sys


from org.noora.io.Properties import Properties
from org.noora.io.PropertyLoader import PropertyLoader
from org.noora.io.File import File
from org.noora.io.FileReader import FileReader
from org.noora.cl.Parser import Parser
from org.noora.connector.OracleConnectorStub import OracleConnectorStub
from org.noora.plugin.oracle.create.CreatePlugin import CreatePlugin
from org.noora.connector.ExecuteFactory import ExecuteFactory
from org.noora.io.Files import Files


class TestOraclePlugin(unittest.TestCase): 
    
  def setUp(self):
    pass
  
  def tearDown(self):
    pass
        

  def testCreatePluginPass(self):    
    
    NOORA_DIR   = os.path.abspath('.').split('test')[0]+"src"
    
    properties = Properties()        
    propertyLoader = PropertyLoader(properties)        
    file = File("project.conf")
    fileReader = FileReader(file) 
    propertyLoader.load(fileReader)
    
    properties.setProperty("noora.dir", NOORA_DIR)
    properties.setProperty("noora.script.dir", NOORA_DIR + os.sep + "scripts")

    connectable=OracleConnectorStub()
    createPlugin = CreatePlugin()
    options = createPlugin.getOptions(properties)
    
    arguments = ['-s=orcl','-e=dev']
    parser = Parser()
    commandLine = parser.parse(options,arguments)
    
    
    createPlugin.execute(commandLine, properties)
    
       

if __name__=='__main__':
    unittest.main()