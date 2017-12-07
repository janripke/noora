import os


class File:
    def __init__(self, url=None):
        self.__url = url

    def get_url(self):
        return self.__url

    def is_file(self):
        url = self.get_url()
        return os.path.isfile(url)

    def is_dir(self):
        url = self.get_url()
        return os.path.isdir(url)

    def tail(self):
        url = self.get_url()
        head, tail = os.path.split(url)
        return tail

    def head(self):
        url = self.get_url()
        head, tail = os.path.split(url)
        return head

    def extension(self):
        url = self.get_url()
        filename, extension = os.path.splitext(url)
        return extension

    def exists(self):
        if self.is_file():
            return True
        if self.is_dir():
            return True
        return False
