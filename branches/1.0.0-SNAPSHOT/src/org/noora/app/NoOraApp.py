
from org.noora.app.Params import Params, PluginParameter
from org.noora.cl.Option import Option, OF_OPTIONARG, OF_SINGLE_ARG
from org.noora.cl.Options import Options
from org.noora.classloader.ClassLoader import ClassLoader
from org.noora.classloader.ClassLoaderException import ClassLoaderException
from org.noora.config.Config import Config
from org.noora.input.FileSystemInput import FileSystemInput
from org.noora.io.Directory import Directory
from org.noora.io.File import File
from org.noora.io.NoOraError import NoOraError
from org.noora.output.ConsoleOutput import ConsoleOutput
from org.noora.plugin.Pluginable import PER_EXIT

import logging.handlers
import os



class NoOraApp(object):
  """ Application object that centralizes NoOra functionality.
    1. It initializes the log, reads the config, loads the plugins and processes command line arguments.
    2. It executes the plugins that were specified (command line arguments)
    3. Terminates all plugins that were initialized.
    
    It is also the central access point to the applications data (directories, config data, loaded plugins).
  """

#---------------------------------------------------------
  def __init__(self, params):
    
    ## @var __parameters
    # @brief 'preprocessed' command line arguments. Note that these are not part of the 'cl' Options. 
    #        They are however used to provide the Option objects with values.
    self.__parameters = Params(params[1:])

    noora_dir = os.path.abspath(os.path.dirname(params[0]))
    project_dir = os.path.abspath(".")

    ## @var __directories
    # @brief Map of often used directory paths
    #        Values: NOORA_DIR, INVOCATION_DIR, RESOURCE_DIR, TEMPLATE_DIR
    self.__directories = { 'NOORA_DIR'     : noora_dir,
                           'INVOCATION_DIR': project_dir,
                           'RESOURCE_DIR'  : os.sep.join([ noora_dir, 'resources']),
                           'TEMPLATE_DIR'  : os.sep.join([ noora_dir, 'resources', 'templates' ])
                         }
    
    ## @var __config
    # @brief configuration object, contains one ore more processed configuration files
    self.__config = Config();
    
    ## @var __plugins
    # @brief List of loaded plugins (as specified on the command line).
    self.__plugins = []
    
    ## @var __defines
    # @brief List of -D <name>=<value> command line options.
    self.__defines = Options();
    
    ## @var __console
    # @brief device that acts as console for runtime output.
    self.__console = ConsoleOutput()
    
    ## @var __logger
    # @brief Logger to be used
    self.__logger = None

#---------------------------------------------------------
  def initialize(self):
    """ Initializes the NoOra application object.
      Initializes the log, reads the config, loads the plugins and processes command-line arguments
      @raise NoOraError: some initialization error occurred
    """
    self.__initLog()
    self.__readConfig()
    self.__loadPlugins()
    self.__parseParameters()

    for plugin in self.__plugins:
      plugin.initialize()

#---------------------------------------------------------
  def terminate(self):
    """ Terminates the loaded plugins
    """
    for plugin in self.__plugins:
      plugin.terminate()

#---------------------------------------------------------
  def run(self):
    """ Executes the loaded plugins.
      Before execution, each plugin loads its configuration file. 
      When the plugin returns PER_EXIT then the execution is stopped, otherwise the next plugin in the list is executed.
    """
    for plugin in self.__plugins:
      plugin.readConfig()
      if plugin.execute() == PER_EXIT:
        break
      plugin.popConfig()

#---------------------------------------------------------
  def getDirectory(self, name):
    return self.__directories[name]

#---------------------------------------------------------
  def getPlugins(self):
    return self.__plugins

#---------------------------------------------------------
  def getConfig(self):
    return self.__config

#---------------------------------------------------------
  def getOptionValue(self, name):
    """ Gets either the value for a -D<name>=<value> command line arg, the value of environment variable or /project/defaults/<name> from the config
      The environment variable must be called 'NOORA_<name>'
      The order of fetching is: command line option, environment variable, project config defaults
      @param: name the name of the option to retrieve
      @return: returns the value found or None when not found
    """

    # look for command line argument
    value = self.__defines.getOption(name, True)
    if value is None:
      value = self.__getEnvironmentValue(name)
    if value is None:
      value = self.__getProjectDefaultValue(name)
      
    return value

#---------------------------------------------------------
# logger methods
#---------------------------------------------------------
  @classmethod
  def error(cls, message):
    cls.__logger.error(message)
    
  @classmethod
  def warning(cls, message):
    cls.__logger.warning(message)
    
#---------------------------------------------------------
# Private methods
#---------------------------------------------------------
  def __initLog(self):

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    
    handler = logging.handlers.RotatingFileHandler('noora.log', 'a', 0, 5)
    handler.setFormatter(formatter)
    
    self.__logger = logging.getLogger('NoOraLogger')
    self.__logger.addHandler(handler)         
    handler.doRollover()        
    self.__logger.setLevel(logging.ERROR)

#---------------------------------------------------------
  def __parseParameters(self):

    # set plugin's Options using the NoOraApp's Params.
    for plugin in self.__plugins:
      try:
        options = plugin.getOptions()
        options.setOptionValues(self.__parameters)
        options.checkRequiredOptions()
      except NoOraError as e:
        raise e.addReason('plugin', plugin.getName())

    # any parameter that is not 'processed' by a plugin is marked 'unused'
    unusedParams = [ ]
    for param in self.__parameters.getParams():
      if not isinstance(param, PluginParameter):
        if not param.isUsed():
          unusedParams.append(param)

    # report unused parameters unless the parameter is '-D'
    # In that case, add the -D to self.__defines
    for param in unusedParams:
      name = param.getName()
      if name == "-D":
        value = param.getValue()
        if value:
          values = value.split("=")
          if len(values) == 2:
            option = Option(values[0], values[0], OF_OPTIONARG | OF_SINGLE_ARG, "", "");
            option.setValues([ values[1] ])
            self.__defines.add(option)
            continue
      print "warning: unknown parameter {0}".format(param.getName())

#---------------------------------------------------------
  def __readConfig(self):
    """
      reads the config file (pushes on config stack). First it attempts 'project-config.xml' and if that file does not exist it will try 'project.conf'.
      It raises a NoOraError when none of the two config files is found.

      @throws NoOraError('usermsg')
    """

    hasNoOraConfig = False

    # first read noora 'system config'
    directory = Directory()
    directory.pushDir(self.__directories['RESOURCE_DIR'])

    sysconfig = os.sep.join([ self.__directories['RESOURCE_DIR'], "noora-config.xml" ])
    xmlconfig = File(sysconfig)
    if xmlconfig.exists():
      self.__config.pushConfig(sysconfig)
      hasNoOraConfig = True

    directory.popDir()

    # now read project config

    xmlconfig = File("project-config.xml")
    if xmlconfig.exists():
      self.__config.pushConfig("project-config.xml")
      return

    propconf = File("project.conf")
    if propconf.exists():
      self.__config.pushConfig("project.conf")
      return

    if not hasNoOraConfig:
      raise NoOraError('usermsg', 'no configuration file found in project dir (project-config.xml or project.conf)')

#---------------------------------------------------------

  def __loadPlugins(self):
    """ Load the specified plugins using the ClassLoader.
      The plugin class is taken from the config (plugins/plugin[@name=<plugin-name>]/class)
      The order of the plugins is stored as specified by plugins/plugin[@name]/priority where lowest means first and highest means last.
    """
    
    loader = ClassLoader()

    try:
      plugins = self.__parameters.getPluginParams()
      for plugin in plugins:
        pluginConfig = self.__config.getElement("plugins/plugin[@name='{0}']".format(plugin.getName()))
        if not pluginConfig or len(pluginConfig) < 1:
          raise NoOraError('usermsg', "unknown command {0}".format(plugin.getName()))

        className = pluginConfig[0].findtext('class')
        if not className:
          raise NoOraError('detail', "invalid plugin config for {0}, no 'class' tag present".format(plugin.getName()))

        inp = self.__getDefaultInput()
        outp = self.__getDefaultOutput()
        plugin = loader.findByPattern(className, [ plugin.getName(), self, inp, outp ])

        execPrio = pluginConfig[0].findtext("priority")
        if execPrio:
          plugin.setExecutionPriority(execPrio)

        self.__plugins.append(plugin)

      # now sort them by priority
      self.__plugins.sort(key = lambda x: x.getExecutionPriority(), reverse = False)

    except ClassLoaderException as e:
      raise NoOraError('detail', e.getMessage())

#---------------------------------------------------------
  def __getProjectDefaultValue(self, name):
    """ Get default value from config
      Each of the config files is queried for <root>/defaults/<name> and <root>/defaults/lists/list[@name='<name>'].
      In case of a list, the element list is converted to a list of strings
    """
    value = self.getConfig().getProperty("defaults/{0}".format(name))
    if value is not None:
      return value
    
    list = self.getConfig().getElement("defaults/lists/list[@name='{0}']/item".format(name))
    if list is not None and len(list) > 0:
      result = []
      for elem in list:
        result.append(elem.text)
      return result
    
    return None
  
#---------------------------------------------------------
  def __getEnvironmentValue(self, name):
    """ Get environment variable
    Note that the environment variable name should be 'NOORA_<name>'
    """
    envname = 'NOORA_' + name
    value = os.environ.get(envname)
    return value

#---------------------------------------------------------
  def __getDefaultInput(self):
    return FileSystemInput()

#---------------------------------------------------------
  def __getDefaultOutput(self):
    return ConsoleOutput()
