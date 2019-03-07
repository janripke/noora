import os
from os.path import expanduser
import json

import noora
from noora.io.File import File


class Properties(object):
    """
    The properties object analyzes the environment and looks for project
    settings. The properties instance emulates the dict type.
    """
    def __init__(self):
        noora_dir = os.path.dirname(noora.__file__)
        current_dir = os.path.abspath('.')

        self.__props = {
            "noora.dir": noora_dir,
            "current.dir": current_dir,
            "plugin.dir": os.path.join(noora_dir, 'plugins'),
            "project.file": "myproject.json",
            'home.dir': expanduser('~'),
        }

        # Get the configuration and merge it into the properties
        self.__props.update(self.__get_config())

    def __get_config(self):
        current_dir = self.__props.get("current.dir")
        project_file = self.__props.get("project.file")

        f = File(os.path.join(current_dir, project_file))
        if f.exists():
            return f

        noora_dir = self.__props.get("noora.dir")
        config_file = File(os.path.join(noora_dir, project_file))

        with open(config_file.get_url()) as fd:
            data = json.load(fd)
        return data

    def __getitem__(self, item):
        # Do not catch exceptions here, but upstream
        return self.__props[item]

    def get(self, item, default=None):
        try:
            return self.__getitem__(item)
        except KeyError:
            return default

    def __setitem__(self, key, value):
        self.__props[key] = value

    def __delitem__(self, key):
        del self.__props[key]

    def __contains__(self, item):
        return item in self.__props


# Initialize the properties so it can be imported project-wide
properties = Properties()
