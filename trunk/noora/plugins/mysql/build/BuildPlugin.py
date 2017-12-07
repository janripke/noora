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
from noora.version.VersionGuesser import VersionGuesser


class BuildPlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self, "generate", None)

    def execute(self, arguments, properties):

        # create a target folder if not present.
        # find the version
        # create the zip file {component_name}_{version}.zip
        # scan the dat folder
        # scan the ddl folder
        # add the script checkversion.sql to the root

        project = ''
        version = None

        if arguments.v:
            version = arguments.v

        current_dir = properties.get_property('current.dir')
        project_file = properties.get_property('project.file')
        config_file = File(os.path.join(current_dir, project_file))
        if not config_file.exists():
            database = raw_input('database : ')
            project = database + "-db"
            host = raw_input('host [localhost] : ')
            host = Ora.nvl(host, "localhost")
            username = raw_input('username : ')
            password = raw_input('password : ')
            version = raw_input('version [1.0.0]: ')
            version = Ora.nvl(version, "1.0.0")

            os.mkdir(project)
            template_dir = os.path.join(properties.get_property('plugin.dir'), 'mysql', 'generate', 'templates')
            template_file = os.path.join(template_dir, project_file)

            f = open(template_file)
            stream = f.read()
            f.close()
            stream = stream.replace('{host}', host)
            stream = stream.replace('{database}', database)
            stream = stream.replace('{username}', username)
            stream = stream.replace('{password}', password)
            stream = stream.replace('{version}', version)

            config_file = os.path.join(current_dir, project, project_file)
            f = open(config_file, 'w')
            f.write(stream)
            f.close()

        properties.set_property('alter.dir', os.path.join(current_dir, project, 'alter'))
        properties.set_property('create.dir', os.path.join(current_dir, project, 'create'))

        config_file = os.path.join(current_dir, project, project_file)
        f = open(config_file)
        data = json.load(f)
        for key in data.keys():
            properties.set_property(key, data[key])
        f.close()

        versions = Versions()
        version_loader = VersionLoader(versions)
        version_loader.load(properties)
        versions.sort()
        version_guesser = VersionGuesser(properties, versions)
        next_version = version_guesser.guess(version).to_string()
        version_dir = version_guesser.to_folder(next_version)

        # create the version folder
        os.makedirs(version_dir)

        databases = properties.get_property('databases')
        version_database = properties.get_property('version_database')
        default_version = properties.get_property('default_version')
        environments = properties.get_property('environments')
        objects = properties.get_property('create_objects')

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
                    stream = properties.get_property('version_insert_statement')
                else:
                    stream = properties.get_property('version_update_statement')

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
                    stream = properties.get_property('environment_insert_statement')
                    stream = stream.replace('<environment>', environment)
                    f.write(stream)
                    f.close()

            # create the ddl folder
            ddl_dir = os.path.join(database_dir, 'ddl')
            os.mkdir(ddl_dir)

            # create the object folders in the ddl folder
            for object in objects:
                os.mkdir(os.path.join(ddl_dir, object))

            # create the template code on create.
            if database == version_database and next_version == default_version:
                for object in objects:
                    object_dir = os.path.join(template_dir, object)
                    if os.path.exists(object_dir):
                        files = Files.list(File(object_dir))
                        for file in files:
                            shutil.copyfile(file.get_url(), os.path.join(ddl_dir, object, file.tail()))

        print "version " + next_version + " created."
