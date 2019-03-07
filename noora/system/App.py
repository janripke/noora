import os
from importlib import import_module

import click

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
        if 'project' in properties:
            return ["generate", ]
        else:
            return ['generate', ]

    def get_command(self, ctx, cmd_name):
        if 'project' in properties:
            mod = import_module('noora.plugins.{}.generate.GeneratePlugin'.format(
                properties['technology']))
            return mod.GeneratePlugin.upgrade_project
        else:
            mod = import_module('noora.plugins.GeneratePlugin')
            return mod.cli
