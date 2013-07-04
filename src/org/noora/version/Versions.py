#!/usr/bin/env python
from org.noora.version.VersionFactory import VersionFactory

class Versions:
  
  def __init__(self):
    self.__versions=[]
       
  def clear(self):
    self.__versions=[]
      
  def getVersions(self):
    return self.__versions
  
  def add(self, version):
    self.__versions.append(version)
  
  def addVersion(self, major=None, minor=None, revision=None, patch=None):
    version = VersionFactory.newVersion(major, minor, revision, patch)
    self.__versions.append(version)
    return version
  
  def lastVersion(self):
    versions = self.__versions
    return versions[len(versions)-1]
  
  def previousVersion(self, other):
    versions = self.__versions
    i = 0
    for version in versions:
      if version == other:
        return versions[i-1]
      i = i + 1
    
      
  def sort(self):
    versions = self.__versions  
    versions.sort(key=lambda version:version.list())
              
  
  def size(self):
    versions = self.__versions
    return len(versions)
  


