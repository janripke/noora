from noora.io.Filterable import Filterable


class FileExtensionFilter(Filterable):
    def __init__(self, file):
        Filterable.__init__(self)
        self.__file = file

    def get_file(self):
        return self.__file

    def accept(self, fileable):
        file = self.get_file()

        if fileable.extension() == file.extension():
            return True
        return False
