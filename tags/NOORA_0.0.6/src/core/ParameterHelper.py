#!/usr/bin/env python

import sys

class ParameterHelper:
  
  def __init__(self):
    self.__parameters=[]
    self.setParameters(sys.argv)

  def setParameters(self,parameters):
    for param in parameters:
      self.__parameters.append(param)
      
  def clearParameters(self):
      self.__parameters=[]
      
  def getParameters(self):
    return self.__parameters

  def hasParameter(self, parameter):
    for param in self.__parameters:
      if param==parameter:
        return True
    return False

  def findParameter(self, parameters,p):
    result=None
    for parameter in parameters:
      if parameter.find(p)!=-1:
        result=parameter
        break
    return result

  def getParameter(self, keyword):
    for param in self.__parameters:
      if param.find(keyword)!=-1:        
        return param
    return None

  def getParameterValue(self, keywords, defaultValue):
    result=[]
    for keyword in keywords:
      parameter=self.getParameter(keyword)
      if parameter:
        result.append(parameter.split('=')[1])

    if len(result)==0:    
      return defaultValue

    return result






