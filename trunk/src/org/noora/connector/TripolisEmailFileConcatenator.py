import os

from org.noora.io.File import File
from org.noora.io.FileReader import FileReader


class TripolisEmailFileConcatenator:

    """
    ctrlfile is of type org.noora.io.File, and has extension .py
    It concatenates a py, html and txt file and returns Python code, which can be used by TripolisDirectEmail
    """
    @staticmethod
    def toPython(ctrlfile):
        root = ctrlfile.getRoot()
        htmlfile = File("%s.%s" % (root, 'html'))
        textfile = File("%s.%s" % (root, 'txt'))
        try:
            ctrl = FileReader(ctrlfile).read()
            html = FileReader(htmlfile).read()
            text = FileReader(textfile).read()
            return "%s%shtml=\"\"\"%s\"\"\"%stext=\"\"\"%s\"\"\"" % (ctrl, os.linesep, html, os.linesep, text)
        except (OSError, IOError) as e:
            raise "Reading one of files %s.(py|html|txt) failed: %s" % (root, e)