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