#!/usr/bin/env python

import os
import sys
import zipfile
import platform
import subprocess
import core.NooraException as NooraException

# 'constant' to determine if we're on the cyswin platform
ON_CYGWIN=platform.system().lower().find("cygwin") == -1;

class ProjectHelper:

  def __init__(self, configReader):
    self.__configReader=configReader
    self.setBaseDir(os.path.abspath('.'))
    self.setNooraDir(os.path.abspath(os.path.dirname(sys.argv[0])))

  def setConfigReader(self,configReader):
    self.__configReader=configReader

  def setBaseDir(self, path):
    self.__baseDir=path

  def getBaseDir(self):
    return self.__baseDir

  def setNooraDir(self,path):
    self.__nooraDir=path

  def getNooraDir(self):
    return self.__nooraDir

  def getScriptDir(self):
    return self.getNooraDir()+os.sep+'scripts'


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


  def findTemplateFile(self, filename):
    baseDir=self.getBaseDir()
    url=baseDir+os.sep+filename
    if os.path.isfile(url):
      return url
    url=self.getNooraDir()+os.sep+filename
    if os.path.isfile(url):
      return url
    url=self.GetScriptDir()+os.sep+filename
    if os.path.isfile(url):
      return url
    return None

  def getAlterFolder(self):
    baseDir=self.getBaseDir()
    alterFolder=baseDir+os.sep+'alter'
    return alterFolder

  def getCreateFolder(self):
    baseDir=self.getBaseDir()
    createFolder=baseDir+os.sep+'create'
    return createFolder

  def getBuildFolder(self, versions, version):
    createVersion=versions[0]
    baseDir=self.getBaseDir()
    if createVersion==version:
      buildFolder=baseDir+os.sep+'create'
    else:
      buildFolder=baseDir+os.sep+'alter'+os.sep+version
    return buildFolder

  # deprecated, use failOnFolderNotPresent instead.
  def invalidBuildFolder(self, buildFolder):
    if self.folderNotPresent(buildFolder):
      raise NooraException.NooraException('build folder is not present.')

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

  def getOracleUser(self, oracleSid, scheme):
    users=self.__configReader.getValue('ORACLE_USERS')
    for user in users:
      if user[0].lower()==oracleSid.lower() and user[1].lower()==scheme.lower():
        return user[2]
    return None

  def getOraclePasswd(self, oracleSid, scheme):
    users=self.__configReader.getValue('ORACLE_USERS')
    for user in users:
      if user[0].lower()==oracleSid.lower() and user[1].lower()==scheme.lower():
        return user[3]
    return None


  def readFile(self, filename):
    handle=open(filename,'rb')
    stream=handle.read()
    handle.close()
    return stream


  def writeFile(self, filename,stream):
    handle=open(filename,'wb')
    handle.write(stream)
    handle.close()


  def copyFile(self, fromUrl, toUrl):
    stream=self.readFile(fromUrl)
    self.writeFile(toUrl,stream)


  def extractFile(self, url):
    folder=self.getFolder(url)
    file=zipfile.ZipFile(url,'r')
    for info in file.infolist():
      stream=file.read(info.filename)
      extractUrl=folder+os.sep+info.filename
      extractFolder=self.getFolder(extractUrl)
      if self.folderNotPresent(extractFolder):
        os.makedirs(extractFolder)
      self.writeFile(extractUrl,stream)


  def getFilename(self, url):
    folder,filename=os.path.split(url)
    return filename


  def getFileExtension(self, url):
    root,ext=os.path.splitext(url)
    return ext.lstrip('.')

  def getFileRoot(self, url):
    root,ext=os.path.splitext(url)
    return root

  def getFolder(self, url):
    folder,filename=os.path.split(url)
    return folder


  def isFileExcluded(self, url):
    excludedFiles=self.__configReader.getValue('EXCLUDED_FILES')
    self.failOnNone(excludedFiles,'the variable EXCLUDED_FILES is not set.')
    for excludedFile in excludedFiles:
      if self.getFilename(url).lower()==excludedFile.lower():
        return True

    excludedExtensions=self.__configReader.getValue('EXCLUDED_EXTENSIONS')
    self.failOnNone(excludedExtensions,'the variable EXCLUDED_EXTENSIONS is not set.')
    for excludedExtension in excludedExtensions:
      if self.getFileExtension(url)==excludedExtension:
        return True
    return False


  def findFiles(self, folder):
    result=[]
    if os.path.isdir(folder):
      files=os.listdir(folder)
      for file in files:
        url=folder+os.sep+file
        if os.path.isfile(url):
          if self.isFileExcluded(url)==False:
            result.append(file)
      result.sort()
    return result


  def findFilesRecursive(self, folder):
    result=[]
    files=os.listdir(folder)
    for file in files:
      url=folder+os.sep+file
      if os.path.isdir(url):
        subFiles=self.findFilesRecursive(url)
        for subFile in subFiles:
          result.append(subFile)
      else:
        result.append(url)
    return result


  def isFolderExcluded(self, folder):
   excludedFolders=self.__configReader.getValue('EXCLUDED_FOLDERS')
   for excludedFolder in excludedFolders:
     if folder.lower()==excludedFolder.lower():
       return True
   return False


  def findFolders(self, folder):
    result=[]
    items=os.listdir(folder)
    for item in items:
      if os.path.isdir(folder+os.sep+item):
        if self.isFolderExcluded(item)==False:
          result.append(item)
    result.sort()
    return result

  def findFoldersRecursive(self, path):
    result=[]
    folders=os.listdir(path)
    for folder in folders:
      if os.path.isdir(path+os.sep+folder):
        result.append(path+os.sep+folder)
        subFolders=self.findFoldersRecursive(path+os.sep+folder)
        for subFolder in subFolders:
          result.append(subFolder)
    return result


  def removeFolderRecursive(self, path):
    files=self.findFilesRecursive(path)
    for file in files:
      os.remove(file)

    folders=self.findFoldersRecursive(path)
    folders.reverse()
    for folder in folders:
      os.rmdir(folder)

    os.rmdir(path)

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





