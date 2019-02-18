class VersionHelper(object):
  def __init__(self, versions):
    self.__versions=self.getWeightList(versions)

  def getVersions(self):
    return self.__versions

  def getMajorPart(self, value):
    if len(value.split('.'))>=1:
      return int(value.split('.')[0])
    return 0

  def getMinorPart(self, value):
    if len(value.split('.'))>=2:
      return int(value.split('.')[1])
    return 0

  def getRevisionPart(self, value):
    if len(value.split('.'))>=3:
      return int(value.split('.')[2])
    return 0
  
  def getPatchPart(self, value):    
    if len(value.split('.'))>=4:
      return int(value.split('.')[3])  
    return 0

  def getNextRevision(self, default):
    versions=self.getVersions()
    versions.sort()
    if len(versions)!=0:
      lastVersion=versions[len(versions)-1][1]
      majorPart=self.getMajorPart(lastVersion)
      minorPart=self.getMinorPart(lastVersion)
      revisionPart=self.getRevisionPart(lastVersion)
      patchPart=self.getPatchPart(lastVersion)
      return str(majorPart)+'.'+str(minorPart)+'.'+str(revisionPart)+'.'+str(patchPart+1)
    return default

  def getWeightList(self, versions):
    items=[]
    for version in versions:
      majorPart=self.getMajorPart(version)
      minorPart=self.getMinorPart(version)
      revisionPart=self.getRevisionPart(version)
      patchPart=self.getPatchPart(version)
      items.append([(patchPart)+(100*revisionPart)+(10000*minorPart)+(1000000*majorPart),version])
    return items

  def sort(self):
    items=[]
    versions=self.getVersions()
    versions.sort()
    for version in versions:
      items.append(version[1])
    return items
