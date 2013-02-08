#!/usr/bin/env python


class VersionHelper:

  def __init__(self, versions):
    self.__versions=self.getWeightList(versions)

  def getVersions(self):
    return self.__versions

  def getMajorPart(self, value):
    return int(value.split('.')[0])

  def getMinorPart(self, value):
    return int(value.split('.')[1])

  def getRevisionPart(self, value):
    return int(value.split('.')[2])

  def getNextRevision(self, default):
    versions=self.getVersions()
    versions.sort()
    if len(versions)!=0:
      lastVersion=versions[len(versions)-1][1]
      majorPart=self.getMajorPart(lastVersion)
      minorPart=self.getMinorPart(lastVersion)
      revisionPart=self.getRevisionPart(lastVersion)
      return str(majorPart)+'.'+str(minorPart)+'.'+str(revisionPart+1)
    return default

  def getWeightList(self, versions):
    items=[]
    for version in versions:
      majorPart=self.getMajorPart(version)
      minorPart=self.getMinorPart(version)
      revisionPart=self.getRevisionPart(version)
      items.append([(10*revisionPart)+(1000*minorPart)+(10000*majorPart),version])
    return items

  def sort(self):
    items=[]
    versions=self.getVersions()
    versions.sort()
    for version in versions:
      items.append(version[1])
    return items


