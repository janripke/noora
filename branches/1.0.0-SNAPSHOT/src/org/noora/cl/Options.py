#!/usr/bin/env python
from org.noora.app.Params import OptionParameter, ArgParameter
from org.noora.cl.Option import OF_OPTION, OF_OPTIONARG
from org.noora.cl.OptionFactory import OptionFactory
from org.noora.io.NoOraError import NoOraError


class Options:
  
#---------------------------------------------------------
  def __init__(self):
    self.__options=[]
       
#---------------------------------------------------------
  def clear(self):
    self.__options=[]
      
#---------------------------------------------------------
  def getOptions(self):
    return self.__options
  
#---------------------------------------------------------
  def add(self, option):
    self.__options.append(option)
    
#---------------------------------------------------------
  def setOptionValues(self, params):
    for param in params.getParams():
      for option in self.__options:
        if (isinstance(param, OptionParameter) and option.getTypeFlag() == OF_OPTION) or \
           (isinstance(param, ArgParameter) and option.getTypeFlag() == OF_OPTIONARG):
          if option.matchesName(param.getName()):
            option.setValues( [ param.getValue() ] )
            param.setUsed(True)
            
#---------------------------------------------------------
  def checkRequiredOptions(self):
    for option in self.__options:
      if option.isRequired() and len(option.getValues()) < 1:
        raise NoOraError('usermsg', "option {0} is required".format(option.getName()))
  
#---------------------------------------------------------
#---------------------------------------------------------
#---------------------------------------------------------

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
  


