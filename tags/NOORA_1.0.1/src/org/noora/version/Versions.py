from org.noora.version.Version import Version

class Versions:
  
  def __init__(self):
    self.__versions = []
  
  def clear(self):
    self.__versions = []
  
  def size(self):
    return len(self.__versions)
  
  def sort(self):
    self.__versions.sort(key=lambda version: version.getWeight(), reverse=False)
  
  def add(self, version):
    versions = self.__versions
    versions.append(version)
  
  def list(self):
    return self.__versions
  
  def previous(self, other):
    versions = self.__versions
    i = 0
    for version in versions:
      if version == other:
        return versions[i-1]
      i = i + 1
      
  def getPart(self, version):
    result = 0
    if version.hasMayor():
      result = result + 1
    if version.hasMinor():
      result = result + 1
    if version.hasRevision():
      result = result + 1
    if version.hasPatch():
      resutl = result + 1
    return result
      
  def next(self):
    last = self.last()
    if last:
      level = self.getPart(last)
      mayor = last.getMayor()
      minor = last.getMinor()
      revision = last.getRevision()
      patch = last.getPatch()
      if level == 1:
        mayor = str(int(mayor)+1)
      if level == 2:
        minor = str(int(minor)+1)
      if level == 3:
        revision = str(int(revision)+1)
      if level == 4:
        patch = str(int(patch)+1)  
      
      if level == 1:
        version = mayor
      if level == 2:
        version = mayor + "." + minor
      if level == 3:
        version = mayor + "." + minor + "." + revision
      if level == 4:
        version = mayor + "." + minor + "." + revision + "." + revision
      
      return Version(version)
      
  def last(self):
    versions = self.__versions
    if versions:
      return versions[self.size()-1]