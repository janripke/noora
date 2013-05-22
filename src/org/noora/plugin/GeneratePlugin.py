
from org.noora.cl.Option import Option, OF_OPTIONARG, OF_SINGLE_ARG, OF_REQUIRED, \
  OF_OPTION, OF_MULTI_ARG
from org.noora.cl.Options import Options
from org.noora.config.Generator import Generator
from org.noora.helper.ProjectHelper import ProjectHelper
from org.noora.io.Directory import Directory
from org.noora.io.File import File
from org.noora.io.NoOraError import NoOraError
from org.noora.output.FileSystemOutput import FileSystemOutput
from org.noora.plugin.Plugin import Plugin
from org.noora.plugin.Pluginable import PER_CONTINUE

import os



class GeneratePlugin(Plugin):
  
  CREATE_PROJECT_DIR = 0x01     # create the project dir and the project config
  CREATE_VERSION_DIR = 0x02     # create a revision tree in the update directory
  CREATE_CREATE_DIR  = 0x04     # create a revision tree in the create directory
  USE_PROJECT_DIR    = 0x08     # use the project dir (always in combination with CREATE_VERSION_DIR)

#---------------------------------------------------------
  def __init__(self, name, application, inputObject, outputObject):
    options = Options()
    options.add(Option(None, "--project",
                       OF_OPTIONARG | OF_SINGLE_ARG,
                       "specify name of project to create", "project"))
    options.add(Option("-d", "--database",
                       OF_OPTIONARG | OF_REQUIRED | OF_SINGLE_ARG,
                       "specify the database (oracle,mysql or sqlite)", "database"))
    options.add(Option("-c", "--connectors",
                       OF_OPTIONARG | OF_MULTI_ARG,
                       "specify names of connector as comma separated list, no spaces (e.g. for oracle this would be the SID)", "c1[,c2,...]"))
    options.add(Option("-h", "--host",
                       OF_OPTIONARG | OF_SINGLE_ARG,
                       "specify database host (or ip-address)", "host"))
    options.add(Option(None, "--port",
                       OF_OPTIONARG | OF_SINGLE_ARG,
                       "specify TNS-listener port", "portnumber"))
    options.add(Option("-u", "--user",
                       OF_OPTIONARG | OF_SINGLE_ARG,
                       "specify name of user to connect to the database", "username"))
    options.add(Option(None, "--password",
                       OF_OPTIONARG | OF_SINGLE_ARG,
                       "specify the password to connect to the database", "password"))
    options.add(Option("-e", "--environments",
                       OF_OPTIONARG | OF_MULTI_ARG,
                       "specify one or more environments (comma separated, no spaces)", "env1[,env2,...]"))
    options.add(Option("-v", "--version",
                       OF_OPTION | OF_SINGLE_ARG,
                       "specify the default version of the database (x.y.z)", "version"))

    Plugin.__init__(self, name, application, inputObject, outputObject, options)
    
    self.__generator = Generator(self)

#---------------------------------------------------------
  def initialize(self):
    # overrule current output with filesystem output
    self.setOutput(FileSystemOutput(self))

#---------------------------------------------------------
  def execute(self):
    
    # cases:
    # 1. project does not exist 
    #    - create project dir and fill with 'create' and 'config' folders. Also create project-config.xml
    #      when --version is specified, then also create the update folder with that version
    # 2. project exists and no --version is specified
    #    - generate an error
    # 3. project exists and --version is specified
    #    - check version number (must be larger than highest version)
    #    - if ok, then create 'update' folder structure and update project-config.xml
    
    # note that --project always implies a chdir into the specified project, so
    # --project=abc will first chdir into 'abc' and then create either the 'create' or 'update' folder structure
    
    # generate an 'update' from within the project implies that --project cannot be specified.
    # specifying --project _and_ --version will result in an error when either project-config.xml or project.conf is present
    # in the current directory (prevents creating a project-dir within a project-dir).

    options = self.getOptions()
    project = options.getOption("--project", True)
    version = options.getOption("--version", True)
    
    try:
      workdir = Directory()   # initializes with current working directory

      action = self.__validateOptions(project, version)
      
      # at this point we're about to really do something (no exception was raised).
        
      if action & GeneratePlugin.CREATE_PROJECT_DIR:
        self.__createProject(project, workdir)

      if action & (GeneratePlugin.CREATE_PROJECT_DIR | GeneratePlugin.USE_PROJECT_DIR):
        workdir.pushDir(os.sep.join( [ workdir.getCurrentDir(), project ] ))
      
      if action & GeneratePlugin.CREATE_CREATE_DIR:
        self.__createCreateDir(workdir)
      
      if action & GeneratePlugin.CREATE_VERSION_DIR:
        self.__createUpdateDir(workdir)
      
    
    except NoOraError as e:
      raise e.addReason('plugin', "GeneratePlugin")
    finally:
      # pop without push has no effect (e.g. when generate was invoked within the project directory)
      workdir.popDir()
          
    # continue running other plugins (if any)
    return PER_CONTINUE

#---------------------------------------------------------
  def getGenerator(self):
    return self.__generator
  
#---------------------------------------------------------
  def __validateOptions(self, project, version):
    currentDirIsProject = ProjectHelper().isProjectDir(".")
    projectDirIsProject = ProjectHelper().isProjectDir(project)
    
    action = 0  # bitmap so do not initialize to None!
    
    if not project:
      # no --project specified so current dir must be a project. version is optional here
      if not currentDirIsProject:
        raise NoOraError('usermsg', "current directory is not a project directory. Please specify a project using --project=<project>")
      else:
        action |= (GeneratePlugin.CREATE_PROJECT_DIR | GeneratePlugin.CREATE_CREATE_DIR)
        if version:
          action |= GeneratePlugin.CREATE_VERSION_DIR
    else:
      if currentDirIsProject:
        raise NoOraError('usermsg', "current directory is a project, cannot create a project within a project")
      
      if projectDirIsProject:
        action |= (GeneratePlugin.USE_PROJECT_DIR | GeneratePlugin.CREATE_VERSION_DIR)
      else:
        action |= (GeneratePlugin.CREATE_PROJECT_DIR | GeneratePlugin.CREATE_CREATE_DIR)
        
      if version:
        action |= GeneratePlugin.CREATE_VERSION_DIR
     
    return action 
  
#---------------------------------------------------------
  def __createProject(self, project, workdir):
    """ Create a project with a master config file and a populated config directory.
      The project is created as ./<project>
      It does not create the 'create' or 'update' directoryies.
    
      @param project the name of the project to create
    """

    curdir = workdir.getCurrentDir()
    
    config = self.getApplication().getConfig()
    configDefinition = config.getFirstElement("config")
    
    # create project dir and go there...
    projdir = os.sep.join( [ curdir, project ])
    if not File(projdir).exists():
      os.makedirs(projdir)
    workdir.pushDir(projdir)
    
    try:
      for elem in configDefinition.findall("./*"):
        self.__processFileSystemConfigItem(elem, os.sep.join( [ curdir, project ] ))
    except NoOraError as e:
      raise e.addReason('action', "create project configuration")
    finally:
      workdir.popDir()

#---------------------------------------------------------
  def __createCreateDir(self, workdir):
    """ Generate the 'create' directory structure (revision-tree) inside the project directory.
      Note: It assumed that the current working directory already is the project directory.
    """
    
    config = self.getApplication().getConfig()
    definition = config.getFirstElement("create-tree")
    
    try:
      for elem in definition.findall("./*"):
        self.__processFileSystemConfigItem(elem, workdir.getCurrentDir())
    except NoOraError as e:
      raise e.addReason('action', "create 'create' revision tree")
      
#---------------------------------------------------------
  def __createUpdateDir(self, workdir):
    """ Generate the 'update' directory structure (revision-tree) inside the project directory.
      Note: It assumed that the current working directory already is the project directory.
    """
    
    config = self.getApplication().getConfig()
    definition = config.getFirstElement("update-tree")
    
    try:
      for elem in definition.findall("./*"):
        self.__processFileSystemConfigItem(elem, workdir.getCurrentDir())
    except NoOraError as e:
      raise e.addReason('action', "create 'create' revision tree")
    
#---------------------------------------------------------
  def __processFileSystemConfigItem(self, elem, outputLocation):
    
    name = elem.get('name')
    map = elem.get('map')
    if not name and not map:
      raise NoOraError('usermsg', "error in generate.xml, cannot create project").addReason('detail', "found folder/file element without name or map attribute")
    if name and map:
      raise NoOraError('usermsg', "error in generate.xml, cannot create project").addReason('detail', "found file/folder element with both name and map attribute. Only one of them is allowed")
    
    try:
    
    
      if name:
        value = self.__generator.getGeneratedValue(name)
        if value:
          name = value
      
      if elem.tag == 'file':
        
        # read input
        content = elem.get('content')
        if not content:
          template = elem.get('template')
          if template:
            templatedir = self.getApplication().getDirectory('TEMPLATE_DIR')
            content = self.getInput().fetchInput(templatedir, template)
          else:
            raise NoOraError('detail', "template file '{0}' not found in $NOORA_HOME/resources/templates".format(template))
        
        if not content:
          raise NoOraError('usermsg', "corrupted generate.xml, cannot find content for element {0}".format(name))
            
        # write output
        name = elem.get('name')
        if name:
          self.getOutput().write(outputLocation, name, content)
        
      elif elem.tag == 'folder':
        
        if name is not None:
          dirpath = os.sep.join( [ outputLocation, name ] )
          if not File(dirpath).exists():
            os.makedirs(dirpath)
          children = elem.findall("./*")
          for child in children:
            self.__processFileSystemConfigItem(child, dirpath)
          
        if map is not None:
          dirlist = self.__generator.getGeneratedValue(map)
          if dirlist:
            for mapelem in dirlist:
              dirpath = os.sep.join( [ outputLocation, mapelem ] )
              if not File(dirpath).exists():
                os.makedirs(dirpath)
              children = elem.findall("./*")
              for child in children:
                self.__processFileSystemConfigItem(child, dirpath)
                          
      else:
        raise NoOraError('tag', elem.tag).addReason('detail', "invalid tag found in generate.xml (can only process 'file' and 'folder' tags")

    except NoOraError as e:
      raise e.addReason('element', elem.tag).addReason('name', name if name else "unknown")
    
#---------------------------------------------------------
#---------------------------------------------------------
#---------------------------------------------------------


  # pre 1.0.0 stuff


  # def __init__(self):
  #  Plugin.Plugin.__init__(self)
  #  self.setType("GENERATE")
  #  self.setBaseDir(os.path.abspath('.'))

  #  self.addParameterDefinition('project',['-pr','--project'])
  #  self.addParameterDefinition('database',['-si','--sid'])
  #  self.addParameterDefinition('scheme',['-sc','--scheme'])
  #  self.addParameterDefinition('username',['-u','--username'])
  #  self.addParameterDefinition('password',['-p','--password'])
  #  self.addParameterDefinition('version',['-v','--version'])

  def getPluginDir(self):
    return self.getNooraDir() + os.sep + 'plugins' + os.sep + 'dynamic' + os.sep + 'generate'

  def getDescription(self):
    return "intiates a new NoOra database project, or a new release of an existing database project."


  def getUsage(self):
    print "NoOra database installer, GeneratePlugin"
    print self.getDescription()
    print "-pr= --project=   not required, contains the database project name."
    print "-si= --sid=       not required, contains the oracle sid."
    print "-sc= --scheme=    not required, contains the scheme name."
    print "-u= --username=   not required, contains the username."
    print "-p= --password=   not required, contains the password."
    print "-v= --version=    required, contains the version to create."

  def getDefaultVersion(self):
    configReader = self.getConfigReader()
    defaultVersion = configReader.getValue('DEFAULT_VERSION')
    return defaultVersion

  def getVersions(self, defaultVersion):
    projectHelper = self.getProjectHelper()
    versions = []
    alterFolder = projectHelper.getAlterFolder()
    if projectHelper.folderPresent(alterFolder):
      versions = projectHelper.findFolders(alterFolder)
    createFolder = projectHelper.getCreateFolder()
    if projectHelper.folderPresent(createFolder):
      versions.append(defaultVersion)
    # versionHelper=VersionHelper.VersionHelper(versions)
    versionHelper = None
    versions = versionHelper.sort()
    return versions


  def getSqlVersionStatement(self, versions, version):
    configReader = self.getConfigReader()
    createVersion = versions[0]
    if createVersion == version:
      stream = configReader.getValue('VERSION_INSERT_STATEMENT')
    else:
      stream = configReader.getValue('VERSION_UPDATE_STATEMENT')
      stream = stream.replace('<version>', version)
    return stream


  def getSqlEnvironmentStatement(self, environment):
    configReader = self.getConfigReader()
    stream = configReader.getValue('ENVIRONMENT_INSERT_STATEMENT')
    stream = stream.replace('<environment>', environment)
    return stream


  def execute_old(self, parameterHelper):
    if parameterHelper.hasParameter('-h'):
      self.getUsage()
      exit(1)

    projectHelper = self.getProjectHelper()

    version = parameterHelper.getParameterValue(['-v=', '--version='], [])

    if projectHelper.fileNotPresent('project.conf'):

      projectFolder = parameterHelper.getParameterValue(['-pr=', '--project='], [])
      projectHelper.failOnEmpty(projectFolder, 'no project is given, use the -pr= option')
      projectFolder = projectFolder[0]

      oracleSid = parameterHelper.getParameterValue(['-si=', '--sid='], [])
      projectHelper.failOnEmpty(oracleSid, 'no oracle sid is given, use the -si option')
      oracleSid = oracleSid[0]

      scheme = parameterHelper.getParameterValue(['-sc=', '--scheme='], [])
      projectHelper.failOnEmpty(scheme, 'no scheme is given, use the -sc option')
      scheme = scheme[0]

      oracleUser = parameterHelper.getParameterValue(['-u=', '--username='], [])
      projectHelper.failOnEmpty(oracleUser, 'no username is given, use the -u option')
      oracleUser = oracleUser[0]

      oraclePasswd = parameterHelper.getParameterValue(['-p=', '--password='], [])
      projectHelper.failOnEmpty(oraclePasswd, 'no username is given, use the -p option')
      oraclePasswd = oraclePasswd[0]

      projectHelper.failOnEmpty(version, 'no version is given, use the -v option')

      projectHelper.failOnFolderPresent(projectFolder, 'the given project is already present')

      # create the project folder
      os.makedirs(projectFolder)

      # create the project.conf file
      filename = 'project.conf'
      folder = self.getPluginDir() + os.sep + 'templates'
      sourceFile = folder + os.sep + filename
      targetFile = projectFolder + os.sep + filename
      projectHelper.copyFile(sourceFile, targetFile)
      stream = projectHelper.readFile(targetFile)
      stream = stream.replace('<SID>', oracleSid)
      stream = stream.replace('<SCHEME>', scheme)
      stream = stream.replace('<USERNAME>', oracleUser)
      stream = stream.replace('<PASSWORD>', oraclePasswd)
      stream = stream.replace('<VERSION>', version[0])
      projectHelper.writeFile(targetFile, stream)

      os.chdir(projectFolder)
      self.setBaseDir(os.path.abspath('.'))
      projectHelper.setBaseDir(os.path.abspath('.'))

      print "project " + projectFolder + " created."


    # configReader=ConfigReader.ConfigReader('project.conf')
    configReader = None
    self.setConfigReader(configReader)
    projectHelper.setConfigReader(configReader)
    # configReader=self.getConfigReader()

    schemes = configReader.getValue('SCHEMES')
    schemes = parameterHelper.getParameterValue(['-sc=', '--scheme='], schemes)
    configReader.failOnValueNotFound('SCHEMES', schemes, 'the given scheme is not valid for this project.')

    versionScheme = configReader.getValue('VERSION_SCHEME')
    projectHelper.failOnEmpty(versionScheme, 'the variable VERSION_SCHEME is not configured for this project.')

    versionInsertStatement = configReader.getValue('VERSION_INSERT_STATEMENT')
    projectHelper.failOnEmpty(versionInsertStatement, 'the variable VERSION_INSERT_STATEMENT is not configured for this project.')

    versionUpdateStatement = configReader.getValue('VERSION_UPDATE_STATEMENT')
    projectHelper.failOnEmpty(versionUpdateStatement, 'the variable VERSION_UPDATE_STATEMENT is not configured for this project.')

    environments = configReader.getValue('ENVIRONMENTS')
    projectHelper.failOnEmpty(environments, 'the variable ENVIRONMENTS is not configured for this project.')

    defaultVersion = self.getDefaultVersion()
    projectHelper.failOnEmpty(defaultVersion, 'the variable DEFAULT_VERSION is not configured for this project.')


    # find the versions
    versions = self.getVersions(defaultVersion)

    if len(version) == 0:
      # versionHelper=VersionHelper.VersionHelper(versions)
      versionHelper = None
      version.append(versionHelper.getNextRevision(defaultVersion))

    version = version[0]

    if len(versions) == 0:
      versions.append(defaultVersion)


    versionFolder = projectHelper.getBuildFolder(versions, version)
    projectHelper.failOnFolderPresent(versionFolder, 'the given version is already present')

    objects = configReader.getValue('CREATE_OBJECTS')
    projectHelper.failOnNone(objects, 'the variable CREATE_OBJECTS is not configured for this project.')

    # create the version folder
    os.makedirs(versionFolder)

    for scheme in schemes:

      # create the scheme folder
      schemeFolder = versionFolder + os.sep + scheme
      os.mkdir(schemeFolder)

      # create the dat folder
      datFolder = schemeFolder + os.sep + 'dat'
      os.mkdir(datFolder)

      # create the version script in the dat folder
      if scheme == versionScheme:
        sqlScript = self.getSqlVersionStatement(versions, version)
        projectHelper.writeFile(datFolder + os.sep + 'version.sql', sqlScript)

      # create the environment folders in the dat folder
      for environment in environments:
        os.mkdir(datFolder + os.sep + environment)

        # create the environment script in the dat folder.
        if scheme == versionScheme and versions[0] == version:
          sqlScript = self.getSqlEnvironmentStatement(environment)
          projectHelper.writeFile(datFolder + os.sep + environment + os.sep + 'environment.sql', sqlScript)


      # create the ddl folder
      ddlFolder = schemeFolder + os.sep + 'ddl'
      os.mkdir(ddlFolder)

      # create the object folders in the ddl folder
      for object in objects:
        os.mkdir(ddlFolder + os.sep + object)

      # create the template code on create.
      if scheme == versionScheme and versions[0] == version:

        files = projectHelper.findFiles(folder)
        for object in objects:
          folder = self.getPluginDir() + os.sep + 'templates' + os.sep + object
          if projectHelper.folderPresent(folder):
            files = projectHelper.findFiles(folder)
            for file in files:
              sourceFile = folder + os.sep + file
              targetFile = ddlFolder + os.sep + object + os.sep + file
              projectHelper.copyFile(sourceFile, targetFile)

    print "version " + version + " created."

