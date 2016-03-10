#!/usr/bin/env python
import suds

from org.noora.connector import Tripolis2Api
from org.noora.connector.Connector import Connector
from org.noora.connector.Tripolis2Api import Tripoli2ApiException
from org.noora.connector.TripolisDirectEmail import TripolisDirectEmail
from org.noora.connector.TripolisEmailFileConcatenator import TripolisEmailFileConcatenator

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
    tripolis_direct_email = TripolisDirectEmail(script, executable)
    client = properties.getPropertyValue('CLIENT')
    username = properties.getPropertyValue('USERNAME')
    password = properties.getPropertyValue('PASSWORD')
    workspace = executable.getWorkspace()
    direct_email_type = executable.getDirectEmailType()
    
    auth_info = Tripolis2Api.AuthInfo(client, username, password)

    try:
      workspace = Tripolis2Api.WorkspaceService(auth_info).getByField('name', workspace)
      for direct_email_type_api in Tripolis2Api.DirectEmailTypeService(auth_info).getByWorkspaceId(workspace.id):
	if direct_email_type == direct_email_type_api.name:
	  update = False
	  for direct_email_type_for_listing in Tripolis2Api.DirectEmailService(auth_info).getByDirectEmailTypeId(direct_email_type_api.id):
	    if direct_email_type_for_listing.name == tripolis_direct_email.getName():
	      if direct_email_type_for_listing.isArchived:
	        raise Tripoli2ApiException("Cannot update email. " + direct_email_type_for_listing.label + " is archived.")
	      update = True
	      break

	  if update:
	    Tripolis2Api.DirectEmailService(auth_info).update(direct_email_type_for_listing, tripolis_direct_email)
	  else:
	    Tripolis2Api.DirectEmailService(auth_info).create(direct_email_type_api.id, tripolis_direct_email)
    except Tripoli2ApiException as e:
      raise Tripoli2ApiException(e.message)
