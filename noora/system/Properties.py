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

        self.update_config()

    def __get_config(self):
        """
        Load a myproject.json file and update some extra parameters if this is an actual project
        """
        current_dir = self.__props.get("current.dir")
        project_file = self.__props.get("project.file")

        config_file = File(os.path.join(current_dir, project_file))
        if not config_file.exists():
            noora_dir = self.__props.get("noora.dir")
            config_file = File(os.path.join(noora_dir, project_file))

        # Read project configuration
        with open(config_file.get_url()) as fd:
            data = json.load(fd)

        return data

    def update_config(self):
        """
        Update the project configuration
        """
        # Get the configuration and merge it into the properties
        self.__props.update(self.__get_config())

        # If this is an actual project, update some other properties
        if 'project' in self:
            self['alter.dir'] = os.path.join(self['current.dir'], 'alter')
            self['create.dir'] = os.path.join(self['current.dir'], 'create')

            # Guess the database technology if not present
            if 'technology' not in self:
                self['technology'] = self['plugins'][0].split(".")[2]

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

    def keys(self):
        return self.__props.keys()
