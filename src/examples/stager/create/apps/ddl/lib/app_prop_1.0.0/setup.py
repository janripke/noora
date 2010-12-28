#!/usr/bin/env python
import sys
import os
import subprocess


import ComponentHelper   as ComponentHelper
import ConfigReader      as ConfigReader
import ParameterHelper   as ParameterHelper
import NooraException    as NooraException

OBJECTS        = ['usr','dbl','dir','scm','seq','syn','tab','cst','fct','prc','pkg','jar','vw','trg','idx','gra']
BASE_DIR       = os.path.abspath(os.path.dirname(sys.argv[0]))
SILENTMODE     = False

def getUsage():
  print "NoOra database installer, setup.py"
  print "installs a database independend component."
  print "-s= --sid=     required contains the tnsname of the database."
  print "-u= --username=  required, contains the username."
  print "-p= --password=  required, contains the password."
  print "-silent          not required, disables the execution output."


def showErrors(componentHelper):
  try:
    stream=componentHelper.readFile('feedback.log')
    print stream
  except:
    exit(1)


def getPreviousVersion(versions, version):
  index=versions.index(version)
  if index>0:
    previousVersion=versions[index-1]
    return previousVersion    
  return "Nothing"


def executeSqlplus(componentHelper, oracleSid, oracleUser, oraclePasswd, oracleScript, paramA, paramB):
  connectString=oracleUser+'/'+oraclePasswd+'@'+oracleSid
  templateScript=componentHelper.cleanPath('@'+BASE_DIR+os.sep+'setup.sql')
  result=subprocess.call(['sqlplus','-l','-s',connectString , templateScript, oracleScript, paramA, paramB])
  if result!=0:
    showErrors(componentHelper)
    exit(1)

def checkVersion(componentHelper, oracleSid,oracleUser,oraclePasswd,previousVersion, versionSelectStatement):
  oracleScript=BASE_DIR+os.sep+'checkversion.sql'
  executeSqlplus(componentHelper, oracleSid,oracleUser,oraclePasswd, oracleScript,previousVersion,versionSelectStatement)



if __name__ == "__main__":

  try:

    parameterHelper=ParameterHelper.ParameterHelper()   
    if parameterHelper.hasParameter('-h'):
      getUsage()
      exit(1)
      
    if parameterHelper.hasParameter('-silent'):
      SILENTMODE=True      

    componentHelper=ComponentHelper.ComponentHelper()
    configReader=ConfigReader.ConfigReader(BASE_DIR+os.sep+'component.conf')

    oracleSid=parameterHelper.getParameterValue(['-s=','--sid='],[])
    componentHelper.failOnEmpty(oracleSid,'no oracle sid was given')
    oracleSid=oracleSid[0]

    oracleUser=parameterHelper.getParameterValue(['-u=','--username='],[])
    componentHelper.failOnEmpty(oracleUser,'no username was given')
    oracleUser=oracleUser[0]

    oraclePasswd=parameterHelper.getParameterValue(['-p=','--password='],[])
    componentHelper.failOnEmpty(oraclePasswd,'no password was given')
    oraclePasswd=oraclePasswd[0]

    componentName=configReader.getValue('COMPONENT_NAME')
    componentHelper.failOnNone(componentName,'the variable COMPONENT_NAME is not set.')

    componentVersion=configReader.getValue('COMPONENT_VERSION')
    componentHelper.failOnNone(componentName,'the variable COMPONENT_VERSION is not set.')

    componentSelectStatement=configReader.getValue('COMPONENT_SELECT_STATEMENT')
    componentHelper.failOnNone(componentSelectStatement,'the variable COMPONENT_SELECT_STATEMENT is not set.')

    componentVersions=configReader.getValue('COMPONENT_VERSIONS')
    componentHelper.failOnNone(componentVersions,'the variable COMPONENT_VERSIONS is not set.')


    previousVersion=getPreviousVersion(componentVersions,componentVersion)
    checkVersion(componentHelper,oracleSid,oracleUser,oraclePasswd,previousVersion,componentSelectStatement)

    if SILENTMODE==False:
      print "installing component "+componentName+'_'+componentVersion

    for object in OBJECTS:
      
      # ddl objects
      folder=BASE_DIR+os.sep+'ddl'+os.sep+object
      if componentHelper.folderPresent(folder):
        files=componentHelper.findFiles(folder)
        for file in files:
          url=folder+os.sep+file
          if SILENTMODE==False:
            print url.split(BASE_DIR)[1]
          executeSqlplus(componentHelper, oracleSid, oracleUser, oraclePasswd, url, "", "")  

    # global dat files
    folder=BASE_DIR+os.sep+'dat'
    if componentHelper.folderPresent(folder):
      files=componentHelper.findFiles(folder)
      for file in files:
        url=folder+os.sep+file
        if SILENTMODE==False:
          print url.split(BASE_DIR)[1]
        executeSqlplus(componentHelper, oracleSid, oracleUser, oraclePasswd, url, "", "")  

    if SILENTMODE==False:
      print "component "+componentName+'_'+componentVersion+" created."

  except NooraException.NooraException as e:
    print e.getMessage()
    exit(1)
