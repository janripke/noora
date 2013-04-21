from org.noora.config.generator.DatabaseGenerator import DatabaseGenerator
from org.noora.config.generator.KeyValueGenerator import KeyValueGenerator
from org.noora.config.generator.ListGenerator import ListGenerator
from org.noora.config.generator.ParamGenerator import ParamGenerator
import re

class Generator(object):

  def __init__(self, plugin):
    self.__generators = { 'keyval'   : KeyValueGenerator(self,plugin),
                          'param'    : ParamGenerator(self,plugin),
                          'database' : DatabaseGenerator(self,plugin),
                          'list'     : ListGenerator(self,plugin)
                        }
    self.__regex = re.compile(r"@{([a-z]+):([^}]+)}")
    
#---------------------------------------------------------
  def getGeneratedValue(self, value):
      
    m = self.__regex.match(value)
    if m:
      groups = m.groups()
      if len(groups) == 2:
        name = groups[0]
        val = groups[1]
        if self.__generators[name]:
          generator = self.__generators[name];
          retval = generator.getGeneratedValue(val)
          if not retval:
            retval = value
          return retval
    return value
    
#---------------------------------------------------------
  def replaceGeneratedValues(self, content):  
    return re.sub(self.__regex, self.__replaceValue, content)

#---------------------------------------------------------
  def __replaceValue(self, m):
    groups = m.groups()
    name = groups[0]
    val = groups[1] 
    
    gen = self.__generators.get(name)
    if gen:
      replacement = gen.getGeneratedValue(val)
      if replacement:
        return replacement
    
    return "[{0} not found]".format(name)
        