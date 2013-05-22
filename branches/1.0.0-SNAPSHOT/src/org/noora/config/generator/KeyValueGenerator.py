
from org.noora.config.generator.GeneratorBase import GeneratorBase
from org.noora.io.NoOraError import NoOraError

## @class KeyValueGenerator
# Generates a value given a key.
# The key-value pair is taken from the configuration files and uses the xpath /keyvals/keyval[\@key='<key>'].
# The configuration file will normally be $PROJECT_HOME/config/defaults.xml
#
# example defaults.xml:
#
#     <defaults>
#       <version>1.0.0</version>
#     </defaults>
#
# will be accessed by "@{param:version}"
#

class KeyValueGenerator(GeneratorBase):

  def __init__(self, generator, plugin):
    GeneratorBase.__init__(self, generator, plugin)

#---------------------------------------------------------
  def getGeneratedValue(self, name):
    ## Get the value associated with key 'name'.
    # @param name the key value.
    # @return the associated value.
    # @exception NoOraError raised when the key is not found or the config object does not exist.
    
    config = self.getConfig()
    if config is not None:
      elem = config.getFirstElement("keyvals/keyval[@key='{0}']".format(name))
      if elem is not None:
        return elem.get('value')
      raise NoOraError('detail', "cannot find element for key {0} (keyval generator)".format(name))
    raise NoOraError('detail', "keyval generator has no config object attached (key={0})".format(name))
    