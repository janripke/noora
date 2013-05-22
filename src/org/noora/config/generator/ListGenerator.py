from org.noora.config.generator.GeneratorBase import GeneratorBase
from org.noora.io.NoOraError import NoOraError

class ListGenerator(GeneratorBase):

  def __init__(self, generator, plugin):
    GeneratorBase.__init__(self, generator, plugin)

#---------------------------------------------------------  
  def getGeneratedValue(self, name):
    result = []
    
    # list available as option/env/default-config?
    plugin = self.getPlugin()
    optionValues = plugin.getOptionValue(name)
    if optionValues is not None:
      return optionValues
    
    # available as default list in config?
    config = self.getConfig()
    listelems = config.getFirstElement("defaults/lists/list[@name='{0}']".format(name))
    if listelems is not None:
      for elem in listelems:
        result.append(elem.text)
      return result
    
    raise NoOraError('detail', "cannot find list defaults/lists/list[@name='{0}']".format(name))
        