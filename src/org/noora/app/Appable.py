#!/usr/bin/env python
from org.noora.app.AppException import AppException

class Appable:
  def __init__(self):
    pass
  
  def checkRequiredOptions(self):
    raise AppException("method not implemented")
    
