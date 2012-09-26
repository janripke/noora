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
  
  def execute(self, executable):
    
    script = executable.getScript()
    scriptReader = FileReader(script) 
      
    properties = Properties()
    properties.setProperty('database', executable.getDatabase())     
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
    properties.setProperty(Processor.ARGUMENT, ["mysql","--host="+executable.getHost(),"--user="+executable.getUsername(),"--password="+executable.getPassword(),executable.getDatabase()])
    properties.setProperty(Processor.SHELL, False)
    mysqlCall= Call(properties)
          
    processor = Processor()
    processor.call(mysqlCall)
         
    logger = logging.getLogger('NoOraLogger')
    logger.info(executable.getScript())

      




