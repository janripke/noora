from org.noora.version.Version import Version
from org.noora.io.Path import Path

class VersionGuesser():
  def __init__(self, properties, versions):
    self.__properties = properties
    self.__versions = versions    
  
  def __next__(self, last):
    last
  
  def guess(self, version):
    versions = self.__versions
    properties = self.__properties
    if version:
      return Version(version)
    if versions.next():
      return versions.next()
    return Version(properties.getPropertyValue("DEFAULT_VERSION"))
  
  def toFolder(self, version):
    properties = self.__properties
    if version == properties.getPropertyValues("DEFAULT_VERSION"):
      return properties.getPropertyValue("create.dir")
    return Path.path(properties.getPropertyValue("alter.dir"),version)