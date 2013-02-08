#!/usr/bin/env python

import core.Plugin as Plugin
import core.StreamHelper  as StreamHelper
import os

M_LF=chr(10)


class BuildPlugin(Plugin.Plugin):
  def __init__(self):
    Plugin.Plugin.__init__(self)
    self.setType("BUILD")

  def getUsage(self):
    print "NoOra database installer, build.py"
    print "creates installation scripts"
    print "-u= --user= --scheme=  not required, contains the scheme."
    print "-v= --verion=  not required, contains the version."

  def hasItem(self, items, value):
    for item in items:
      if item.lower()==value.lower():
        return True
    return False

  def appendNotPresent(self, items, value):
    if self.hasItem(items, value)==False:
      items.append(value)
    return items


  def synchronizeFile(self, folder, filename):

    projectHelper=self.getProjectHelper()  
    files=projectHelper.findFiles(folder)
    url=folder+os.sep+filename

    stream=''          
    if os.path.isfile(url):
      stream=projectHelper.readFile(url)

    # convert the content of the file to linux format (LF)
    streamHelper=StreamHelper.StreamHelper()
    stream=streamHelper.convert(stream)

    lines=stream.split(M_LF)
    for file in files:
      if self.hasItem(lines,'@@'+file)==False:
        print "adding "+folder.split(self.getBaseDir())[1]+os.sep+file
      lines=self.appendNotPresent(lines,'prompt '+folder.split(self.getBaseDir())[1]+os.sep+file)
      lines=self.appendNotPresent(lines,'@@'+file)

    synchronized_lines=list(lines)
    for line in lines:

      if line.startswith('prompt '):
        if self.hasItem(files,line.replace('prompt '+folder.split(self.getBaseDir())[1]+os.sep,''))==False:
          synchronized_lines.remove(line)
      if line.startswith('@@'):        
        if self.hasItem(files,line.replace('@@',''))==False:
          print "removing "+folder.split(self.getBaseDir())[1]+os.sep+line
          synchronized_lines.remove(line)
              
    stream = M_LF.join(synchronized_lines)              
    projectHelper.writeFile(url,stream)    


  def execute(self, parameterHelper):
    if parameterHelper.hasParameter('-h'):
      self.getUsage()
      exit(1)

    projectHelper=self.getProjectHelper()
    configReader=self.getConfigReader()
           
    schemes=configReader.getValue('SCHEMES')
    schemes=parameterHelper.getParameterValue(['-u=','--scheme=','--user='],schemes)
    configReader.invalidValue('SCHEMES',schemes)

    versions=configReader.getValue('VERSIONS')
    versions=parameterHelper.getParameterValue(['-v=','--version='],versions)
    configReader.invalidValue('VERSIONS',versions)

    objects = configReader.getValue('CREATE_OBJECTS')
    environments= configReader.getValue('ENVIRONMENTS')

    for version in versions:
      buildFolder=projectHelper.getBuildFolder(versions, version)
      projectHelper.invalidBuildFolder(buildFolder)

      
      for scheme in schemes:
        globalDdlObjects=[]
        specificDdlObjects=[]
        globalDatObjects=[]
        specificDatObjects=[]

        print "building scheme '"+scheme+"' for version '"+version+"'"
        for object in objects:  

          # global ddl objects
          folder=buildFolder+os.sep+scheme+os.sep+'ddl'+os.sep+object
          if projectHelper.folderPresent(folder):
            self.synchronizeFile(folder,'install.sql')           
            globalDdlObjects.append('@@ddl/'+object+'/install.sql')

          # environment specific ddl objects
          for environment in environments:          
            folder=buildFolder+os.sep+scheme+os.sep+'ddl'+os.sep+object+os.sep+environment
            if projectHelper.folderPresent(folder):
              self.synchronizeFile(folder,'install.sql')
              specificDdlObjects.append([environment,'@@ddl/'+object+'/'+environment+'/install.sql'])          

        # global dat objects
        folder=buildFolder+os.sep+scheme+os.sep+'dat'
        if projectHelper.folderPresent(folder):
          self.synchronizeFile(folder,'install.sql')
          globalDatObjects.append('@@dat/install.sql')

        # environment specific dat objects
        for environment in environments:
          folder=buildFolder+os.sep+scheme+os.sep+'dat'+os.sep+environment
          if projectHelper.folderPresent(folder):
            self.synchronizeFile(folder,'install.sql')
            specificDatObjects.append([environment,'@@dat/'+environment+'/install.sql'])

        # create install_scheme.sql script if not present
        for environment in environments:
          filename='install_scheme_'+environment+'.sql'      
          url=buildFolder+os.sep+scheme+os.sep+filename

          if os.path.isfile(url)==False:
            templateUrl=projectHelper.findTemplateFile('install_scheme.sql')
            projectHelper.copyFile(templateUrl,url)
            stream=projectHelper.readFile(url)            
            stream=stream.replace('<install>','install_'+environment)
            projectHelper.writeFile(url,stream)
      
        # create install.sql for install_scheme.sql
        for environment in environments:
          filename='install_'+environment+'.sql'            
          url=buildFolder+os.sep+scheme+os.sep+filename
                  
          stream = M_LF.join(globalDdlObjects)  
          for specificDdlObject in specificDdlObjects:
            if specificDdlObject[0]==environment:
              stream = stream + M_LF + specificDdlObject[1]
          stream = stream + M_LF + M_LF.join(globalDatObjects)  
          for specificDatObject in specificDatObjects:
            if specificDatObject[0]==environment:
              stream = stream + M_LF + specificDatObject[1]

          projectHelper.writeFile(url,stream)      


