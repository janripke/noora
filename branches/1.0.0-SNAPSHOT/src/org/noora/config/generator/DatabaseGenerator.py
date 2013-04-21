from org.noora.config.generator.GeneratorBase import GeneratorBase
from org.noora.io.NoOraError import NoOraError
from xml.etree import ElementTree


class DatabaseGenerator(GeneratorBase):

  def __init__(self, generator, plugin):
    GeneratorBase.__init__(self, generator, plugin)
    
#---------------------------------------------------------
  def getGeneratedValue(self, name):
    # this generator only works for plugins that define (and set) option 'database'
    plugin = self.getPlugin()
    database = plugin.getOptionValue('database')
    
    if database is None:
      raise NoOraError('detail', "cannot generate value for database:{0}. No --database specified".format(name))
    
    if name == 'connector-template':
      return self.__getConnectorTemplate(database)
    
    raise NoOraError('detail', "invalid attribute to generator 'database', {0} not implemented".format(name))
    
#---------------------------------------------------------
  def __getConnectorTemplate(self, database):
    
    config = self.getConfig()
    if config is not None:
      
        elem = config.getFirstElement("databases/database[@name='{0}']/connector-template".format(database))
        if elem is not None and len(elem) > 0:
          xmlstr = ElementTree.tostring(elem[0])
          if xmlstr:
            generator = self.getGenerator()
            xmlstr = generator.replaceGeneratedValues(xmlstr)
          return xmlstr
        
    raise NoOraError('detail', "invalid configuration, database connector-template for {0} not found".format(database))

          
          