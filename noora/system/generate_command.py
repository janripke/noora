import os
from importlib import import_module

import click


class GenerateCommand(click.MultiCommand):
    def list_commands(self, ctx):
        """
        Return a list of technologies that contain a 'generate' package with
        a cli_outside_scope method

        :return: A list of available technologies
        """
        res = []
        plugin_dir = ctx.obj['plugin.dir']
        for f in os.listdir(plugin_dir):
            f_path = "{}/{}".format(plugin_dir, f)
            if os.path.isdir(f_path) and os.path.exists("{}/generate".format(f_path)):
                try:
                    mod = import_module("noora.plugins.{}.generate".format(f))
                    if hasattr(mod, 'cli_outside_scope'):
                        res.append(f)
                # Generic handling, Py < 3.6 throws ImportError, >= 3.6 ModuleNotFoundError
                except:
                    pass
        return res

    def get_command(self, ctx, cmd_name):
        try:
            mod = import_module("noora.plugins.{}.generate".format(cmd_name))
        # Generic handling, Py < 3.6 throws ImportError, >= 3.6 ModuleNotFoundError
        except:
            return None

        if hasattr(mod, 'cli_outside_scope'):
            return mod.cli_outside_scope

        return None


@click.command(cls=GenerateCommand)
def cli():
    """
    The generate plugin can be used to create a new database project or
    bootstrap a new version for the currently selected project.
    """
    pass
