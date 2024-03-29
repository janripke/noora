import os
import shutil

from noora.version.versions import Versions
from noora.version.version_loader import VersionLoader
from noora.version.version_guesser import VersionGuesser

from noora.plugins.postgresql.pqsql_plugin import PGSQLPlugin
from noora.plugins.fails import Fail
from noora.io.file import File
from noora.io.files import Files


class GeneratePlugin(PGSQLPlugin):
    """This class provides generation functionality for MySQL projects."""
    def _validate_and_prepare(self, properties, arguments):
        prepared_args = {}

        # If no hostname was provided, we only set the version and then return
        version = arguments.get('version')
        if version:
            prepared_args['version'] = version

        host = arguments.get('host')
        if not host:
            return prepared_args

        project_file = properties.get('project.file')
        current_dir = properties.get('current.dir')

        # Determine the project's name and create a new directory
        database = arguments.get('database')
        Fail.fail_on_no_database(database)
        project = database + "-db"

        # First check the rest of the arguments before we continue
        port = arguments.get('port')
        Fail.fail_on_no_port(port)
        username = arguments.get('username')
        Fail.fail_on_no_user('username')
        password = arguments.get('password')

        # Get the json project template for this plugin
        template_file = os.path.join(
            properties.get('plugin.dir'), 'postgresql', 'generate', 'templates', project_file)

        # Create the project directory
        os.mkdir(project)

        # Parse the template and replace the parameters
        with open(template_file) as fd:
            stream = fd.read()
        stream = stream.replace('{project}', project)
        stream = stream.replace('{database}', database)
        stream = stream.replace('{host}', host)
        stream = stream.replace('{port}', str(port))
        stream = stream.replace('{username}', username)
        stream = stream.replace('{password}', password)
        stream = stream.replace('{version}', version)

        # Write the new configuration back to file
        config_file = os.path.join(current_dir, project, project_file)
        with open(config_file, 'w') as fd:
            fd.write(stream)

        # Update the project properties to set current.dir to the new project dir
        properties['current.dir'] = os.path.join(current_dir, project)

        # Update the project properties
        properties.update_config()

        return prepared_args

    def execute(self, properties, arguments):
        """
        Create or upgrade a project. The version is always required, the rest
        only when generating an entirely new project.

        :type properties: system.Properties.Properties
        :param properties: The project properties
        :type arguments: dict
        :param arguments: This dict contains the plugin arguments:

            * **version**: (Initial) project version to generate for;
            * **host**: The hostname for the new project. If not provided, an upgrade is assumed (optional);
            * **port**: Port to connect to (optional);
            * **database**: Name of the database (optional);
            * **schema**: Name of the schema (optional);
            * **username**: Database username (optional);
            * **password**: Database password (optional).
        """
        prepared_args = self._validate_and_prepare(properties, arguments)

        template_dir = os.path.join(
            properties.get('plugin.dir'), 'postgresql', 'generate', 'templates')

        versions = Versions()
        version_loader = VersionLoader(versions)
        version_loader.load(properties)
        versions.sort()
        version_guesser = VersionGuesser(properties, versions)
        next_version = version_guesser.guess(prepared_args.get('version')).to_string()
        version_dir = version_guesser.to_folder(next_version)

        # create the version folder
        os.makedirs(version_dir)

        databases = properties.get('databases')
        version_database = properties.get('version_database')
        default_version = properties.get('default_version')
        environments = properties.get('environments')
        objects = properties.get('create_objects')

        for database in databases:
            # create the scheme folder
            database_dir = os.path.join(version_dir, database)
            os.mkdir(database_dir)

            # create the dat folder
            dat_dir = os.path.join(database_dir, 'dat')
            os.mkdir(dat_dir)

            # create the version script in the dat folder
            if database == version_database:
                version_file = os.path.join(dat_dir, 'version.sql')
                f = open(version_file, 'w')

                if next_version == default_version:
                    stream = properties.get('version_insert_statement')
                else:
                    stream = properties.get('version_update_statement')

                stream = stream.replace('<version>', next_version)
                f.write(stream)
                f.close()

                # sqlScript=self.getSqlVersionStatement(versions, version)
                # projectHelper.writeFile(datFolder+os.sep+'version.sql', sqlScript)

            # create the environment folders in the dat folder
            for environment in environments:
                os.mkdir(os.path.join(dat_dir, environment))

                # create the environment script in the dat folder.
                if database == version_database and next_version == default_version:
                    environment_file = os.path.join(dat_dir, environment, 'environment.sql')

                    f = open(environment_file, 'w')
                    stream = properties.get('environment_insert_statement')
                    stream = stream.replace('<environment>', environment)
                    f.write(stream)
                    f.close()

            # create the ddl folder
            ddl_dir = os.path.join(database_dir, 'ddl')
            os.mkdir(ddl_dir)

            # create the object folders in the ddl folder
            for obj in objects:
                os.mkdir(os.path.join(ddl_dir, obj))

            # create the template code on create.
            if database == version_database and next_version == default_version:
                for obj in objects:
                    object_dir = os.path.join(template_dir, obj)
                    if os.path.exists(object_dir):
                        files = Files.list(File(object_dir))
                        for file in files:
                            shutil.copyfile(
                                file.get_url(), os.path.join(ddl_dir, obj, file.tail()))

        print("version {} created.".format(next_version))
