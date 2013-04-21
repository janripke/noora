
from org.noora.io.NoOraError import NoOraError

OF_OPTION = 0x01
OF_ARGUMENT = 0x02

OF_OPTIONARG = 0x04

OF_TYPE_MASK = 0x07
  
OF_REQUIRED = 0x08
OF_REQUIRED_MASK = 0x08
  
OF_SINGLE_ARG = 0x10
OF_MULTI_ARG = 0x20
OF_ARG_MASK = 0x30
  
OF_INVALID = 0x00
    
class Option(object):
  
  def __init__(self, shortName=None, longName=None, flags = None, description=None, argDescription=None):
    self.__shortName = shortName
    self.__longName = longName
    self.__flags = flags
    self.__values = None
    self.__valueDescription = argDescription
    self.__description = description
    
    if not flags:
      self.__flags = OF_INVALID
    else:
      self.__validateFlags(self.__flags)
      
    if not self.__shortName and not self.__longName:
      raise NoOraError('detail', "cannot create Option without either a short or long name (both are not given)")
      
#---------------------------------------------------------
      
  def getShortName(self):
    return self.__shortName
  
#---------------------------------------------------------
  def getLongName(self):
    return self.__longName
  
#---------------------------------------------------------
  def getName(self):
    return self.__shortName if self.__shortName else self.__longName
  
#---------------------------------------------------------
  def matchesName(self, name):
    if self.__shortName == name or self.__longName == name:
      return True
    return False
  
#---------------------------------------------------------
  def getTypeFlag(self):
    return self.__flags & OF_TYPE_MASK
  
#---------------------------------------------------------
  def isRequired(self):
    return self.__flags & OF_REQUIRED
  
#---------------------------------------------------------
  def getArgType(self):
    """ Get the type of the option's value.
      @return: OF_SINGLE_ARG (values contains a scalar) or OF_MULTI_ARG (values contains a list)
    """
    return self.__flgs & OF_ARG_MASK
  
#---------------------------------------------------------
  def __validateFlags(self, flags):
    if bin(self.__flags & OF_TYPE_MASK).count('1') != 1:
      raise NoOraError('detail', "invalid flags, may only contain one of OF_OPTION, OF_ARGUMENT, OF_OPTIONARG")

#---------------------------------------------------------
  def getValues(self):
    if self.__values is not None:
      if self.__flags & OF_SINGLE_ARG:
        return self.__values[0] if len(self.__values) > 0 else None
      
    return self.__values
  
#---------------------------------------------------------
  def setValues(self,values):
    # note: values is always a list
    if values is not None:
      if self.__flags & OF_SINGLE_ARG and len(values) > 1:
        NoOraError('detail', "cannot setValues(values) with OF_SINGLE_ARG and 'values' having > 1 elements")
      
    self.__values = values

#---------------------------------------------------------
  def getDescription(self):
    return self.__description
  
#---------------------------------------------------------
  def getValueDescription(self):
    return self.__valueDescription

  
#  def __init2__(self, type=None, longType=None, hasArguments=False, required=False, description=None):
#    self.__type = type
#    self.__longType = longType
#    self.__hasArguments = hasArguments
#    self.__description = description
#    self.__values = []
#    self.__required = required
#
#  def getType(self):
#    return self.__type
#  
#  def setType(self, type):
#    self.__type = type
#
#  def setLongType(self):
#    self.__longType = type
#    
#  def getLongType(self):
#    return self.__longType
#
#  def hasArguments(self):
#    return self.__hasArguments
#  
#  def hasLongType(self):
#    if self.__longType:
#      return True
#    return False  
#  
#  def hasValues(self):
#    values = self.getValues()
#    if values:
#      return True
#    return False
  

#  def getDescription(self):
#    return self.__description
#  
#  def setDescription(self, description):
#    self.__description=description
#    
#  def setValues(self, values):
#    self.__values = values
#    
#  def getValues(self):
#    return self.__values
#  
#  def getValue(self):
#    values = self.getValues()
#    return values[0]
#  
#  def setRequired(self, required):
#    self.__required = required
#    
#  def isRequired(self):
#    return self.__required


