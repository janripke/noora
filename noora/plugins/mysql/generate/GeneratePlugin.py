import os
import shutil

import click

from noora.version.Versions import Versions
from noora.version.VersionLoader import VersionLoader
from noora.version.VersionGuesser import VersionGuesser

from noora.plugins.Plugin import Plugin
from noora.system.Properties import properties
from noora.io.File import File
from noora.io.Files import Files


class GeneratePlugin(Plugin):
    """
    This class provides generation functionality for MySQL projects.
    """
    _executable = 'execute_new_project'
    _executable_outside_scope = 'execute_new_version'

    @staticmethod
    @click.command()
    @click.option('-h', '--host', required=False, prompt=True, default='localhost')
    @click.option('-p', '--port', required=False, prompt=True, type=int, default=3306)
    @click.option('-d', '--database', required=True, prompt='Database name')
    @click.option('-U', '--username', required=True, prompt='Database username')
    @click.option('-P', '--password', required=True, prompt='Database password',
                  hide_input=True, confirmation_prompt=True)
    @click.option('-v', '--version', required=False,
                  prompt='Initial project version', default='1.0.0')
    def execute_new_project(host, port, database, username, password, version):
        """
        Generate a new MySQL database project
        """
        project_file = properties.get('project.file')
        current_dir = properties.get('current.dir')

        # Determine the project's name and create a new directory
        project = database + "-db"
        os.mkdir(project)

        # Get the json project template for this plugin
        template_file = os.path.join(
            properties.get('plugin.dir'), 'mysql', 'generate', 'templates', project_file)

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

        # Do the project creation crunching stuff
        GeneratePlugin.execute(version)

    @staticmethod
    @click.command()
    @click.option('-v', '--version')
    def execute_new_version(version):
        """
        Bootstrap a new version of a MySQL database project
        """
        # All we have to do here is call process_project with the new version
        GeneratePlugin.execute(version)

    @staticmethod
    def execute(version):
        template_dir = os.path.join(
            properties.get('plugin.dir'), 'mysql', 'generate', 'templates')

        versions = Versions()
        version_loader = VersionLoader(versions)
        version_loader.load(properties)
        versions.sort()
        version_guesser = VersionGuesser(properties, versions)
        next_version = version_guesser.guess(version).to_string()
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
