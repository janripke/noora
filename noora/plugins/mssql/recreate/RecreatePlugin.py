import os
from noora.plugins.Plugin import Plugin
from noora.connectors.MssqlConnector import MssqlConnector
from noora.version.Versions import Versions
from noora.version.VersionLoader import VersionLoader
from noora.system.ClassLoader import ClassLoader
import argparse


class RecreatePlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self, "recreate", MssqlConnector())

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
        parser.add_argument('-h', type=str, help='host', required=False)
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

        # create the drop arguments and execute the plugin
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('-h', type=str, help='host', required=False)
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

        # remove the default_version from the version list
        # by doing so, this reflects the present alters in the project folder
        alter_versions = []
        for version in versions.list():
            if version.get_value() != properties.get('default_version'):
                alter_versions.append(version.get_value())

        # create a list of versions up to the given version
        # if no version is given, the last available version in the project folder is assumed.
        if arguments.v:
            update_versions = []
            for version in alter_versions:
                update_versions.append(version)
                if version == arguments.v:
                    break

            alter_versions = update_versions

        # find the update plugin.
        plugin = self.find_plugin(properties, 'update')

        # create the arguments and execute the plugin
        for version in alter_versions:
            parser = argparse.ArgumentParser(add_help=False)
            parser.add_argument('-h', type=str, help='host', required=False)
            parser.add_argument('-s', type=str, help='schema', required=False)
            parser.add_argument('-e', type=str, help='environment', required=False)
            parser.add_argument('-a', type=str, help='alias', required=False)
            parser.add_argument('-v', type=str, help='version', required=False)

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