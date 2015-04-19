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

class PostgresqlConnector(Connector):
  
  def __init__(self):
    Connector.__init__(self)
    self.__processorResult = None
    
  def setProcessorResult(self, processorResult):
    self.__processorResult = processorResult
    
  def getProcessorResult(self):
    return self.__processorResult    
  
  def execute(self, executable, properties):
    
      
    cp = Properties()
    cp.setProperty('database', executable.getDatabase())
    cp.setProperty('environment', properties.getPropertyValue('environment'))    
    cp.setProperty('previous', properties.getPropertyValue('previous'))  
    
    feedback = File('feedback.log')
    feedbackWriter = FileWriter(feedback) 
    
    startupInfo = StartupInfoFactory.newStartupInfo()      
    
    cp = Properties()
    cp.setProperty(Processor.STDERR, feedbackWriter)
    cp.setProperty(Processor.STDIN, None)
    cp.setProperty(Processor.STDOUT, feedbackWriter)
    cp.setProperty(Processor.STARTUPINFO, startupInfo)
    cp.setProperty(Processor.ARGUMENT, ["psql",
                                        "--host="+executable.getHost(),
                                        "--port="+executable.getPort(),
                                        "-U", executable.getUsername(),
                                        "-w",
                                        "-d", executable.getDatabase(),
                                        "-f", executable.getScript()])
    cp.setProperty(Processor.SHELL, False)
    psqlCall= Call(cp)
          
    processor = Processor()
    processorResult = processor.call(psqlCall)
    self.setProcessorResult(processorResult)
         
    logger = logging.getLogger('NoOraLogger')
    logger.info(executable.getScript())

