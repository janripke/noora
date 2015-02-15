#!/usr/bin/env python
from org.noora.io.File import File
import os
    
class Files:
  def __init__(self):
    pass
  
  def copy(self, fileReader, fileWriter):
    stream = fileReader.read()
    fileReader.close()
    
    fileWriter.write(stream)
    fileWriter.close()
    
  def move(self, fileReader, fileWriter):
    stream = fileReader.read()
    fileReader.close()
    
    fileWriter.write(stream)
    fileWriter.close()
    
    file = fileReader.getFile()
    file.delete()
  
  
  
  @staticmethod
  def list(file=None,recursive=False, exclude=None):
    result=[]
    
    if file.exists():
      folder = file.getPath()+os.sep+file.getName()
      fileList=os.listdir(folder) 
      fileList.sort()     
      for fileItem in fileList:
        pathName = folder + os.sep + fileItem
        candidateFile = File(pathName)
        if candidateFile.isFile() and exclude!="file":          
          result.append(candidateFile)
        if candidateFile.isDirectory() and exclude!="directory":
          result.append(candidateFile)
        if candidateFile.isDirectory() and recursive==True:
          recursiveFiles = Files.list(candidateFile, recursive, exclude)
          for recursiveFile in recursiveFiles:
            result.append(recursiveFile)
      #result.sort()
    return result

  
  def delete(self, file=None, recursive=False):
    if file.isFile():
      file.delete()
    if file.isDirectory() and recursive==False:
      file.delete()
    if file.isDirectory() and recursive==True:
      foundFiles=self.listFiles(file, recursive)
      for foundFile in foundFiles:
        foundFile.delete()

      foundDirectories=self.listDirectories(file)
      foundDirectories.reverse()
      for foundDirectory in foundDirectories:
        foundDirectory.delete()

      file.delete()    


       


