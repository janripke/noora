#!/usr/bin/env python

import unittest
import os
import sys

BASE_DIR = os.path.abspath('.')
NOORA_DIR = BASE_DIR.split('test')[0] + "src"

sys.path.append(NOORA_DIR)

from org.noora.processor.Processor import Processor
from org.noora.processor.Call import Call
from org.noora.processor.StartupInfoFactory import StartupInfoFactory
from org.noora.io.File import File
from org.noora.io.FileWriter import FileWriter
from org.noora.io.FileReader import FileReader
from org.noora.io.Properties import Properties
from org.noora.io.XmlFileReader import XmlFileReader
from org.noora.io.Property import Property
from org.noora.io.Readable import Readable
from org.noora.parser.Parser import Parser
from org.noora.parser.PreProcessor import PreProcessor

class TestPreProcessor(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testProcessor(self):
            
      script = File("drop_tables.sql")
      scriptReader = FileReader(script) 
      
      properties = Properties()
      properties.setProperty('database', 'orcl')
      
      parser = Parser(scriptReader,properties)    
      preProcessor = PreProcessor()
      stream = preProcessor.parse(parser)
      self.assertEqual(stream, 'orcl', "invalid transformation")


if __name__ == '__main__':
    unittest.main()
