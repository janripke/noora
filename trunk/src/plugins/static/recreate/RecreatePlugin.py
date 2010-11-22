#!/usr/bin/env python

import core.Plugin as Plugin
import os
import sys
import subprocess

NOORA_DIR    = os.path.abspath(os.path.dirname(sys.argv[0]))
BASE_DIR     = os.path.abspath('.')
CREATE_DIR   = BASE_DIR+os.sep+'create'
PLUGIN_DIR   = NOORA_DIR+os.sep+'plugins'+os.sep+'static'+os.sep+'recreate'
SCRIPT_DIR   = NOORA_DIR+os.sep+'scripts'


class RecreatePlugin(Plugin.Plugin):
  def __init__(self):
    Plugin.Plugin.__init__(self)
    self.setType("RECREATE")


  def getUsage(self):  
    print "NoOra database installer, recreate.py"
    print "recreates the database objects of the defined schemes."
    print "-s= --sid=     required contains the tnsname of the database."
    print "-u= --scheme=  not required, contains the scheme of "
    print "               the database objects to drop."
    print "-e= --env=     not required, used for mapping "
    print "               the username and password."
    print "-nocompile     not required, disable the compilation of "
    print "               packages, triggers and views."  
    print "-m= --max=     not required, after the given version recreation will stop."
    print "-test          not required, executes the defined unit tests after recreation."



  def showErrors(self):
    try:
      projectHelper=self.getProjectHelper()
      stream=projectHelper.readFile('feedback.log')
      print stream
    except:
      exit(1)

  def getMaxVersion(self,versions):
    return versions[len(versions)-1]

  def executeSqlplus(self, oracleSid, oracleUser, oraclePasswd, oracleScript):
    projectHelper=self.getProjectHelper()
    os.chdir(os.path.dirname(oracleScript))
    connectString=oracleUser+'/'+oraclePasswd+'@'+oracleSid
    templateScript=projectHelper.cleanPath('@'+SCRIPT_DIR+os.sep+'template.sql')
    result=subprocess.call(['sqlplus','-l','-s',connectString , templateScript, oracleScript])
    if result!=0:
      self.showErrors()
      exit(1)

  def dropDatabase(self, oracleSid, scheme, environment):
    if len(scheme)==0:
      result=subprocess.call(['python',NOORA_DIR+os.sep+'noora.py','drop','--sid='+oracleSid,'--env='+environment])
      if result!=0:
        exit(1)    
    else:
      result=subprocess.call(['python',NOORA_DIR+os.sep+'noora.py','drop','--sid='+oracleSid,'--scheme='+scheme[0],'--env='+environment])
      if result!=0:
        exit(1)

  def createDatabase(self, oracleSid, scheme, environment):
    if len(scheme)==0:
      result=subprocess.call(['python',NOORA_DIR+os.sep+'noora.py', 'create','--sid='+oracleSid,'--env='+environment,'-nocompile'])
      if result!=0:
        exit(1)
    else:      
      result=subprocess.call(['python',NOORA_DIR+os.sep+'noora.py','create', '--sid='+oracleSid,'--scheme='+scheme[0],'--env='+environment,'-nocompile'])
      if result!=0:
        exit(1)


  def updateDatabase(self, oracleSid, scheme, environment, versions, maxVersion):
    for version in versions:
      if version!=versions[0]:
        if len(scheme)==0:
          result=subprocess.call(['python',NOORA_DIR+os.sep+'noora.py','update','-v='+version,'--sid='+oracleSid,'--env='+environment,'-nocompile'])        
          if result!=0:
            exit(1)
        else:
          result=subprocess.call(['python',NOORA_DIR+os.sep+'noora.py','update','-v='+version,'--sid='+oracleSid,'--scheme='+scheme,'--env='+environment,'-nocompile'])
          if result!=0:
            exit(1)
        if version==maxVersion:
          break


  def recompile(self, oracleSid, oracleUser, oraclePasswd):
    oracleScript=SCRIPT_DIR+os.sep+'recompile.sql'
    self.executeSqlplus(oracleSid, oracleUser, oraclePasswd, oracleScript)

  def unittest(self, oracleSid, oracleUser, oraclePasswd):
    oracleScript=SCRIPT_DIR+os.sep+'unittest.sql'
    self.executeSqlplus(oracleSid, oracleUser, oraclePasswd, oracleScript)



  def execute(self, parameterHelper):
    if parameterHelper.hasParameter('-h'):
      self.getUsage()
      exit(1)    

    configReader=self.getConfigReader()
    projectHelper=self.getProjectHelper()

    oracleSid=parameterHelper.getParameterValue(['-s=','--sid='],[])
    projectHelper.failOnEmpty(oracleSid,'no oracle sid was given.')
    configReader.failOnValueNotFound('ORACLE_SIDS',oracleSid,'the given oracle sid is not valid for this project.')
    oracleSid=oracleSid[0]

    scheme=parameterHelper.getParameterValue(['-u=','--scheme=','--user='],[])
    
    schemes=configReader.getValue('SCHEMES')
    schemes=parameterHelper.getParameterValue(['-u=','--scheme=','--user='],schemes)
    configReader.failOnValueNotFound('SCHEMES',schemes,'the given scheme is not valid for this project.')

    environment=configReader.getValue('DEFAULT_ENVIRONMENT')
    environment=parameterHelper.getParameterValue(['-e=','--env='],[environment])
    projectHelper.failOnEmpty(environment,'no environment was found')
    configReader.failOnValueNotFound('ENVIRONMENTS',environment,'the given environment is not valid for this project.')
    environment=environment[0]

    versions=configReader.getValue('VERSIONS')
    projectHelper.failOnEmpty(versions,'the variable VERSIONS is not set.')
    maxVersion=self.getMaxVersion(versions)
    maxVersion=parameterHelper.getParameterValue(['-m=','--max='],[maxVersion])
    configReader.failOnValueNotFound('VERSIONS',maxVersion,'the given max version is not valid for this project.')
    maxVersion=maxVersion[0]

    self.dropDatabase(oracleSid, scheme, environment)
    self.createDatabase(oracleSid, scheme, environment)
    self.updateDatabase(oracleSid, scheme, environment, versions, maxVersion)

    if  parameterHelper.hasParameter('-nocompile')==False:
      for scheme in schemes:
        print "compiling scheme '"+scheme+"' in database '"+oracleSid+"' using environment '"+environment+"'"
        oracleUser=projectHelper.getOracleUser(oracleSid, scheme)
        oraclePasswd=projectHelper.getOraclePasswd(oracleSid, scheme)
        self.recompile(oracleSid,oracleUser,oraclePasswd)
        print "scheme '"+scheme+"' compiled."

    if parameterHelper.hasParameter('-test')==True:
      for scheme in schemes:
        oracleUser=projectHelper.getOracleUser(oracleSid, scheme)
        oraclePasswd=projectHelper.getOraclePasswd(oracleSid, scheme)
        self.unittest(oracleSid, oracleUser, oraclePasswd)

