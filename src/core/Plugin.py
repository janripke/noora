#!/usr/bin/env python

import core.ProjectHelper as ProjectHelper
import core.ConfigReader  as ConfigReader

__revision__ = "$Revision: $"

class Plugin:

  def __init__(self):
    configReader=ConfigReader.ConfigReader('project.conf')
    self.setConfigReader(configReader)
    self.setProjectHelper(ProjectHelper.ProjectHelper(configReader))

  def setConfigReader(self, configReader):
    self.__configReader=configReader

  def setProjectHelper(self, projectHelper):
    self.__projectHelper=projectHelper

  def getConfigReader(self):
    return self.__configReader

  def getProjectHelper(self):
    return self.__projectHelper

  def getUsage(self):
    pass

  def setType(self, type):
    self.__type = type

  def getType(self):
    return self.__type

  def getRevision(self):
    return self.__revision__

  def execute(self, parameters):
    pass
