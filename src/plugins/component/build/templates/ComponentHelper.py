#!/usr/bin/env python

import os
import platform
import NooraException as NooraException
import subprocess

BASE_DIR    = os.path.abspath('.')
# 'constant' to determine if we're on the cyswin platform
ON_CYGWIN=platform.system().lower().find("cygwin") == -1;

class ComponentHelper:
  
  def __init__(self):
    pass

  def fileNotPresent(self, url):
    if os.path.isfile(url):
      return False
    return True      


  def folderNotPresent(self, folder):
    if os.path.isdir(folder):
      return False
    return True

  def folderPresent(self, folder):
    if os.path.isdir(folder):
      return True
    return False

  def failOnEmpty(self, values, message):
    if len(values)==0:
      raise NooraException.NooraException(message)

  def failOnFolderNotPresent(self, folder, message):
    if self.folderNotPresent(folder):
      raise NooraException.NooraException(message)

  def failOnFolderPresent(self, folder, message):
    if self.folderPresent(folder):
      raise NooraException.NooraException(message)

  def failOnNone(self, value, message):
    if value==None:
      raise NooraException.NooraException(message)
  
  def failOnFileNotPresent(self, url, message):
    if self.fileNotPresent(url):
      raise NooraException.NooraException(message)
  
  def hasValue(self, list, value):
    for item in list:
      if item==value:
        return True
    return False
  
  def failOnValueNotFound(self, list, value, message):  
    if self.hasValue(list, value)==False:
      raise NooraException.NooraException(message)


  def findFiles(self, folder):
    result=[]
    if os.path.isdir(folder):
      files=os.listdir(folder)
      for file in files:
        url=folder+os.sep+file
        if os.path.isfile(url):
          result.append(file)
      result.sort()
    return result

  def readFile(self, filename):
    handle=open(filename,'rb')
    stream=handle.read()
    handle.close()
    return stream


  # if we're on cygwin: change cygwin path to windows path 
  # so we can use it as a command line param for windows programs (e.g. sqlplus)
  # (exec.. so pretty expensive :-( )
  def cleanPath(self, path):
    if ON_CYGWIN:
      return path
    else:
      proc = subprocess.Popen(["cygpath -wa "+ path], stdout=subprocess.PIPE, shell=True);
      (out, err) = proc.communicate();
      result = out.rstrip();      
      
    return result;




     
