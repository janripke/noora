from org.noora.io.File import File
from org.noora.io.Files import Files
from org.noora.version.Version import Version

class VersionLoader:
  def __init__(self, versions):
    self.__versions = versions
    
  def load(self, properties):
    alter = File(properties.getPropertyValue("alter.dir"))
    if alter.exists():
      files = Files()
      for version in files.list(alter):                
        self.__versions.add(Version(version.getName()))
    
    create = File(properties.getPropertyValue("create.dir"))
    if create.exists():
      self.__versions.add(Version(properties.getPropertyValues("DEFAULT_VERSION")))