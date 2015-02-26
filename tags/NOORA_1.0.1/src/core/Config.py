import os.path

import core.config.ConfigReaderXML
import core.config.ConfigReaderProperty

CONFIG_TYPE_UNKNOWN = 1
CONFIG_TYPE_PROPERTY = 2
CONFIG_TYPE_XML = 3

CONFIG_FILE_PROPERTY = "project.conf"
CONFIG_FILE_XML = "project-config.xml"

CONFIG_STATUS_OK = 1
CONFIG_STATUS_ERROR = 2

# do not change config-file type 
CONFIG_POLICY_UNCHANGED = 1
# upgrade project.conf to project-config.xml
CONFIG_POLICY_UPGRADE = 2
# downgrade project-config.xml to project.conf
CONFIG_POLICY_DOWNGRADE = 3

class Config:

    def __init__(self, projectdir):
        self.__projectdir = projectdir
        self.__configFile, self.__configType = self.__getConfigFileInfo()

        confFile = "%s%c%s" % (self.__projectdir, os.path.sep, self.__configFile)

        if self.__configType == CONFIG_TYPE_XML:
            self.__configReader = core.config.ConfigReaderXML(confFile)
        if self.__configType == CONFIG_TYPE_PROPERTY:
            self.__configReader = core.config.ConfigReaderProperty(confFile)
        if self.__configType == CONFIG_TYPE_UNKNOWN:
            self.status = CONFIG_STATUS_ERROR
            return

        self.status = CONFIG_STATUS_OK

    def load(self):
        if self.__status == CONFIG_STATUS_OK:
            self.__configReader.load()

    def __getConfigFileInfo(self):
        if self.__hasConfigFile(CONFIG_FILE_XML) == True:
            return (CONFIG_FILE_XML, CONFIG_TYPE_XML);
        if self.__hasConfigFile(CONFIG_FILE_PROPERTY) == True:
            return (CONFIG_FILE_PROPERTY, CONFIG_TYPE_PROPERTY);
        return (None, CONFIG_TYPE_UNKNOWN)

    def __hasConfigFile(self, configFile):
        if (os.path.exists(configFile) and os.path.isfile(self.configFile)):
            return True
        return False
