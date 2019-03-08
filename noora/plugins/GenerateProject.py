import os
from importlib import import_module

import click


class GenerateProject(click.MultiCommand):
    def list_commands(self, ctx):
        """
        Check all plugin directories and return a list of plugins with a "GeneratePlugin" module
        :return: A list of available technologies
        """
        res = []
        cur_path = os.path.dirname(__file__)
        for f in os.listdir(cur_path):
            f_path = "{}/{}".format(cur_path, f)
            if os.path.isdir(f_path) and os.path.exists("{}/generate/GeneratePlugin.py".format(f_path)):
                res.append(f)
        return res

    def get_command(self, ctx, cmd_name):
        mod = import_module("noora.plugins.{}.generate.GeneratePlugin".format(cmd_name))
        return mod.GeneratePlugin.get_executor(outside_scope=True)


@click.command(cls=GenerateProject)
def cli():
    """
    The generate plugin can be used to create a new database project or
    bootstrap a new version for the currently selected project.
    """
    pass
