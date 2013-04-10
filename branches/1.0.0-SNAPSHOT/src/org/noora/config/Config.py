
from org.noora.config.XmlConfig import XmlConfig
from org.noora.io.File import File
from org.noora.config.PropertyConfig import PropertyConfig

class Config(object):
  
  
  GET_MODE_FIRST = 1    
  """ GET_MODE_FIRST get the first value found """
  
  GET_MODE_MERGE = 2
  """ @var GET_MODE_MERGE merge all values found on the config stack. only works on lists or dictionaries """ 
  
#---------------------------------------------------------
  def __init__(self):
    self.__configs = [];
  
#---------------------------------------------------------
  def pushConfig(self, filepath):
    """ Parse the specified config file and push the result on the config stack
    """
    config = Config.__createConfig(filepath)
    if config:
      config.load()
    self.__configs.append(config)
  
#---------------------------------------------------------
  def popConfig(self):
    if self.__configs:
      self.__configs.pop();
        
#---------------------------------------------------------
  def getProperty(self, name, mode = GET_MODE_FIRST):
    """ get property from config stack.
      When mode = GET_MODE_FIRST then the first value found is returned.
      When mode = GET_MODE_MERGE and the found result is a list then the full config stack is travered 
      and all found values will be merged into the resulting string
      @param name the name of the property
      @param mode either GET_MODE_FIRST (default) or GET_MODE_MERGE
      @return a string or list when the property was found or None when not found
    """
    result = None
    for c in reversed(self.__configs):
      value = c.getProperty(name)
      if value:
        if mode == Config.GET_MODE_FIRST or type(value) != 'list':
          return value

        if result:
          result.extend(value)
        else:
          result = value
 
    return result
  
#---------------------------------------------------------
  def setProperty(self,name, value):
    c = self.__configs[-1]
    if c:
      c.setProperty(name,value)

#---------------------------------------------------------
  def getElement(self, name, mode = GET_MODE_FIRST):
    """ get element(s) from config stack.
      When mode = GET_MODE_FIRST then the first value found is returned.
      When mode = GET_MODE_MERGE and the found result is a list then the full config stack is travered 
      and all found values will be merged into the resulting string
      @param name the name of the property
      @param mode either GET_MODE_FIRST (default) or GET_MODE_MERGE
      @return a string or list when the property was found or None when not found
    """
    result = None
    for c in reversed(self.__configs):
      value = c.getElement(name)
      if value:
        if mode == Config.GET_MODE_FIRST:
          return value

        if result:
          result.extend(value)
        else:
          result = value
 
    return result
  
#---------------------------------------------------------
  def getFirstElement(self, name, mode = GET_MODE_FIRST):
    elem = self.getElement(name, mode)
    if elem and len(elem) > 0:
      return elem[0]
    
    return None
    
#---------------------------------------------------------
  @classmethod
  def __createConfig(cls, filepath):
    configfile = File(filepath)
    ext = configfile.getExtension();
    
    if (ext == "xml"):
      return XmlConfig(configfile);
    elif (ext == "conf"):
      return PropertyConfig(configfile)
    else:
      return None;
  