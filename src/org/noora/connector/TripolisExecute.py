#!/usr/bin/env python
from org.noora.connector.Execute import Execute

__revision__ = "$Revision: $"

class TripolisExecute(Execute):

  def __init__(self):
    Execute.__init__(self)
    self.__workspace = None
    self.__direct_email_type = None
    self.__additional_description = None

  def getWorkspace(self):
    return self.__workspace

  def setWorkspace(self, value):
    self.__workspace = value

  def getDirectEmailType(self):
    return self.__direct_email_type

  def setDirectEmailType(self, value):
    self.__direct_email_type = value

  def getAdditionalDescription(self):
    return self.__additional_description

  def setAdditionalDescription(self, value):
    self.__additional_description = value

