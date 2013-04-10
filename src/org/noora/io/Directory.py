
import os

class Directory(object):
  
  def __init__(self):
    self.__dirstack = [ os.getcwd() ]
    
#---------------------------------------------------------
  def pushDir(self,directory):
    self.__dirstack.append(directory)
    os.chdir(directory)
    
#---------------------------------------------------------
  def popDir(self):
    if len(self.__dirstack) > 1:
      # safeguard agains extra popDir calls
      self.__dirstack.pop()
      directory = self.__dirstack[-1]
      if directory:
        os.chdir(directory)
        
#---------------------------------------------------------
  def getCurrentDir(self):
    return self.__dirstack[-1]
  