#!/usr/bin/env python


class Property:
  
  def __init__(self, key, value):
    self.__key = key
    self.__value = value
    
  def getKey(self):
    return self.__key
  
  def getValue(self):
    return self.__value
  
  def setValue(self, value):
    self.__value = value



       


