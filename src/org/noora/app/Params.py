from org.noora.io.NoOraError import NoOraError

#=========================================================

class Parameter(object):

#---------------------------------------------------------
  def __init__(self):
    self.__used = False

#---------------------------------------------------------
  def getName(self):
    pass

#---------------------------------------------------------
  def getValue(self):
    pass
  
  def isUsed(self):
    return self.__used
  
  def setUsed(self, used):
    self.__used = used

#=========================================================

class PluginParameter(Parameter):

  def __init__(self, pluginName):
    Parameter.__init__(self);
    self.__pluginName = pluginName      
  
#---------------------------------------------------------
  def getName(self):
    return self.__pluginName

#---------------------------------------------------------
  def getValue(self):
    return None

#=========================================================

class OptionParameter(Parameter):

  def __init__(self, optionName):
    Parameter.__init__(self)
    self.__option = optionName
  
#---------------------------------------------------------
  def getName(self):
    return self.__option;

#---------------------------------------------------------
  def getValue(self):
    return None

#=========================================================

class ArgParameter(Parameter):

  def __init__(self, switch, argument):
    Parameter.__init__(self)
    self.__switch = switch
    self.__argument = argument
    
#---------------------------------------------------------
  def getName(self):
    return self.__switch

#---------------------------------------------------------
  def getValue(self):
    return self.__argument

#=========================================================

class Params(object):
  
  def __init__(self, params):
    """
      Initialize and preprocess a list of arguments.
      Single arguments are stored as PluginParameter (help, recreate, etc).
      arguments in the form of '-v' are stored as OptionParameter.
      arguments in the form '-e dev' or '-e=dev' are stored as ArgParameter
      @param params a list of parameters (as strings, such as sys.argv)
      @throws NoOraError Thrown when a parameter like -option=arg is malformed
    """
    self.__params = []
    self.__preprocess(params)
    
#---------------------------------------------------------
  def getParams(self):
    return self.__params
  
#---------------------------------------------------------
  def __preprocess(self, params):
    size = len(params)
    i = 0;
    
    while (i < size):
      param = params[i].strip()
      
      if (param[0] == "-"):
        decomp = param.split("=")
        count = len(decomp)
        if (count == 2):
          # -option=value
          self.__params.append(ArgParameter(decomp[0],decomp[1]))
        elif (count > 2):
          raise NoOraError('usermsg', "invalid argument {0} (-option=arg expected".format(param))
        else:
          # -option or -option arg
          if (i + 1 < size):
            if (params[i+1][0] != "-"):
              # -option arg
              i += 1
              self.__params.append(ArgParameter(param, params[i]))
            else:
              self.__params.append(OptionParameter(param))
          else:
            self.__params.append(OptionParameter(param))
      else:
        # plugin param
        self.__params.append(PluginParameter(param))   
      i += 1
      
#---------------------------------------------------------
  def getPluginParams(self):
    return self.__getTypedParam(PluginParameter)
        
#---------------------------------------------------------
  def getOptionParams(self):
    return self.__getTypedParam(OptionParameter)
  
#---------------------------------------------------------
  def getArgParams(self):
    return self.__getTypedParam(ArgParameter)
 
#---------------------------------------------------------
  def __getTypedParam(self, cls):
    result = []
    for param in self.__params:
      if (isinstance(param, cls)):
        result.append(param)
    return result
      