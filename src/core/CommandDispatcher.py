import core.ConfigReader
import core.ParameterHelper
import os

class CommandDispatcher:
    '''
    This class will invoke the specified command. It will read the project configuration and
    use the specified arguments to dispatch the correct command.
    '''
    
    def setParameters(self,params):
        self.__parameterHelper = core.ParameterHelper.ParameterHelper()
        # clear parameters from params that are set in the constructor
        self.__parameterHelper.clearParameters()
        self.__parameterHelper.setParameters(params)
        
    def __init__(self,projectDir):
        
        self.__projectDir = projectDir
        self.__configFile = projectDir + os.sep + 'project.conf'
        os.chdir (self.__projectDir)
        
        self.__config = core.ConfigReader.ConfigReader(self.__configFile)
        