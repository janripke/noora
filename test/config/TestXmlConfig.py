#!/usr/bin/env python

import unittest
import os
import sys
from org.noora.config.XmlConfig import XmlConfig

BASE_DIR = os.path.abspath('.')
NOORA_DIR = BASE_DIR.split('test')[0] + "src"

sys.path.append(NOORA_DIR)

from org.noora.io.File import File
from org.noora.io.FileReader import FileReader
from org.noora.io.XmlFileReader import XmlFileReader

class TestXmlConfig(unittest.TestCase):
  
  def getFileReader(self, fileName):
    file = File(fileName)
    fileReader = XmlFileReader(file)
    return fileReader
  
  def setUp(self):
    pass

  def tearDown(self):
    pass
      
  def testXmlFileReader(self):
    file = File("project-config.xml")
    fileReader = XmlFileReader(file)
    tree = fileReader.read()
    fileReader.close()
    
    self.assertEqual(tree.findall("./name")[0].text,"ExampleProject","./name is invalid")
    self.assertEqual(tree.findall("name")[0].text,"ExampleProject","name is invalid")

  def testXmlConfig(self):
    file = File("project-config.xml")
    xmlConfig = XmlConfig(file)
    xmlConfig.load();
    
    self.assertEqual(xmlConfig.getProperty("name"),"ExampleProject", "'name' property not found or invalid")
    self.assertEqual(xmlConfig.getProperty("plugins/plugin[@name='generate']/class"),"dynamic.generate.GeneratePlugin.GeneratePlugin", "'plugin-class' property not found or invalid")
    
    #self.assertEqual(xmlConfig.getProperty("connectors/connect-options[@database='mysql']/options/option[6][@value]"),"<${file}","'<' not parsed properly")


if __name__ == '__main__':
    unittest.main()
