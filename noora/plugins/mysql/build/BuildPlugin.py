#!/usr/bin/env python
import os
import json
import shutil
from noora.plugins.Plugin import Plugin
from noora.io.File import File
from noora.io.Files import Files
from noora.system.Ora import Ora
from noora.version.Versions import Versions
from noora.version.VersionLoader import VersionLoader
from noora.version.Version import Version
from noora.plugins.Fail import Fail
from noora.system.App import App
from zipfile import ZipFile
from zipfile import ZIP_DEFLATED


class BuildPlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self, "generate", None)

    def version_statement(self, version, properties):
        if version == properties.get_property("default_version"):
            return properties.get_property("component_insert_statement")
        return properties.get_property("component_update_statement")

    def execute(self, arguments, properties):

        properties.set_property('create.dir', os.path.join(properties.get_property('current.dir'), 'create'))
        properties.set_property('alter.dir', os.path.join(properties.get_property('current.dir'), 'alter'))

        version = arguments.v
        Fail.fail_on_no_version(version)
        Fail.fail_on_unknown_version(version, properties)

        default_databases = properties.get_property('databases')
        databases = Ora.nvl(arguments.d, default_databases)
        Fail.fail_on_invalid_database(arguments.d, properties)

        current_dir = properties.get_property('current.dir')
        component_name = properties.get_property('component_name')
        target_dir = os.path.join(current_dir, properties.get_property('component_target_folder'))

        objects = properties.get_property('create_objects')

        build_dir = App.build_dir(version, properties)

        # exclude the file 'version.sql', this file is excluded from the dat listing below.
        component_excluded_files = properties.get_property('component_excluded_files')
        excluded_files = properties.get_property('excluded_files')
        excluded_files.extend(component_excluded_files)

        # create the target folder, if not present.
        if not File(target_dir).exists():
            os.makedirs(target_dir)

        print "building component with version '" + version + "'"

        zip_file = os.path.join(target_dir, component_name + '_' + version + '.zip')
        zip_handle = ZipFile(zip_file, 'w')

        for database in databases:

            for object in objects:

                if not object == 'lib':
                    # global ddl objects
                    folder = File(os.path.join(build_dir, database, 'ddl', object))
                    zip_dir = File(os.path.join(component_name + '_' + version, 'ddl', object))

                    files = Files.list_filtered(folder, properties)
                    for file in files:
                        print file.get_url()
                        target_file = File(os.path.join(zip_dir.get_url(), file.tail()))
                        zip_handle.write(file.get_url(), target_file.get_url(), ZIP_DEFLATED)

            # global dat files
            folder = File(os.path.join(build_dir, database, 'dat'))
            zip_dir = File(os.path.join(component_name + '_' + version, 'dat'))

            files = Files.list_filtered(folder, properties)
            for file in files:
                print file.get_url()
                target_file = File(os.path.join(zip_dir.get_url(), file.tail()))
                zip_handle.write(file.get_url(), target_file.get_url(), ZIP_DEFLATED)

        # create the version script in the dat folder
        version_statement = self.version_statement(version, properties)
        version_statement = version_statement.replace('<version>', version)
        version_statement = version_statement.replace('<name>', component_name)

        f = open('version.sql', 'w')
        f.write(version_statement)
        f.close()

        zip_dir = File(os.path.join(component_name + '_' + version, 'dat'))
        target_file = File(os.path.join(zip_dir.get_url(), 'version.sql'))
        zip_handle.write('version.sql', target_file.get_url())

        # remove the version.sql file.
        os.remove('version.sql')

        # create the checkversion script in the root folder
        # first retrieve the previous version for the checkversion script
        versions = Versions()
        version_loader = VersionLoader(versions)
        version_loader.load(properties)
        versions.sort()
        previous = versions.previous(Version(version))

        component_select_statement = properties.get_property("component_select_statement")
        component_select_statement = component_select_statement.replace('<name>', component_name)
        component_select_statement = component_select_statement.replace('<previous>', previous.get_value())
        print component_select_statement

        f = open('checkversion.sql', 'w')
        f.write(component_select_statement)
        f.close()

        zip_dir = File(os.path.join(component_name + '_' + version))
        target_file = File(os.path.join(zip_dir.get_url(), 'checkversion.sql'))
        zip_handle.write('checkversion.sql', target_file.get_url())

        # remove the version.sql file.
        os.remove('checkversion.sql')

        zip_handle.close()

        print "component with version " + version + " created."

