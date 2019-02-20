#!/usr/bin/env python
import logging

from org.noora.connector.Connector import Connector
from org.noora.io.File import File
from org.noora.io.FileReader import FileReader
from org.noora.io.Properties import Properties
from org.noora.parser.Parser import Parser
from org.noora.parser.PreProcessor import PreProcessor
from org.noora.io.FileWriter import FileWriter
from org.noora.processor.StartupInfoFactory import StartupInfoFactory
from org.noora.processor.Processor import Processor
from org.noora.processor.Call import Call

class MysqlConnector(Connector):
  
  def __init__(self):
    Connector.__init__(self)
    self.__processorResult = None
    
  def setProcessorResult(self, processorResult):
    self.__processorResult = processorResult
    
  def getProcessorResult(self):
    return self.__processorResult    
  
  def execute(self, executable, properties):
    
    script = executable.getScript()
    scriptReader = FileReader(script) 
      
    cp = Properties()
    cp.setProperty('database', executable.getDatabase())
    cp.setProperty('environment', properties.getPropertyValue('environment'))    
    cp.setProperty('previous', properties.getPropertyValue('previous'))  
    parser = Parser(scriptReader,cp)      
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

    cp = Properties()
    cp.setProperty(Processor.STDERR, feedbackWriter)
    cp.setProperty(Processor.STDIN,scriptReader)
    cp.setProperty(Processor.STDOUT, feedbackWriter)
    cp.setProperty(Processor.STARTUPINFO, startupInfo)
    cp.setProperty(Processor.ARGUMENT, ["mysql","--show-warnings","--host="+executable.getHost(),"--user="+executable.getUsername(),"--password="+executable.getPassword(),executable.getDatabase()])
    cp.setProperty(Processor.SHELL, False)
    mysqlCall= Call(cp)
          
    processor = Processor()
    processorResult = processor.call(mysqlCall)
    self.setProcessorResult(processorResult)
         
    logger = logging.getLogger('NoOraLogger')
    logger.info(executable.getScript())

      




