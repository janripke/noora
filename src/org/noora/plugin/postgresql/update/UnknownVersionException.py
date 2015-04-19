#!/usr/bin/env python

class UnknownVersionException(Exception):
    
  def __init__(self, message, version):
    Exception.__init__(self)            
    self.__version=version    
    message = message + " " + version 
    self.__message=message  

  def __str__(self):
    return repr(self.__message)

  def getMessage(self):
    return self.__message
  
  def getUnknownVersion(self):
    return self.__version
