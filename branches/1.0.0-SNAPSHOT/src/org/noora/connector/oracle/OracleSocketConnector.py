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
import os

class OracleSocketConnector(Connector):
  
  def __init__(self):
    Connector.__init__(self)
  
  def execute(self, executable, properties):
    
    script = executable.getScript()
    
    feedback = File('feedback.log')
    feedbackWriter = FileWriter(feedback) 
    
    startupInfo = StartupInfoFactory.newStartupInfo()    
    template = properties.getPropertyValue("noora.script.dir")+os.sep+"template.sql"  
    
    cp = Properties()
    cp.setProperty(Processor.STDERR, feedbackWriter)
    cp.setProperty(Processor.STDIN,None)
    cp.setProperty(Processor.STDOUT, feedbackWriter)
    cp.setProperty(Processor.STARTUPINFO, startupInfo)
    
    cp.setProperty(Processor.ARGUMENT, ["sqlplus","-l","-s",executable.getUsername()+"/"+executable.getPassword()+'@'+executable.getHost(),"@ "+template,script.getAbsolutePath() + os.sep + script.getName()])
    cp.setProperty(Processor.SHELL, False)
    oracleCall= Call(cp)
          
    processor = Processor()
    processor.call(oracleCall)
         
    logger = logging.getLogger('NoOraLogger')
    logger.info(executable.getScript())

      




