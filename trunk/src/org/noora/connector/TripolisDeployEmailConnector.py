#!/usr/bin/env python

from org.noora.connector.Connector import Connector
from org.noora.connector.TripolisDirectEmail import TripolisDirectEmail
from org.noora.connector.TripolisEmailFileConcatenator import TripolisEmailFileConcatenator
from org.noora.connector.TripolisUpsertDirectEmail import TripolisUpsertDirectEmail


class TripolisDeployEmailConnector(Connector):
  
  def __init__(self):
    Connector.__init__(self)
    self.__processorResult = None
    
  def setProcessorResult(self, processorResult):
    self.__processorResult = processorResult
    
  def getProcessorResult(self):
    return self.__processorResult    
  
  def execute(self, executable, properties):

    script = TripolisEmailFileConcatenator.toPython(executable.getScript())
    tripolis_direct_email = TripolisDirectEmail(script)
    url = properties.getPropertyValue('URL')
    client = properties.getPropertyValue('CLIENT')
    username = properties.getPropertyValue('USERNAME')
    password = properties.getPropertyValue('PASSWORD')
    workspace = executable.getWorkspace()
    direct_email_type = executable.getDirectEmailType()

    TripolisUpsertDirectEmail(url, client, username, password, workspace, direct_email_type, tripolis_direct_email).upsert()
    print executable.getScript().getName()





