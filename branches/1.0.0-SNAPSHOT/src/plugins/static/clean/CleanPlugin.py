#!/usr/bin/env python

import core.Plugin as Plugin
import os


class CleanPlugin(Plugin.Plugin):
  def __init__(self):
    Plugin.Plugin.__init__(self)
    self.setType("CLEAN")


  def getUsage(self):
    print "NoOra database installer, clean"
    print "removes installation scripts"
    print "-u= --scheme=  not required, contains the scheme."
    print "-v= --verion=  not required, contains the version."

  def execute(self, parameterHelper):
    if parameterHelper.hasParameter('-h'):
      self.getUsage()
      exit(1)    

    configReader=self.getConfigReader()
    projectHelper=self.getProjectHelper()
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

        print "cleaning scheme '"+scheme+"' for version '"+version+"'"
        for object in objects:  
          for environment in environments:          

            # environment specific ddl objects
            folder=buildFolder+os.sep+scheme+os.sep+'ddl'+os.sep+object+os.sep+environment
            url=folder+os.sep+'install.sql'
            if os.path.isfile(url):
              os.remove(url)

          # global ddl objects
          folder=buildFolder+os.sep+scheme+os.sep+'ddl'+os.sep+object
          url=folder+os.sep+'install.sql'
          if os.path.isfile(url):
            os.remove(url)

        for environment in environments:
 
          # environment specific dat objects
          folder=buildFolder+os.sep+scheme+os.sep+'dat'+os.sep+environment
          url=folder+os.sep+'install.sql'
          if os.path.isfile(url):
            os.remove(url)


        # global dat objects
        folder=buildFolder+os.sep+scheme+os.sep+'dat'
        url=folder+os.sep+'install.sql'
        if os.path.isfile(url):
          os.remove(url)


      # remove install_scheme.sql script
      folder=buildFolder+os.sep+scheme
      for environment in environments:
        url=folder+os.sep+'install_scheme_'+environment+'.sql'
        if os.path.isfile(url):
          os.remove(url)

      # remove install.sql script in the schema folder.
      folder=buildFolder+os.sep+scheme
      for environment in environments:
        url=folder+os.sep+'install_'+environment+'.sql'
        if os.path.isfile(url):
          os.remove(url)


