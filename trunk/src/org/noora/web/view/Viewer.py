from org.noora.web.view.Renderer import Renderer
from org.noora.web.view.Persister import Persister

class Viewer:

    def __init__(self):
      self.__renderer = Renderer()
      self.__persister = Persister()      
            
    def getRenderer(self):
      return self.__renderer
          
    def getPersister(self):
      return self.__persister
    