import os
from importlib import import_module

import click

from noora.system.Properties import Properties


class App(click.MultiCommand):
    @staticmethod
    def initialize_and_get_properties(ctx):
        """
        Makes sure the Properties object is initialized and assigned to the context object.
        :param ctx: The click context
        :return: a reference to the properties object
        """
        if not ctx.obj:
            ctx.obj = Properties()
        return ctx.obj

    def list_commands(self, ctx):
        """
        Get the commands based on the context. If 'project' is defined on the
        properties, look up all available plugins for the project's
        technology. Else, only return 'generate'.

        :return: A list of available commands
        """
        props = self.initialize_and_get_properties(ctx)

        if 'project' in props:
            technology = props.get('technology')
            res = []

            # Loop over the plugins for this technology and add all plugins to the list that have
            # a valid execute method # configured.
            plugin_path = os.path.join(props['plugin.dir'], technology)
            for p in os.listdir(plugin_path):
                p_path = os.path.join(plugin_path, p)
                if os.path.isdir(p_path):
                    # Try to import the cli command from the package root
                    try:
                        mod = import_module('noora.plugins.{}.{}'.format(technology, p))
                        if hasattr(mod, 'cli'):
                            res.append(p)
                    except:
                        pass
            return res

        # NOTE: in the future it might happen we support more than just 'generate' outside of a
        # project's scope. In this case one should loop over all technologies and plugins per
        # technology to check if an execute method exists that can be run outside of a project's
        # scope.
        else:
            return ['generate', ]

    def get_command(self, ctx, cmd_name):
        props = self.initialize_and_get_properties(ctx)

        if 'project' in props:
            # Import the module and return the cli method
            try:
                mod = import_module('noora.plugins.{}.{}'.format(props['technology'], cmd_name))
            except:
                return None
            if hasattr(mod, 'cli'):
                return mod.cli
        elif cmd_name == 'generate':
            mod = import_module('noora.system.GenerateCommand')
            return mod.cli

        return None
