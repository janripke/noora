#!/usr/bin/env python
from org.noora.version.Version import Version

class VersionFactory:
  def __init__(self):
    pass
  
  @staticmethod
  def newVersion(major=None, minor=None, revision=None, patch=None):
    return Version(major, minor, revision, patch)
