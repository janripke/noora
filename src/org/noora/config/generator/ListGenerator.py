from org.noora.config.generator.GeneratorBase import GeneratorBase

class ListGenerator(GeneratorBase):

  def __init__(self, generator, plugin):
    GeneratorBase.__init__(self, generator, plugin)

#---------------------------------------------------------  
  def getGeneratedValue(self, name):
    result = []
    
    config = self.getConfig()
    if config is not None:
      listelems = config.getFirstElement("defaults/lists/list[@name='{0}']".format(name))
      if listelems is not None:
        for elem in listelems:
          result.append(elem.text)
          
    return result
        