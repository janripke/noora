#!/usr/bin/env python

import core.Plugin as Plugin
import os


class UnitTestPlugin(Plugin.Plugin):
  def __init__(self):
    Plugin.Plugin.__init__(self)
    self.setType("UNITTEST")
    
    self.addParameterDefinition('database',['-s','-si','--sid'])
    self.addParameterDefinition('scheme',['-u','-sc','--scheme'])
    
  def getDescription(self):
    return "executes unit tests. Uses the noora unit test framework."


  def getUsage(self):  
    print "NoOra database installer, unittest.py."
    print self.getDescription()
    print "remarks : a unit test is always a package. "
    print "          A package containing procedures that start with T_ is considered"
    print "          as a unit test."

    print "-s= --sid=     required contains the tnsname of the database."
    print "-u= --scheme=  not required, contains the scheme of "
    print "               the unit tests to execute."


  def unittest(self, oracleSid, oracleUser, oraclePasswd, ignoreErrors):
    connector=self.getConnector()
    oracleScript=self.getScriptDir()+os.sep+'unittest.sql'
    connector.execute(oracleSid, oracleUser, oraclePasswd, oracleScript,'','',ignoreErrors)


  def execute(self, parameterHelper):
    if parameterHelper.hasParameter('-h'):
      self.getUsage()
      exit(1)    

    ignoreErrors=False  
    if  parameterHelper.hasParameter('-ignore_errors')==True:
      ignoreErrors=True      


    configReader=self.getConfigReader()
    projectHelper=self.getProjectHelper()

    oracleSid=parameterHelper.getParameterValue(['-s=','--sid='],[])
    projectHelper.failOnEmpty(oracleSid,'no oracle sid was given.')
    configReader.failOnValueNotFound('ORACLE_SIDS',oracleSid,'the given oracle sid is not valid for this project.')
    oracleSid=oracleSid[0]
    
    schemes=configReader.getValue('SCHEMES')
    schemes=parameterHelper.getParameterValue(['-u=','--scheme=','--user='],schemes)
    configReader.failOnValueNotFound('SCHEMES',schemes,'the given scheme is not valid for this project.')

    for scheme in schemes:
      print "executing unit tests for scheme '"+scheme+"' in database '"+oracleSid+"'"
      oracleUser=projectHelper.getOracleUser(oracleSid, scheme)
      oraclePasswd=projectHelper.getOraclePasswd(oracleSid, scheme)
      self.unittest(oracleSid,oracleUser,oraclePasswd,ignoreErrors)
      print "unit tests for scheme '"+scheme+"' executed."



