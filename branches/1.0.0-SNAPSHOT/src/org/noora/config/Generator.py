from org.noora.config.generator.DatabaseGenerator import DatabaseGenerator
from org.noora.config.generator.KeyValueGenerator import KeyValueGenerator
from org.noora.config.generator.ListGenerator import ListGenerator
from org.noora.config.generator.ParamGenerator import ParamGenerator
from org.noora.io.NoOraError import NoOraError
import re

class Generator(object):

  def __init__(self, plugin):
    self.__generators = { 'keyval'   : KeyValueGenerator(self,plugin),
                          'param'    : ParamGenerator(self,plugin),
                          'database' : DatabaseGenerator(self,plugin),
                          'list'     : ListGenerator(self,plugin)
                        }
    #self.__regex = re.compile(r"@{([a-z]+):([^}]+)}")
    self.__regex = re.compile(r"@{([a-z]+):([-_a-zA-Z0-9]+)(\[[0-9]\])?}")

#---------------------------------------------------------
# Wheezy template accessor functions
#---------------------------------------------------------
  def keyval(self,name):
    return self.__generators['keyval'].getGeneratedValue(name)

  def param(self,name):
    return self.__generators['param'].getGeneratedValue(name)

  def database(self,name):
    return self.__generators['database'].getGeneratedValue(name)

  def list(self,name):
    return self.__generators['list'].getGeneratedValue(name)

#---------------------------------------------------------
  def getGeneratedValue(self, value):
      
    m = self.__regex.match(value)
    if m:
      value = self.__substituteValue(m)
      
    return value
  
#---------------------------------------------------------
  def replaceGeneratedValues(self, content):  
    return re.sub(self.__regex, self.__replaceValue, content)

#---------------------------------------------------------
  def __replaceValue(self, m):
    value = self.__substituteValue(m)
    if value is None:
      value = "[{0} not found]".format(m.groups()[0])
    
    return value
  
#---------------------------------------------------------
  def __substituteValue(self,m):
    value = None
    (generator,name,offset) = m.groups();
      
    gen = self.__generators.get(generator)
    if gen is None:
      raise NoOraError('detail', "invalid generator command {0}, generator not found".format(name))
        
    genval = gen.getGeneratedValue(name)
    if genval is not None:
      if offset is not None:
        # got @{generator:name[offset]} form
        if not isinstance(genval, list):
          raise NoOraError('detail', "cannot get {0}[{1}] because generated value is not a list".format(name, offset))
          
        idx = offset[1]
        if len(genval) < idx:
          raise NoOraError('detail', "cannot get {0}[{1}] because list contains only {1} elements".format(name, idx, len(genval)))
        
        value = genval[idx]
      else:
        value = genval
        
    return value
        