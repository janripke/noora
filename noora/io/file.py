import os


class File(object):
    """
    File management functionality. Initialize a file object with its path (url).
    """
    def __init__(self, url=None):
        """Initialize the file path"""
        self.__url = url

    def get_url(self):
        """Return the path to the file"""
        return self.__url

    def is_file(self):
        """
        Returns True if url points to a file, false if not (e.g. when the
        file is a directory).
        """
        url = self.get_url()
        return os.path.isfile(url)

    def is_dir(self):
        """
        Returns True if url points to a directory, False otherwise.
        """
        url = self.get_url()
        return os.path.isdir(url)

    def tail(self):
        """
        Returns the tail part after splitting the File's url.
        """
        url = self.get_url()
        head, tail = os.path.split(url)
        return tail

    def head(self):
        """
        Returns the head part after splitting the File's url.
        """
        url = self.get_url()
        head, tail = os.path.split(url)
        return head

    def extension(self):
        """
        Get the file's extension
        """
        url = self.get_url()
        filename, extension = os.path.splitext(url)
        return extension

    def exists(self):
        """
        Check if the file exists.
        """
        if self.is_file():
            return True
        if self.is_dir():
            return True
        return False
