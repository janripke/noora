#!/usr/bin/env python
import os
from noora.io.File import File
from noora.system.ClassLoader import ClassLoader


class App:
    def __init__(self):
        pass

    @staticmethod
    def get_config_file(properties):
        current_dir = properties.get("current.dir")
        project_file = properties.get("project.file")

        f = File(os.path.join(current_dir, project_file))
        if f.exists():
            return f

        noora_dir = properties.get("noora.dir")
        f = File(os.path.join(noora_dir, project_file))
        return f

    @staticmethod
    def find_plugin(command, properties):
        plugins = properties.get('plugins')
        for plugin in plugins:
            p = ClassLoader.find(plugin)
            if command.lower() == p.get_type().lower():
                return p

    @staticmethod
    def build_dir(version, properties):
        if version == properties.get("default_version"):
            return properties.get("create.dir")
        return os.path.join(properties.get("alter.dir"), version)
