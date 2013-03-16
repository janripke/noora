#!/usr/bin/env python

class Option:
  
  OPTION_TYPE_ARGUMENT = 1
  OPTION_TYPE_OPTIONARG = 2
  OPTION_TYPE_OPTION = 3
  
  def __init__(self, type=None, longType=None, hasArguments=False, required=False, description=None):
    self.__type = type
    self.__longType = longType
    self.__hasArguments = hasArguments
    self.__description = description
    self.__values = []
    self.__required = required

  def getType(self):
    return self.__type
  
  def setType(self, type):
    self.__type = type

  def setLongType(self):
    self.__longType = type
    
  def getLongType(self):
    return self.__longType

  def hasArguments(self):
    return self.__hasArguments
  
  def hasLongType(self):
    if self.__longType:
      return True
    return False  
  
  def hasValues(self):
    values = self.getValues()
    if values:
      return True
    return False
  
  def getDescription(self):
    return self.__description
  
  def setDescription(self, description):
    self.__description=description
    
  def setValues(self, values):
    self.__values = values
    
  def getValues(self):
    return self.__values
  
  def getValue(self):
    values = self.getValues()
    return values[0]
  
  def setRequired(self, required):
    self.__required = required
    
  def isRequired(self):
    return self.__required
    

