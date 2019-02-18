from xml.etree.ElementTree import ElementTree

import core.config.ConfigReader as ConfigReader


class ConfigReaderXML(ConfigReader):
    def load(self):
        self.__tree = ElementTree()
        self.__tree.parse(self.__filename)
        if self.__tree == None:
            self.__status = ConfigReader.CR_STATUS_ERROR
            self.__message = "Invalid xml file"
