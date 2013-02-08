#!/usr/bin/env python
import core.ApplicationException  as ApplicationException
import os.path

class Fileable:
  def __init__(self, pathName=None):
    pass
    
  @staticmethod
  def pathSeperator(self):
    raise ApplicationException.ApplicationException("method not implemented")
  
  def exists(self):
    raise ApplicationException.ApplicationException("method not implemented")
  
  def notExists(self):
    raise ApplicationException.ApplicationException("method not implemented")
  
  def isFile(self):
    raise ApplicationException.ApplicationException("method not implemented")
  
  def isDirectory(self):
    raise ApplicationException.ApplicationException("method not implemented")
  
  def getName(self):
    raise ApplicationException.ApplicationException("method not implemented")
  
  def getPath(self):
    raise ApplicationException.ApplicationException("method not implemented")
  
  def getExtension(self):
    raise ApplicationException.ApplicationException("method not implemented")
  
  def getRoot(self):
    raise ApplicationException.ApplicationException("method not implemented")
  
  def delete(self,recursive=False):
    raise ApplicationException.ApplicationException("method not implemented")

class File(Fileable):
  def __init__(self, pathName=None):
    self.__pathName=pathName
    
  @staticmethod
  def pathSeperator():
    return os.sep    
    
  def exists(self):
    if self.isFile():
      return True
    if self.isDirectory():
      return True
    return False
      
  def notExists(self):
    if self.exists():
      return False
    return True
  
  def isFile(self):
    pathName = self.__pathName
    return os.path.isfile(pathName)
  
  def isDirectory(self):
    pathName = self.__pathName
    return os.path.isdir(pathName)
  
  def getName(self):
    pathName = self.__pathName
    folder,filename=os.path.split(pathName)
    return filename
  
  def getPath(self):
    pathName = self.__pathName
    folder,filename=os.path.split(pathName)
    return folder

  def getExtension(self):
    pathName = self.__pathName
    root,extension=os.path.splitext(pathName)
    return extension.lstrip('.')  
  
  def getRoot(self):
    pathName = self.__pathName
    root,extension=os.path.splitext(pathName)
    return root 

  def delete(self):
    pathName = self.__pathName
    if self.isFile():      
      os.remove(pathName)
    if self.isDirectory():
      os.rmdir(pathName)



class Readable:
  
  def __init__(self):
    pass
  
  def read(self):  
    raise ApplicationException.ApplicationException("method not implemented")
  
  def close(self):
    raise ApplicationException.ApplicationException("method not implemented")
  
  
class FileReader(Readable):
  def __init__(self, file=None):
    Readable.__init__(self)
    self.__file = file
    pathName = file.getPath() + file.getName()
    self.__handle = open(pathName,'rb')
    
  def read(self):
    handle = self.__handle
    stream = handle.read()
    stream = stream.replace(chr(13)+chr(10),chr(10))
    stream = stream.replace(chr(13),chr(10)) 
    return stream
  
  def getFile(self):
    return self.__file
    
  def close(self):
    handle = self.__handle
    handle.close()
    
    
    
    
class Writeable:
  
  def __init__(self):
    pass
  
  def write(self, buffer):  
    raise ApplicationException.ApplicationException("method not implemented")
  
  def close(self):
    raise ApplicationException.ApplicationException("method not implemented")


class FileWriter(Writeable):
  def __init__(self, file=None):
    Writeable.__init__(self)
    self.__file = file
    pathName = file.getPath() + file.getPathSeperator() + file.getName()        
    self.__handle = open(pathName,'wb')
    
  def write(self, buffer):
    handle = self.__handle
    handle.write(buffer)
    
  def close(self):
    handle = self.__handle
    handle.close()
    
    
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
  
  def list(self, file=None,recursive=False, exclude=None):
    result=[]
    if file.exists():
      folder = file.getPath()
      fileList=os.listdir(folder)

      for fileItem in fileList:
        pathName = folder + os.sep + fileItem
        candidateFile = File(pathName)
        if candidateFile.isFile() and exclude!="file":          
          result.append(candidateFile)
        if candidateFile.isDirectory() and exclude!="directory":
          result.append(candidateFile)
        if candidateFile.isDirectory() and recursive==True:
          recursiveFiles = self.list(file, recursive, exclude)
          for recursiveFile in recursiveFiles:
            result.append(recursiveFile)
      result.sort()
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


class Loadable:  
  def __init__(self):
    pass
  
  def load(self, fileReader = None):  
    raise ApplicationException.ApplicationException("method not implemented")
  
class NoOraPropertyLoader(Loadable):
  def __init__(self, properties):
    Loadable.__init__(self)
    self.__properties = properties

  def getProperties(self):
    return self.__properties
    
    
  def load(self, fileReader = None):
    properties = self.getProperties()
    
    lines = fileReader.read()
    lines = lines.split(chr(10))
    buffer=[]
    for line  in lines:
      if len(line)!=0 and line.startswith("#")==False:
        buffer.append(line)

    property = None
    for line in buffer:
      pairs=line.split("=",1)
      
      if len(pairs)==2:
        key = pairs[0]
        value  = pairs[1].strip()
        property = properties.setProperty(key, value)
      if len(pairs)==1:
        key = property.getKey()
        value = property.getValue() + pairs[0].strip()
        property = properties.setProperty(key, value)
    return properties
  
class Properties:

  def __init__(self):
    self.__properties = []

  def clear(self):
    self.__properties = []
    


  def containsProperty(self, key):
    result = True
    property = self.getProperty(key)
    if property == None:
      result = False
    return result
    

  def setProperty(self, key, value):
    properties = self.__properties
    if self.containsProperty(key):
      property = self.getProperty(key)
      properties.remove(property)          
    property = Property(key, value)
    properties.append(property)
    return property

  def size(self):
    properties=self.__properties
    return len(properties)
  
  def list(self):
    return self.__properties
  
  def getProperty(self, key):
    result = None
    properties = self.__properties
    for property in properties:
      if property.getKey() == key:
        result = property
    return result
       


