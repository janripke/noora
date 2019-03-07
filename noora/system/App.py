import os
from importlib import import_module

import click

from noora.system.ClassLoader import ClassLoader
from noora.system.Properties import properties


class App(click.MultiCommand):
    def list_commands(self, ctx):
        """
        Get the commands based on the context. If 'project' is defined on the
        properties, look up all available plugins for the project's
        technology. Else, only return 'generate'
        :param ctx:
        :return:
        """
        print('project' in properties)
        if 'project' in properties:
            return ["PROJECTS", ]
        else:
            return ['generate', ]

    def get_command(self, ctx, cmd_name):
        if 'project' in properties:
            return None
        else:
            mod = import_module('noora.plugins.GeneratePlugin')
            return mod.cli

    @staticmethod
    def find_plugin(command, properties):
        plugins = properties.get('plugins')
        for plugin in plugins:
            p = ClassLoader.find(plugin)
            if command.lower() == p.get_type().lower():
                return p

    @staticmethod
    # FIXME: move to proper place
    def build_dir(version, properties):
        if version == properties.get("default_version"):
            return properties.get("create.dir")
        return os.path.join(properties.get("alter.dir"), version)
