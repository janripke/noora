#!/usr/bin/env python

import unittest
import os
import sys

BASE_DIR = os.path.abspath('.')
NOORA_DIR = BASE_DIR.split('test')[0] + "src"

sys.path.append(NOORA_DIR)

from org.noora.io.File import File
from org.noora.io.Files import Files

class TestFile(unittest.TestCase): 
  
  NOORA_DIR   = os.path.abspath('.').split('test')[0]+"src"     

  def setUp(self):
    pass

  def tearDown(self):
    pass

      
  def testFile(self):
    file = File('project.conf')
    self.assertEquals(file.isFile(), True, "is a file expected")
    self.assertEquals(file.isDirectory(), False, "is not a directory expected")
    self.assertEquals(file.getName(), 'project.conf', "invalid name") 
    self.assertEquals(file.getPath(), '', "invalid path") 

  def testFiles(self):
    
    folder = File(NOORA_DIR + os.sep + 'org'+os.sep+'noora'+os.sep+'plugin'+os.sep+'mysql'+os.sep+'drop')
    files = Files.list(file=folder, recursive=True)
    for foundFile in files:
      print foundFile.getPath()+os.sep+foundFile.getName()


if __name__ == '__main__':
    unittest.main()
