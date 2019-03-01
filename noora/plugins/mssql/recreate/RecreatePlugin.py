import os
import argparse

from noora.version.Versions import Versions
from noora.version.VersionLoader import VersionLoader

from noora.system.ClassLoader import ClassLoader

from noora.plugins.Plugin import Plugin

from noora.connectors.MssqlConnector import MssqlConnector


class RecreatePlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self, "recreate", MssqlConnector())

    def parse_args(self, parser, args):
        parser.add_argument('-h', type=str, help='host', required=False)
        parser.add_argument('-s', type=str, help='schema', required=False)
        parser.add_argument('-e', type=str, help='environment', required=False)
        parser.add_argument('-v', type=str, help='version', required=False)
        parser.add_argument('-a', type=str, help='alias', required=False)
        return parser.parse_args(args)

    def find_plugin(self, properties, name):
        plugins = properties.get('plugins')
        for plugin in plugins:
            p = ClassLoader.find(plugin)
            if name.lower() == p.get_type().lower():
                return p

    def execute(self, arguments, properties):
        properties['create.dir'] = os.path.join(properties.get('current.dir'), 'create')
        properties['alter.dir'] = os.path.join(properties.get('current.dir'), 'alter')

        # find the drop plugin.
        plugin = self.find_plugin(properties, 'drop')

        # create the drop arguments and execute the plugin
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('-h', type=str, help='host', required=True)
        parser.add_argument('-s', type=str, help='schema', required=False)
        parser.add_argument('-e', type=str, help='environment', required=False)
        parser.add_argument('-a', type=str, help='alias', required=False)

        commands = []
        if arguments.h:
            commands.append('-h='+arguments.h)

        if arguments.s:
            commands.append('-s='+arguments.d)

        if arguments.e:
            commands.append('-e='+arguments.e)

        if arguments.a:
            commands.append('-a='+arguments.a)

        drop_arguments = parser.parse_args(commands)
        plugin.execute(drop_arguments, properties)

        # find the create plugin.
        plugin = self.find_plugin(properties, 'create')

        # create the create arguments and execute the plugin
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('-h', type=str, help='host', required=True)
        parser.add_argument('-s', type=str, help='schema', required=False)
        parser.add_argument('-e', type=str, help='environment', required=False)
        parser.add_argument('-a', type=str, help='alias', required=False)

        commands = []
        if arguments.h:
            commands.append('-h='+arguments.h)

        if arguments.s:
            commands.append('-s='+arguments.s)

        if arguments.e:
            commands.append('-e='+arguments.e)

        if arguments.a:
            commands.append('-a='+arguments.a)

        create_arguments = parser.parse_args(commands)
        plugin.execute(create_arguments, properties)

        versions = Versions()
        version_loader = VersionLoader(versions)
        version_loader.load(properties)
        versions.sort()

        # retrieve the update versions
        default_version = properties.get('default_version')
        update_versions = []
        for version in versions.list():
            if version.get_value() == default_version and arguments.v == version.get_value():
                break
            if version.get_value() == arguments.v:
                update_versions.append(version.get_value())
                break

            if version.get_value() != default_version:
                update_versions.append(version.get_value())

        # find the update plugin.
        plugin = self.find_plugin(properties, 'update')

        # create the arguments and execute the plugin
        for version in update_versions:
            parser = argparse.ArgumentParser(add_help=False)
            parser.add_argument('-h', type=str, help='host', required=True)
            parser.add_argument('-s', type=str, help='schema', required=False)
            parser.add_argument('-e', type=str, help='environment', required=False)
            parser.add_argument('-v', type=str, help='version', required=True)

            commands = []
            if arguments.h:
                commands.append('-h='+arguments.h)

            if arguments.s:
                commands.append('-s='+arguments.s)

            if arguments.e:
                commands.append('-e='+arguments.e)

            if arguments.a:
                commands.append('-a='+arguments.a)

            commands.append('-v='+version)

            update_arguments = parser.parse_args(commands)
            plugin.execute(update_arguments, properties)