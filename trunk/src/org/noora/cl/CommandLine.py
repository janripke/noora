#!/usr/bin/env python

from org.noora.cl.Options import Options

class CommandLine:
  
  def __init__(self):
    self.__options=Options()
    
  def addOption(self, option):
    self.__options.add(option)    
    
  def hasOption(self, type):
    options = self.__options
    return options.hasOption(type)

  def getOption(self, type):
    options = self.getOptions()
    if options.hasOption(type):
      return options.getOption(type)

  def getOptionValues(self, type, defaultValue=None):
    options = self.getOptions()
    if options.hasOption(type):
      option = options.getOption(type)
      return option.getValues()
    return defaultValue
  
  def getOptionValue(self, type, defaultValue=None):
    options = self.getOptions()
    if options.hasOption(type):
      option = options.getOption(type)
      return option.getValue()
    return defaultValue
  
  def getRequiredArguments(self):
    options = self.getOptions()
    return options.getRequiredArguments() 
      
  def getOptions(self):
    return self.__options
  
  

