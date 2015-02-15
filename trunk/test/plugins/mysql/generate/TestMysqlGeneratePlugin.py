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
from org.noora.plugin.mysql.generate.GeneratePlugin import GeneratePlugin
from org.noora.cl.Parser import Parser
from org.noora.connector.MysqlConnector import MysqlConnector
from org.noora.connector.ExecuteFactory import ExecuteFactory


class TestBase(unittest.TestCase): 
    
  def setUp(self):
    pass
  
  def tearDown(self):
    pass

  def testGenerateProjectPass(self):    

    properties = Properties()    
    properties.setProperty("noora.dir", NOORA_DIR)
    properties.setProperty("plugin.dir", NOORA_DIR+os.sep+"org"+os.sep+"noora"+os.sep+"plugin")
    properties.setProperty("current.dir", os.path.abspath('.'))
    properties.setProperty("alter.dir",properties.getPropertyValue("current.dir")+os.sep+"alter")
    properties.setProperty("create.dir",properties.getPropertyValue("current.dir")+os.sep+"create")
    properties.setProperty("project.file", "myproject.conf")



    #connectable=MysqlConnector()
    generatePlugin = GeneratePlugin()
    print generatePlugin.getRevision()
    options = generatePlugin.getOptions(properties)

    arguments = ['-pr=example','-h=localhost','-d=orcl','-u=apps','-p=apps','-v=1.0.0']
    parser = Parser()
    commandLine = parser.parse(options,arguments)
    parser.checkRequiredOptions()
    parser.checkRequiredArguments()
    generatePlugin.execute(commandLine, properties)
    
    
       

if __name__=='__main__':
    unittest.main()