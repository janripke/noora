import os
from zipfile import ZipFile
from zipfile import ZIP_DEFLATED

from noora.version.Versions import Versions
from noora.version.VersionLoader import VersionLoader
from noora.version.Version import Version

from noora.system import Ora
from noora.io.File import File
from noora.io.Files import Files

from noora.plugins.mysql.MysqlPlugin import MysqlPlugin
from noora.plugins.Fail import Fail


class BuildPlugin(MysqlPlugin):
    def _validate_and_prepare(self, properties, arguments):
        prepared_args = {}

        version = arguments.get('version')
        Fail.fail_on_no_version(version)
        Fail.fail_on_unknown_version(version, properties)
        prepared_args['version'] = version

        database = arguments.get('database')
        default_databases = properties.get('databases')
        databases = Ora.nvl(database, default_databases)
        Fail.fail_on_invalid_database(database, properties)
        prepared_args['databases'] = databases

        return prepared_args

    def execute(self, properties, arguments):
        """
        Build the package after verifying version is valid, and database,
        if provided.

        :param properties: The project properties
        :param arguments: A dict of {
            'version': 'The version to package for'
            'database': 'The database to package for (optional)'
        }
        """
        prepared_args = self._validate_and_prepare(properties, arguments)

        version = prepared_args['version']
        databases = prepared_args['databases']
        current_dir = properties.get('current.dir')
        component_name = properties.get('component_name')
        target_dir = os.path.join(current_dir, properties.get('component_target_folder'))

        objects = properties.get('create_objects')

        if version == properties.get("default_version"):
            build_dir = properties.get("create.dir")
        else:
            build_dir = os.path.join(properties.get("alter.dir"), version)

        # exclude the file 'version.sql', this file is excluded from the dat listing below.
        component_excluded_files = properties.get('component_excluded_files')
        excluded_files = properties.get('excluded_files')
        excluded_files.extend(component_excluded_files)

        # create the target folder, if not present.
        if not File(target_dir).exists():
            os.makedirs(target_dir)

        print("building component with version '{}'".format(version))

        zip_file = os.path.join(target_dir, component_name + '_' + version + '.zip')
        zip_handle = ZipFile(zip_file, 'w')

        for database in databases:
            for obj in objects:
                if not obj == 'lib':
                    # global ddl objects
                    folder = File(os.path.join(build_dir, database, 'ddl', obj))
                    zip_dir = File(os.path.join(component_name + '_' + version, 'ddl', obj))

                    files = Files.list_filtered(folder, properties)
                    for file in files:
                        print(file.get_url())
                        target_file = File(os.path.join(zip_dir.get_url(), file.tail()))
                        zip_handle.write(file.get_url(), target_file.get_url(), ZIP_DEFLATED)

            # global dat files
            folder = File(os.path.join(build_dir, database, 'dat'))
            zip_dir = File(os.path.join(component_name + '_' + version, 'dat'))

            files = Files.list_filtered(folder, properties)
            for file in files:
                print(file.get_url())
                target_file = File(os.path.join(zip_dir.get_url(), file.tail()))
                zip_handle.write(file.get_url(), target_file.get_url(), ZIP_DEFLATED)

        # create the version script in the dat folder
        if version == properties.get("default_version"):
            version_statement = properties.get("component_insert_statement")
        else:
            version_statement = properties.get("component_update_statement")
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

        component_select_statement = properties.get("component_select_statement")
        component_select_statement = component_select_statement.replace('<name>', component_name)
        component_select_statement = component_select_statement.replace(
            '<previous>', previous.get_value())

        print(component_select_statement)

        f = open('checkversion.sql', 'w')
        f.write(component_select_statement)
        f.close()

        zip_dir = File(os.path.join(component_name + '_' + version))
        target_file = File(os.path.join(zip_dir.get_url(), 'checkversion.sql'))
        zip_handle.write('checkversion.sql', target_file.get_url())

        # remove the version.sql file.
        os.remove('checkversion.sql')

        zip_handle.close()

        print("component with version {} created.".format(version))
