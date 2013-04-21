from org.noora.config.generator.GeneratorBase import GeneratorBase
from org.noora.io.NoOraError import NoOraError

class ParamGenerator(GeneratorBase):

  def __init__(self, generator, plugin):
    GeneratorBase.__init__(self, generator, plugin)

#---------------------------------------------------------  
  def getGeneratedValue(self, name):
    value = self.getPlugin().getOptionValue(name)
    if value:
      return value
    
    raise NoOraError('detail', "Unknown parameter {0}".format(name))
        