from org.noora.config.generator.Generatable import Generatable

class GeneratorBase(Generatable):

  def __init__(self, generator, plugin):
    Generatable.__init__(self)
    self.__generator = generator
    self.__plugin = plugin
    
#---------------------------------------------------------
  def getGenerator(self):
    return self.__generator

#---------------------------------------------------------
  def getPlugin(self):
    return self.__plugin;
  
#---------------------------------------------------------
  def getApplication(self):
    plugin = self.getPlugin()
    if plugin is not None:
      return plugin.getApplication()
    return None
  
#---------------------------------------------------------
  def getConfig(self):
    application = self.getApplication()
    if application is not None:
      return application.getConfig()
    return None
    
        