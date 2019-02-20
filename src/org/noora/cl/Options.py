#!/usr/bin/env python
from org.noora.cl.OptionFactory import OptionFactory


class Options:
  
  def __init__(self):
    self.__options=[]
       
  def clear(self):
    self.__options=[]
      
  def getOptions(self):
    return self.__options
  
  def add(self, option):
    self.__options.append(option)
  
  def addOption(self, type=None, longType=None, hasArguments=False, required=False, description=None):
    option = OptionFactory.newOption(type, longType, hasArguments, required, description)
    self.__options.append(option)
    return option
    
  def hasOption(self, type):
    options = self.getOptions()
    for option in options:
      if option.getType()==type or option.getLongType()==type:
        return True
    return False      
    
  def getOption(self, type):
    options=self.getOptions()
    for option in options:
      if option.getType()==type or option.getLongType()==type:
        return option
  
  def getRequiredOptions(self):
    result = []
    options=self.getOptions()
    for option in options:
      if option.isRequired():
        result.append(option)
    return result
  
  def getRequiredArguments(self):
    result = []
    options = self.getOptions()
    for option in options:
      if option.hasValues()==False:
        result.append(option)
    return result
  
  def size(self):
    options = self.__options
    return len(options)
  


