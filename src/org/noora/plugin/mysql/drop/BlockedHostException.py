#!/usr/bin/env python

class BlockedHostException(Exception):
    
  def __init__(self, message, blockedHost):
    Exception.__init__(self)            
    self.__blockedHost=blockedHost    
    message = message + " " + blockedHost 
    self.__message=message  

  def __str__(self):
    return repr(self.__message)

  def getMessage(self):
    return self.__message
  
  def getBlockedHost(self):
    return self.__blockedHost
