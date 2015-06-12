#!/usr/bin/env python

import core.Connector as Connector
import logging


from org.noora.io.File import File
from org.noora.io.FileReader import FileReader
from org.noora.io.Properties import Properties
from org.noora.parser.Parser import Parser
from org.noora.parser.PreProcessor import PreProcessor
from org.noora.io.FileWriter import FileWriter
from org.noora.processor.StartupInfoFactory import StartupInfoFactory
from org.noora.processor.Processor import Processor
from org.noora.processor.Call import Call


class MysqlConnector(Connector.Connector):
  
  def __init__(self):
    Connector.Connector.__init__(self)
  
  def execute(self, mysqlHost, mysqlDatabase, mysqlUser, mysqlPasswd, mysqlScript, paramA, paramB, ignoreErrors):
    #try:
      
      script = File(mysqlScript)
      scriptReader = FileReader(script) 
      
      properties = Properties()
      properties.setProperty('database', mysqlDatabase)     
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
      properties.setProperty(Processor.ARGUMENT, ["mysql","--host="+str(mysqlHost),"--user="+str(mysqlUser),"--password="+str(mysqlPasswd),str(mysqlDatabase)])
      properties.setProperty(Processor.SHELL, False)
      mysqlCall= Call(properties)
            
      processor = Processor()
      processor.call(mysqlCall)
           
      logger = logging.getLogger('NoOraLogger')
      logger.info(mysqlScript)
    #except:
    #  logger = logging.getLogger('NoOraLogger')      
    #  if ignoreErrors==False:
    #    message = ""
    #    for info in sys.exc_info():
    #      message = message + str(info)

    #    logger.error(message)
    #    raise NooraException.NooraException(message)
    #  logger.info(stream)
      
