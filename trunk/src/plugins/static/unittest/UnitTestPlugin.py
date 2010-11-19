#!/usr/bin/env python

import core.Plugin as Plugin
import os
import sys
import subprocess


NOORA_DIR    = os.path.abspath(os.path.dirname(sys.argv[0]))
BASE_DIR     = os.path.abspath('.')
PLUGIN_DIR   = NOORA_DIR+os.sep+'plugins'+os.sep+'static'+os.sep+'unittest'
SCRIPT_DIR   = NOORA_DIR+os.sep+'scripts'

class UnitTestPlugin(Plugin.Plugin):
  def __init__(self):
    Plugin.Plugin.__init__(self)
    self.setType("UNITTEST")


  def getUsage(self):  
    print "NoOra database installer, unittest.py."
    print "executes unit tests. Uses the noora unit test framework."
    print "remarks : a unit test is always a package. "
    print "          A package containing procedures that start with T_ is considered"
    print "          as a unit test."

    print "-s= --sid=     required contains the tnsname of the database."
    print "-u= --scheme=  not required, contains the scheme of "
    print "               the unit tests to execute."
    print "-e= --env=     not required, used for mapping "
    print "               the username and password."


  def showErrors(self):
    try:
      projectHelper=self.getProjectHelper()
      stream=projectHelper.readFile('feedback.log')
      print stream
    except:
      exit(1)

  def executeSqlplus(self, oracleSid, oracleUser, oraclePasswd, oracleScript):
    projectHelper=self.getProjectHelper()
    os.chdir(os.path.dirname(oracleScript))
    connectString=oracleUser+'/'+oraclePasswd+'@'+oracleSid
    templateScript=projectHelper.cleanPath('@'+SCRIPT_DIR+os.sep+'template.sql')
    result=subprocess.call(['sqlplus','-l','-s',connectString , templateScript, oracleScript])
    if result!=0:
      self.showErrors()
      exit(1)

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
    
    schemes=configReader.getValue('SCHEMES')
    schemes=parameterHelper.getParameterValue(['-u=','--scheme=','--user='],schemes)
    configReader.failOnValueNotFound('SCHEMES',schemes,'the given scheme is not valid for this project.')

    environment=configReader.getValue('DEFAULT_ENVIRONMENT')
    environment=parameterHelper.getParameterValue(['-e=','--env='],[environment])
    projectHelper.failOnEmpty(environment,'no environment was found')
    configReader.failOnValueNotFound('ENVIRONMENTS',environment,'the given environment is not valid for this project.')
    environment=environment[0]


    for scheme in schemes:
      print "executing unit tests for scheme '"+scheme+"' in database '"+oracleSid+"' using environment '"+environment+"'"
      oracleUser=projectHelper.getOracleUser(oracleSid, scheme)
      oraclePasswd=projectHelper.getOraclePasswd(oracleSid, scheme)
      self.unittest(oracleSid,oracleUser,oraclePasswd)
      print "unit tests for scheme '"+scheme+"' executed."



