
import core.config.ConfigReader
import core.NooraException as NooraException
import core.StreamHelper as StreamHelper

M_LF = chr(10)

class ConfigReaderProperty(core.config.ConfigReader):
    '''
    The original config (property based) reader
    '''

    def __init__(self, filename):
        core.config.ConfigReader.ConfigReader.__init__(self, filename)

        self.__lines = []
        self.__message = None
        self.__filename = filename
        self.loadFromFile(filename)

    def parse(self, stream):
        stream = StreamHelper.StreamHelper().convert(stream)
        lines = stream.split(chr(10))
        for line in lines:
            self.__lines.append(line)

    def loadFromFile(self, filename):
        try:
            handle = open(filename, 'r')
            stream = handle.read()
            handle.close()
            self.parse(stream)
        except IOError:
            self.setMessage('project configuration file "' + filename + '" not found.')

    def loadFromStream(self, stream):
        self.parse(stream)

    def saveToFile(self, filename):
        stream = M_LF.join(self.__lines)
        handle = open(filename, 'w')
        handle.write(stream)
        handle.close()

    def getValue(self, keyword):
        lines = self.__lines
        for line in lines:
            if line.startswith(keyword):
                values = line.split('=')[1::]
                value = '='.join(values)
                return eval(value)
        return None

    def setValue(self, keyword, value):
        lines = self.__lines
        for line in lines:
            if line.startswith(keyword):
                newLine = keyword + '=' + str(value)
                lines[lines.index(line)] = newLine


    def hasValue(self, keyword, value):
        values = self.getValue(keyword)
        if values != None:
            for val in values:
                if val.lower() == value.lower():
                    return True
        return False

  # deprecated, use failOnValueNotFound instead.
    def invalidValue(self, keyword, values):
        for value in values:
            if self.hasValue(keyword, value) == False:
                raise NooraException.NooraException("the given value " + value + " for keyword " + keyword + " is not valid for this project.")

    def failOnValueNotFound(self, keyword, values, message):
        for value in values:
            if self.hasValue(keyword, value) == False:
                raise NooraException.NooraException(message)

    def failOnValueFound(self, keyword, values, message):
        for value in values:
            if self.hasValue(keyword, value) == True:
                raise NooraException.NooraException(message)

    def failOnConfigNotLoaded(self):
        if self.getMessage() != None:
            print self.getMessage()
            exit(1)


    def setMessage(self, message):
        self.__message = message

    def getMessage(self):
        return self.__message

    def getLines(self):
        return self.__lines

    def getFilename(self):
        return self.__filename

