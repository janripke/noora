#!/usr/bin/env python
   
import unittest
import os
import sys

BASE_DIR    = os.path.abspath('.')
NOORA_DIR   = BASE_DIR.split('test')[0]+"src"

sys.path.append(NOORA_DIR)

from org.noora.io.Properties import Properties
from org.noora.io.PropertyLoader import PropertyLoader
from org.noora.io.Path import Path
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

  def testGenerateCreate(self):    

    properties = Properties()    
    properties.setProperty("noora.dir", NOORA_DIR)
    properties.setProperty("plugin.dir", Path.path(NOORA_DIR,"org","noora","plugin"))
    properties.setProperty("current.dir", os.path.abspath('.'))
    properties.setProperty("alter.dir",Path.path(properties.getPropertyValue("current.dir"),"alter"))
    properties.setProperty("create.dir",Path.path(properties.getPropertyValue("current.dir"),"create"))
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

    
  def testGenerateUpdateSpecific(self):
    properties = Properties()    
    properties.setProperty("noora.dir", NOORA_DIR)
    properties.setProperty("plugin.dir", Path.path(NOORA_DIR,"org","noora","plugin"))
    properties.setProperty("current.dir", Path.path(os.path.abspath('.'),'example'))
    properties.setProperty("alter.dir",Path.path(properties.getPropertyValue("current.dir"),"alter"))
    properties.setProperty("create.dir",Path.path(properties.getPropertyValue("current.dir"),"create"))
    properties.setProperty("project.file", "myproject.conf")



    #connectable=MysqlConnector()
    generatePlugin = GeneratePlugin()
    print generatePlugin.getRevision()
    options = generatePlugin.getOptions(properties)

    arguments = ['-v=1.0.6']
    parser = Parser()
    commandLine = parser.parse(options,arguments)
    parser.checkRequiredOptions()
    parser.checkRequiredArguments()
    generatePlugin.execute(commandLine, properties)    

  def testGenerateUpdateGuess(self):
    properties = Properties()    
    properties.setProperty("noora.dir", NOORA_DIR)
    properties.setProperty("plugin.dir", Path.path(NOORA_DIR,"org","noora","plugin"))
    properties.setProperty("current.dir", Path.path(os.path.abspath('.'),'example'))
    properties.setProperty("alter.dir",Path.path(properties.getPropertyValue("current.dir"),"alter"))
    properties.setProperty("create.dir",Path.path(properties.getPropertyValue("current.dir"),"create"))
    properties.setProperty("project.file", "myproject.conf")



    #connectable=MysqlConnector()
    generatePlugin = GeneratePlugin()
    print generatePlugin.getRevision()
    options = generatePlugin.getOptions(properties)

    arguments = []
    parser = Parser()
    commandLine = parser.parse(options,arguments)
    parser.checkRequiredOptions()
    parser.checkRequiredArguments()
    generatePlugin.execute(commandLine, properties)    
       

if __name__=='__main__':
    unittest.main()