#!/usr/bin/env python

import unittest
import os
import sys

BASE_DIR = os.path.abspath('.')
NOORA_DIR = BASE_DIR.split('test')[0] + "src"

sys.path.append(NOORA_DIR)

from org.noora.processor.Processor import Processor
from org.noora.processor.ProcessorStub import ProcessorStub
from org.noora.processor.Call import Call
from org.noora.processor.StartupInfoFactory import StartupInfoFactory
from org.noora.io.File import File
from org.noora.io.FileWriter import FileWriter
from org.noora.io.FileReader import FileReader
from org.noora.io.Properties import Properties
from org.noora.parser.Parser import Parser
from org.noora.parser.PreProcessor import PreProcessor

class TestProcessor(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testProcessor(self):
      
      script = File("show_tables.sql")
      scriptReader = FileReader(script) 
      
      properties = Properties()
      properties.setProperty('database', 'orcl')
      
      parser = Parser(scriptReader,properties)
      
      preProcessor = PreProcessor()
      stream = preProcessor.parse(parser)
      
      tmp = File("tmp.sql")
      tmpWriter = FileWriter(tmp)
      tmpWriter.write(stream)
      tmpWriter.close()
      
      scriptReader = FileReader(tmp)
      
      
      feedback = File('feedback.log')
      feedbackWriter = FileWriter(feedback) 
            
      startupInfo = StartupInfoFactory.newStartupInfo()      
      
      properties = Properties()
      properties.setProperty(Processor.STDERR, feedbackWriter)
      properties.setProperty(Processor.STDIN,scriptReader)
      properties.setProperty(Processor.STDOUT, feedbackWriter)
      properties.setProperty(Processor.STARTUPINFO, startupInfo)
      properties.setProperty(Processor.ARGUMENT, ["mysql","--host=192.168.1.13","--user=apps","--password=apps","--html","orcl"])
      properties.setProperty(Processor.SHELL, False)
      mysqlCall= Call(properties)
            
      processor = Processor()
      processor.call(mysqlCall)
      
    def testProcessorStub(self):
      
      script = File("show_routines.sql")
      scriptReader = FileReader(script) 
      
      properties = Properties()
      properties.setProperty('database', 'orcl')
      
      parser = Parser(scriptReader,properties)
      
      preProcessor = PreProcessor()
      stream = preProcessor.parse(parser)
      
      tmp = File("tmp.sql")
      tmpWriter = FileWriter(tmp)
      tmpWriter.write(stream)
      tmpWriter.close()
      
      scriptReader = FileReader(tmp)
      
      
      feedback = File('feedback.log')
      feedbackWriter = FileWriter(feedback) 
            
      startupInfo = StartupInfoFactory.newStartupInfo()      
      
      properties = Properties()
      properties.setProperty(Processor.STDERR, feedbackWriter)
      properties.setProperty(Processor.STDIN,scriptReader)
      properties.setProperty(Processor.STDOUT, feedbackWriter)
      properties.setProperty(Processor.STARTUPINFO, startupInfo)
      properties.setProperty(Processor.ARGUMENT, ["mysql","--host=192.168.1.13","--user=apps","--password=apps","-s","-r","orcl"])
      properties.setProperty(Processor.SHELL, False)
      mysqlCall= Call(properties)
            
      processor = Processor()
      processor.call(mysqlCall) 
 
      feedback = File('feedback1.log')
      feedbackWriter = FileWriter(feedback) 

      tmp = File("feedback.log")
      scriptReader = FileReader(tmp)
            
      startupInfo = StartupInfoFactory.newStartupInfo()      
      
      properties = Properties()
      properties.setProperty(Processor.STDERR, feedbackWriter)
      properties.setProperty(Processor.STDIN,scriptReader)
      properties.setProperty(Processor.STDOUT, feedbackWriter)
      properties.setProperty(Processor.STARTUPINFO, startupInfo)
      properties.setProperty(Processor.ARGUMENT, ["mysql","--host=192.168.1.13","--user=apps","--password=apps","-s","-r","orcl"])
      properties.setProperty(Processor.SHELL, False)
      mysqlCall= Call(properties)
            
      processor = Processor()
      processor.call(mysqlCall) 
     
           
       
      
      


if __name__ == '__main__':
    unittest.main()
