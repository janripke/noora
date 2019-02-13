#!/usr/bin/env python
import os
import json
import shutil

from noora.version.Versions import Versions
from noora.version.VersionLoader import VersionLoader
from noora.version.VersionGuesser import VersionGuesser

from noora.system.Ora import Ora
from noora.io.File import File
from noora.io.Files import Files

from noora.plugins.Plugin import Plugin


class GeneratePlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self, "generate", None)

    def parse_args(self, parser, args):
        parser.add_argument('-v', type=str, help='version', required=False)
        return parser.parse_args(args)

    def execute(self, arguments, properties):
        project = ''
        version = None

        if arguments.v:
            version = arguments.v

        current_dir = properties.get('current.dir')
        project_file = properties.get('project.file')
        config_file = File(os.path.join(current_dir, project_file))
        if not config_file.exists():
            database = input('database : ')
            project = database + "-db"
            host = input('host [localhost] : ')
            host = Ora.nvl(host, "localhost")
            username = input('username : ')
            password = input('password : ')
            # FIXME: this plugin version is embedded pretty deep in the code
            version = input('version [1.0.0]: ')
            version = Ora.nvl(version, "1.0.0")

            os.mkdir(project)
            template_dir = os.path.join(
                properties.get('plugin.dir'), 'mysql', 'generate', 'templates')
            template_file = os.path.join(template_dir, project_file)

            f = open(template_file)
            stream = f.read()
            f.close()
            stream = stream.replace('{project}', project)
            stream = stream.replace('{database}', database)
            stream = stream.replace('{host}', host)
            stream = stream.replace('{username}', username)
            stream = stream.replace('{password}', password)
            stream = stream.replace('{version}', version)

            config_file = os.path.join(current_dir, project, project_file)
            f = open(config_file, 'w')
            f.write(stream)
            f.close()

        properties['alter.dir'] = os.path.join(current_dir, project, 'alter')
        properties['create.dir'] = os.path.join(current_dir, project, 'create')

        config_file = os.path.join(current_dir, project, project_file)
        f = open(config_file)
        data = json.load(f)
        for key in data.keys():
            properties[key] = data[key]
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
                    # FIXME: template_dir may be unassigned
                    object_dir = os.path.join(template_dir, obj)
                    if os.path.exists(object_dir):
                        files = Files.list(File(object_dir))
                        for file in files:
                            shutil.copyfile(
                                file.get_url(), os.path.join(ddl_dir, obj, file.tail()))

        print("version " + next_version + " created.")
