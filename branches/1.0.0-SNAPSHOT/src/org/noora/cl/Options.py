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
    """ Fills those option-values that are specified by the params list.
      Each param that matches an option will get it's 'used' flag set.
      A match is found when either the shortName or the longName matches with the named param.
      
      @param params the list of params that contains values to be assigned to relevant options
    """
    for param in params.getParams():
      for option in self.__options:
        if isinstance(param, OptionParameter) and option.getTypeFlag() == OF_OPTION:
          if option.matchesName(param.getName()):
            option.setValues( [ True ] )
            param.setUsed(True)
            break
        if isinstance(param, ArgParameter) and option.getTypeFlag() == OF_OPTIONARG:
          if option.matchesName(param.getName()):
            option.setValues( [ param.getValue() ] )
            param.setUsed(True)
            break
            
#---------------------------------------------------------
  def checkRequiredOptions(self):
    for option in self.__options:
      if option.isRequired():
        if not option.getValues() or len(option.getValues()) < 1:
          raise NoOraError('usermsg', "option {0} is required".format(option.getName()))
        
#---------------------------------------------------------
  def size(self):
    return len(self.getOptions()) if self.getOptions() else 0 

#---------------------------------------------------------
  def getOption(self, name, returnValue=False):
    for option in self.getOptions():
      if option.matchesName(name):
        if returnValue == False:
          return option
        else:
          values = option.getValues()
          return values[0] if values else None
      
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
    
  def getOptionOld(self, type):
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
  

  


