import os
import shutil

from noora.version.Versions import Versions
from noora.version.VersionLoader import VersionLoader
from noora.version.VersionGuesser import VersionGuesser

from noora.plugins.Plugin import Plugin
from noora.io.File import File
from noora.io.Files import Files


class GeneratePlugin(Plugin):
    """
    This class provides generation functionality for MSSQL projects.
    """
    def prepare(self, version, host=None, port=None,
                database=None, schema=None, username=None, password=None):
        """
        Prepare the plugin. The version is always required, the rest only when
        generating an entirely new project.

        :param version: (Initial) project version to generate for
        :param host: The hostname for the new project. If not provided, an
            upgrade is assumed (optional)
        :param port: Port to connect on (optional)
        :param database: Name of the database (optional)
        :param schema: Name of the schema (optional)
        :param username: Database username (optional)
        :param password: Database password (optional)
        """
        # If no hostname was provided, we only set the version and then return
        self.set_argument('version', version)

        if not host:
            return

        properties = self._properties

        project_file = properties.get('project.file')
        current_dir = properties.get('current.dir')

        # Determine the project's name and create a new directory
        project = database + "-db"
        os.mkdir(project)

        # Get the json project template for this plugin
        template_file = os.path.join(
            properties.get('plugin.dir'), 'mssql', 'generate', 'templates', project_file)

        # Parse the template and replace the parameters
        with open(template_file) as fd:
            stream = fd.read()
        stream = stream.replace('{project}', project)
        stream = stream.replace('{database}', database)
        stream = stream.replace('{host}', host)
        stream = stream.replace('{port}', str(port))
        stream = stream.replace('{schema}', schema)
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

    def execute(self):
        properties = self._properties

        template_dir = os.path.join(
            properties.get('plugin.dir'), 'mssql', 'generate', 'templates')

        versions = Versions()
        version_loader = VersionLoader(versions)
        version_loader.load(properties)
        versions.sort()
        version_guesser = VersionGuesser(properties, versions)
        next_version = version_guesser.guess(self.get_argument('version')).to_string()
        version_dir = version_guesser.to_folder(next_version)

        # create the version folder
        os.makedirs(version_dir)

        schemes = properties.get('schemes')
        version_schema = properties.get('version_schema')
        default_version = properties.get('default_version')
        environments = properties.get('environments')
        objects = properties.get('create_objects')

        for schema in schemes:
            # create the scheme folder
            schema_dir = os.path.join(version_dir, schema)
            os.mkdir(schema_dir)

            # create the dat folder
            dat_dir = os.path.join(schema_dir, 'dat')
            os.mkdir(dat_dir)

            # create the version script in the dat folder
            if schema == version_schema:
                version_file = os.path.join(dat_dir, 'version.sql')
                f = open(version_file, 'w')

                if next_version == default_version:
                    stream = properties.get('version_insert_statement')
                else:
                    stream = properties.get('version_update_statement')

                stream = stream.replace('<version>', next_version)
                f.write(stream)
                f.close()

                # FIXME: remove?
                # sqlScript=self.getSqlVersionStatement(versions, version)
                # projectHelper.writeFile(datFolder+os.sep+'version.sql', sqlScript)

            # create the environment folders in the dat folder
            for environment in environments:
                os.mkdir(os.path.join(dat_dir, environment))

                # create the environment script in the dat folder.
                if schema == version_schema and next_version == default_version:
                    environment_file = os.path.join(dat_dir, environment, 'environment.sql')

                    f = open(environment_file, 'w')
                    stream = properties.get('environment_insert_statement')
                    stream = stream.replace('<environment>', environment)
                    f.write(stream)
                    f.close()

            # create the ddl folder
            ddl_dir = os.path.join(schema_dir, 'ddl')
            os.mkdir(ddl_dir)

            # create the object folders in the ddl folder
            for obj in objects:
                os.mkdir(os.path.join(ddl_dir, obj))

            # create the template code on create.
            if schema == version_schema and next_version == default_version:
                for obj in objects:
                    object_dir = os.path.join(template_dir, obj)
                    if os.path.exists(object_dir):
                        files = Files.list(File(object_dir))
                        for file in files:
                            shutil.copyfile(
                                file.get_url(), os.path.join(ddl_dir, obj, file.tail()))

        print("version {} created.".format(next_version))
