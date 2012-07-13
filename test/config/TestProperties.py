#!/usr/bin/env python

import unittest
import os
import sys

BASE_DIR = os.path.abspath('.')
NOORA_DIR = BASE_DIR.split('test')[0] + "src"

sys.path.append(NOORA_DIR)

from org.noora.io.Properties import Properties
from org.noora.io.Property import Property
from org.noora.io.File import File
from org.noora.io.FileReader import FileReader
from org.noora.io.PropertyLoader import PropertyLoader


class TestProperties(unittest.TestCase):

      
    def getFileReader(self, fileName):
        file = File(pathName=fileName)
        fileReader = FileReader(file)
        return fileReader      

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testProperties(self):
        properties = Properties()
        properties.setProperty("application.version", "1.0.0")
        self.assertEqual(properties.size(), 1, "invalid size")
        properties.clear()
        self.assertEqual(properties.size(), 0, "invalid size")
        
        
        
    def testFileReader(self):
        fileReader = self.getFileReader("test.txt")
        characterBuffer= fileReader.read()
        fileReader.close()
        
    def testPropertyLoader(self):
        properties = Properties()        
        propertyLoader = PropertyLoader(properties)
        fileReader = self.getFileReader("test.txt")
        propertyLoader.load(fileReader)
        self.assertEqual(properties.size(), 3, "invalid size")
        property = properties.getProperty("ORACLE_USERS")
        self.assertEqual(len(eval(property.getValue())), 2, "invalid size")
        


if __name__ == '__main__':
    unittest.main()
