#!/usr/bin/env python
import os
from noora.io.File import File
from noora.system.ClassLoader import ClassLoader


class App:
    def __init__(self):
        pass

    @staticmethod
    def get_config_file(properties):
        current_dir = properties.get_property("current.dir")
        project_file = properties.get_property("project.file")

        f = File(os.path.join(current_dir, project_file))
        if f.exists():
            return f

        noora_dir = properties.get_property("noora.dir")
        f = File(os.path.join(noora_dir, project_file))
        return f

    @staticmethod
    def find_plugin(command, properties):
        plugins = properties.get_property('plugins')
        for plugin in plugins:
            p = ClassLoader.find(plugin)
            if command.lower() == p.get_type().lower():
                return p


