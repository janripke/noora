#!/usr/bin/env python

from org.noora.config.XmlConfig import XmlConfig
from org.noora.io.File import File
from org.noora.io.FileReader import FileReader
from org.noora.io.PropertyFileReader import PropertyFileReader
from org.noora.config.PropertyConfig import PropertyConfig

import os
import sys
import unittest



BASE_DIR = os.path.abspath('.')
NOORA_DIR = BASE_DIR.split('test')[0] + "src"

sys.path.append(NOORA_DIR)


class TestPropertyConfig(unittest.TestCase):
  
  def setUp(self):
    pass

  def tearDown(self):
    pass
      
  def testPropertyFileReader(self):

    file = File("project.conf")
    fileReader = PropertyFileReader(file)
    fileReader.read()
    fileReader.close()
    
    lines = fileReader.getLines();
    self.assertEqual(lines[1],"VERSIONS=[]", "invalid 'VERSIONS' line")
    
  def testPropertyConfig(self):
    file = File("project.conf")
    pConfig = PropertyConfig(file)
    pConfig.load();
    
    self.assertEqual(pConfig.getProperty("DEFAULT_ENVIRONMENT"),"dev", "'DEFAULT_ENVIRONMENT' property not found or invalid")
    self.assertEqual(pConfig.getProperty("CREATE_OBJECTS")[1],"dbl", "'CREATE_OBJECTS[1]' property not found or invalid")
    
if __name__ == '__main__':
    unittest.main()
