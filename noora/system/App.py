import os
from os.path import expanduser
import argparse
import json

import noora
from noora.io.File import File
from noora.system.ClassLoader import ClassLoader


class App(object):
    def __init__(self):
        pass

    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser(
            description="mynoora, a sql deployment tool", add_help=False)
        parser.add_argument("commands", help="command to execute", type=str, nargs='+')
        parser.add_argument('-r', action='store_true', help='show the revision', required=False)
        return parser

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
    def properties():
        noora_dir = os.path.dirname(noora.__file__)
        current_dir = os.path.abspath('.')

        properties = dict()
        properties["noora.dir"] = noora_dir
        properties["current.dir"] = current_dir
        properties["plugin.dir"] = os.path.join(noora_dir, 'plugins')
        properties["project.file"] = "myproject.json"
        properties['home.dir'] = expanduser('~')
        return properties

    @staticmethod
    def load_properties(properties):
        f = App.get_config_file(properties)
        f = open(f.get_url())

        data = json.load(f)
        for key in data.keys():
            properties[key] = data[key]
        f.close()

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
