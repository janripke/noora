#!/usr/bin/env python
from org.noora.connector.Execute import Execute

__revision__ = "$Revision: $"

class TripolisExecute(Execute):

  def __init__(self):
    Execute.__init__(self)
    self.__workspace = None
    self.__direct_email_type = None

  def getWorkspace(self):
    return self.__workspace

  def setWorkspace(self, value):
    self.__workspace = value

  def getDirectEmailType(self):
    return self.__direct_email_type

  def setDiretEmailType(self, value):
    self.__direct_email_type = value