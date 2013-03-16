
import os

class Directory(object):
  
  def __init__(self):
    self.__dirstack = [ os.getcwd() ]
    
  def pushDir(self,directory):
    self.__dirstack.append(directory)
    os.chdir(directory)
    
  def popDir(self):
    self.__dirstack.pop()
    directory = self.__dirstack[-1]
    if directory:
      os.chdir(directory)
        