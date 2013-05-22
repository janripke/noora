from org.noora.cl.Option import Option, OF_OPTIONARG, OF_SINGLE_ARG, \
  OF_MULTI_ARG, OF_OPTION, OF_REQUIRED
from org.noora.cl.Options import Options
from org.noora.config.Generator import Generator
from org.noora.plugin.Plugin import Plugin
import core.NooraException as NooraException
import os
import subprocess


class CreatePlugin(Plugin):

  def __init__(self, name, application, inputObject, outputObject):
    
    options = Options()
    options.add(Option("-c", "--connectors",
                       OF_OPTIONARG | OF_MULTI_ARG | OF_REQUIRED,
                       "specify name of one or more connectors (comma seperated)", "connector1[,connector2,...]"))
    options.add(Option("-e", "--environment",
                       OF_OPTIONARG | OF_SINGLE_ARG,
                       "specify the environment to create", "environment"))
    options.add(Option("-v", "--version",
                       OF_OPTION | OF_SINGLE_ARG,
                       "specify the version upto which to create the update trees (x.y.z)", "version"))
    options.add(Option(None, "--nocompile",
                       OF_OPTION | OF_SINGLE_ARG,
                       "disable the compilation of packages, triggers and views.", None))
    options.add(Option(None, "--ignore-errors",
                       OF_OPTION | OF_SINGLE_ARG,
                       "disable the compilation of packages, triggers and views.", None))
    options.add(Option("-n", "--no-action",
                       OF_OPTION | OF_SINGLE_ARG,
                       "Do not perform database actions, show actions only.", None))

    Plugin.__init__(self, name, application, inputObject, outputObject, options)
    
    self.__generator = Generator(self)
  
#---------------------------------------------------------
  def initialize(self):
    pass
  
#---------------------------------------------------------
  def terminate(self):
    pass
        
#---------------------------------------------------------
  def execute(self):
    
    connectors = self.getOptionValue("connectors")
    createObjects = self.__generator.getGeneratedValue("list:create-objects")
    
    projectdir = self.getApplication().getDirectory("INVOKATION_DIR")

    for connector in connectors:
      print "creating scheme '"+connector+"' in database '"+connector+"' using environment '"+connector+"'"
      
      ddlDir = os.sep.join([projectdir, connector, 'ddl'])
      datDir = os.sep.join([projectdir, connector, 'dat'])
      
      for obj in createObjects: 
        objdir = os.sep.join([ddlDir, obj])
        
      
  
#---------------------------------------------------------
  def setSqlLoaderConnector(self, connector):
    self.__sqlLoaderConnector = connector
  
  def getSqlLoaderConnector(self):
    return self.__sqlLoaderConnector

  def getDescription(self):
    return "executes the defined baseline scripts in the create folder."

  def getUsage(self):  
    print "NoOra database installer, create.py"
    print self.getDescription()
    print "-s= --sid=     required contains the tnsname of the database."
    print "-u= --scheme=  not required, contains the scheme of "
    print "               the database objects to drop."
    print "-e= --env=     not required, used for mapping "
    print "               the username and password."
    print "-nocompile     not required, disable the compilation of "
    print "               packages, triggers and views."

  
  def getCreateDir(self):
    return self.getBaseDir()+os.sep+'create'


  def installComponent(self, url, oracleSid, oracleUser, oraclePasswd):
    projectHelper=self.getProjectHelper()
    handle=open('feedback.log','wb')
    result=subprocess.call(['python',url+os.sep+'setup.py','-s='+oracleSid,'-u='+oracleUser,'-p='+oraclePasswd,'-silent'],shell=False,stdout=handle,stderr=handle)
    if result!=0:
      stream=projectHelper.readFile('feedback.log')
      raise NooraException.NooraException(stream)


  def installFiles(self, folder, oracleSid, oracleUser, oraclePasswd, ignoreErrors):
    connector=self.getConnector()
    projectHelper=self.getProjectHelper()
    files=projectHelper.findFiles(folder)
    for file in files:
      url=folder+os.sep+file
      print url.split(self.getBaseDir())[1]
      if projectHelper.getFileExtension(file).lower()=='zip':
        projectHelper.extractFile(url)
        extractFolder=projectHelper.getFileRoot(url)
        self.installComponent(extractFolder,oracleSid,oracleUser,oraclePasswd)
        projectHelper.removeFolderRecursive(extractFolder)
      elif projectHelper.getFileExtension(file).lower()=='mdl':
        pass
      else:
        connector.execute(oracleSid, oracleUser, oraclePasswd, url, '', '', ignoreErrors)  


  def loadFiles(self, folder, oracleSid, oracleUser, oraclePasswd, ctlFile, ignoreErrors):   
    connector=self.getSqlLoaderConnector()
    projectHelper=self.getProjectHelper() 
    
    files=projectHelper.findFiles(folder)
    for file in files:
      url=folder+os.sep+file
      print url.split(self.getBaseDir())[1]
      if projectHelper.getFileExtension(file).lower()=='zip':
        projectHelper.extractFile(url,projectHelper.getFileRoot(file))
        
        for extractedFile in projectHelper.findFiles(folder+os.sep+projectHelper.getFileRoot(file)):
          connector.execute(oracleSid, oracleUser, oraclePasswd, ctlFile, extractedFile, ignoreErrors)
        projectHelper.removeFolderRecursive(folder+os.sep+projectHelper.getFileRoot(file))
      elif projectHelper.getFileExtension(file).lower()=='mdl':
        pass
      else:
        connector.execute(oracleSid, oracleUser, oraclePasswd, ctlFile, file, ignoreErrors)  



  def recompile(self, oracleSid, oracleUser, oraclePasswd, ignoreErrors):
    connector=self.getConnector()
    oracleScript=self.getScriptDir()+os.sep+'recompile.sql'
    connector.execute(oracleSid, oracleUser, oraclePasswd, oracleScript, '', '', ignoreErrors)
    

  def execute_v07(self, parameterHelper):

    ignoreErrors=False  
    if  parameterHelper.hasParameter('-ignore_errors')==True:
      ignoreErrors=True
    print ignoreErrors      

    configReader=self.getConfigReader()
    projectHelper=self.getProjectHelper()

    oracleSid=parameterHelper.getParameterValue(['-s=','--sid='],[])
    projectHelper.failOnEmpty(oracleSid,'no oracle sid was given.')
    configReader.failOnValueNotFound('ORACLE_SIDS',oracleSid,'the given oracle sid is not valid for this project.')
    oracleSid=oracleSid[0]
    
    schemes=configReader.getValue('SCHEMES')
    projectHelper.failOnNone(schemes,'the variable SCHEMES is not set.')
    schemes=parameterHelper.getParameterValue(['-u=','--scheme=','--user='],schemes)
    configReader.failOnValueNotFound('SCHEMES',schemes,'the given scheme is not valid for this project.')

    environment=configReader.getValue('DEFAULT_ENVIRONMENT')
    environment=parameterHelper.getParameterValue(['-e=','--env='],[environment])
    projectHelper.failOnEmpty(environment,'no environment was found')
    configReader.failOnValueNotFound('ENVIRONMENTS',environment,'the given environment is not valid for this project.')
    environment=environment[0]

    objects = configReader.getValue('CREATE_OBJECTS')
    projectHelper.failOnNone(objects,'the variable CREATE_OBJECTS is not set.')
    projectHelper.failOnEmpty(objects,'the variable CREATE_OBJECTS is not set.')

    for scheme in schemes:
      print "creating scheme '"+scheme+"' in database '"+oracleSid+"' using environment '"+environment+"'"
      oracleUser=projectHelper.getOracleUser(oracleSid, scheme)
      oraclePasswd=projectHelper.getOraclePasswd(oracleSid, scheme)
 
      for object in objects:  

        # global ddl objects
        folder=self.getCreateDir()+os.sep+scheme+os.sep+'ddl'+os.sep+object
        if projectHelper.folderPresent(folder):
          self.installFiles(folder, oracleSid, oracleUser, oraclePasswd, ignoreErrors)

        # environment specific ddl objects
        folder=self.getCreateDir()+os.sep+scheme+os.sep+'ddl'+os.sep+object+os.sep+environment
        if projectHelper.folderPresent(folder):
          self.installFiles(folder, oracleSid, oracleUser, oraclePasswd, ignoreErrors)

      # global dat objects
      folder=self.getCreateDir()+os.sep+scheme+os.sep+'dat'
      if projectHelper.folderPresent(folder):
        self.installFiles(folder, oracleSid, oracleUser, oraclePasswd, ignoreErrors)

      # environment specific dat objects
      folder=self.getCreateDir()+os.sep+scheme+os.sep+'dat'+os.sep+environment
      if projectHelper.folderPresent(folder):
        self.installFiles(folder, oracleSid, oracleUser, oraclePasswd, ignoreErrors)
        
      # global sqlldr files
      folder=self.getCreateDir()+os.sep+scheme+os.sep+'sqlldr'
      if projectHelper.folderPresent(folder):
        ctlFolders = projectHelper.findFolders(folder)
        for ctlFolder in ctlFolders:
          ctlFile = folder+os.sep+ctlFolder + ".ctl"
          self.loadFiles(folder+os.sep+ctlFolder, oracleSid, oracleUser, oraclePasswd, ctlFile, ignoreErrors)


      # environment sqlldr files
      folder=self.getCreateDir()+os.sep+scheme+os.sep+'sqlldr'
      if projectHelper.folderPresent(folder):
        ctlFolders = projectHelper.findFolders(folder)
        for ctlFolder in ctlFolders:
          ctlFile = folder+os.sep+ctlFolder + ".ctl"
          envFolder=folder + os.sep + ctlFolder + os.sep + environment
          if projectHelper.folderPresent(envFolder):          
            self.loadFiles(envFolder, oracleSid, oracleUser, oraclePasswd, ctlFile, ignoreErrors)

          
    
      print "scheme '"+scheme+"' created."

    if  parameterHelper.hasParameter('-nocompile')==False:
      for scheme in schemes:
        print "compiling scheme '"+scheme+"' in database '"+oracleSid+"' using environment '"+environment+"'"
        oracleUser=projectHelper.getOracleUser(oracleSid, scheme)
        oraclePasswd=projectHelper.getOraclePasswd(oracleSid, scheme)
        self.recompile(oracleSid,oracleUser,oraclePasswd, ignoreErrors)
        print "scheme '"+scheme+"' compiled."
