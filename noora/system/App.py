import os
from importlib import import_module

import click

from noora.system.Properties import properties
from noora.plugins.Plugin import Plugin


class App(click.MultiCommand):
    def list_commands(self, ctx):
        """
        Get the commands based on the context. If 'project' is defined on the
        properties, look up all available plugins for the project's
        technology. Else, only return 'generate'

        :return: A list of available commands
        """
        if 'project' in properties:
            technology = properties.get('technology')
            res = []

            # Loop over the plugins for this technology and add all plugins to the list that have
            # a valid execute method # configured.
            plugin_path = os.path.join(properties['plugin.dir'], technology)
            for p in os.listdir(plugin_path):
                p_path = os.path.join(plugin_path, p)
                if os.path.isdir(p_path):
                    for f in os.listdir(p_path):
                        f_path = os.path.join(p_path, f)
                        if os.path.isfile(f_path) and f.endswith('Plugin.py'):
                            pname = f[:-3]
                            # Try importing the module and if the module has a class with the same name
                            mod = import_module('noora.plugins.{}.{}.{}'.format(technology, p, pname))
                            cls = getattr(mod, pname)
                            if cls and issubclass(cls, Plugin) and cls.get_executor():
                                res.append(p)
            return res

        # NOTE: in the future it might happen we support more than just 'generate' outside of a project's scope.
        # In this case one should loop over all technologies and plugins per technology to check if an execute method\
        # exists that can be run outside of a project's scope.
        else:
            return ['generate', ]

    def get_command(self, ctx, cmd_name):
        if 'project' in properties:
            # FIXME: not very nice to use cmd_name to generate plugin module name
            cls_name = "{}Plugin".format(cmd_name.capitalize())
            mod = import_module('noora.plugins.{}.{}.{}'.format(
                properties['technology'], cmd_name, cls_name))
            cls = getattr(mod, cls_name)
            return cls.get_executor()
        else:
            mod = import_module('noora.plugins.GeneratePlugin')
            return mod.cli
