
import core.config.ConfigReader as ConfigReader
from xml.etree.ElementTree import ElementTree

class ConfigReaderXML(ConfigReader):

    def __init__(self, filename):
        ConfigReader.ConfigReader.__init__(self, filename)

    def load(self):
        self.__tree = ElementTree()
        self.__tree.parse(self.__filename)
        if self.__tree == None:
            self.__status = ConfigReader.CR_STATUS_ERROR
            self.__message = "Invalid xml file"
