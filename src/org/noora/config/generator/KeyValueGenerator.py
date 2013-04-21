
from org.noora.config.generator.GeneratorBase import GeneratorBase
from org.noora.io.NoOraError import NoOraError

class KeyValueGenerator(GeneratorBase):

  def __init__(self, generator, plugin):
    GeneratorBase.__init__(self, generator, plugin)

#---------------------------------------------------------
  def getGeneratedValue(self, name):
    config = self.getConfig()
    if config is not None:
      elem = config.getFirstElement("keyvals/keyval[@key='{0}']".format(name))
      if elem is not None:
        return elem.get('value')
      raise NoOraError('detail', "cannot find element for key {0} (keyval generator)".format(name))
    raise NoOraError('detail', "keyval generator has no config object attached (key={0})".format(name))
    