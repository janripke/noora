#!/usr/bin/env python

class Version:

  def __init__(self, major=None, minor=None, revision=None, patch=None):
    self.__major = major
    self.__minor = minor
    self.__revision = revision
    self.__patch = patch

  def getMajor(self):
    return self.__major
  
  def getMinor(self):
    return self.__minor
  
  def getRevision(self):
    return self.__revision
  
  def getPatch(self):    
    return self.__patch
  
  def list(self):
    result = []    
    if self.__major!=None:
      result.append(self.__major)
    if self.__minor!=None:
      result.append(self.__minor)
    if self.__revision!=None:
      result.append(self.__revision)
    if self.__patch!=None:
      result.append(self.__patch)
    return result
  
  def __eq__(self, other):
    if self.list() == other.list():  # compare name value (should be unique)
      return 1
    else: return 0     
  

  


