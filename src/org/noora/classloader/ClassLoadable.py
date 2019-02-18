from org.noora.classloader.ClassLoaderException import ClassLoaderException


class ClassLoadable(object):
  def find(self, moduleName, className):
    raise ClassLoaderException("method not implemented") 
    
  def findByPattern(self, pattern):
    raise ClassLoaderException("method not implemented")
