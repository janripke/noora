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

        # configReader = self.getConfigReader()
        # createVersion = versions[0]
        # if createVersion == version:
        #     stream = configReader.getValue('COMPONENT_INSERT_STATEMENT')
        # else:
        #     stream = configReader.getValue('COMPONENT_UPDATE_STATEMENT')
        # stream = stream.replace('<version>', version)
        # stream = stream.replace('<name>', componentName)
        # return stream

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
        component_select_statement = properties.get_property("component_select_statement")
        component_select_statement = component_select_statement.replace('<name>', component_name)
        component_select_statement = component_select_statement.replace('<previous>', '')
        print component_select_statement

        zip_handle.close()

        print "component with version " + version + " created."
                # if projectHelper.folderPresent(folder):
                #     if folder.endswith('lib') == False:
                #         files = projectHelper.findFiles(folder)
                #         for file in files:
                #             sourceFile = folder + os.sep + file
                #             targetFile = zipFolder + file
                #             zipHandle.write(sourceFile, targetFile, zipfile.ZIP_DEFLATED)


        # # componentSelectStatement = configReader.getValue('COMPONENT_SELECT_STATEMENT')
        # # projectHelper.failOnNone(componentSelectStatement, 'the variable COMPONENT_SELECT_STATEMENT is not set.')
        #
        # componentTargetFolder = configReader.getValue('COMPONENT_TARGET_FOLDER')
        # projectHelper.failOnNone(componentTargetFolder, 'the variable COMPONENT_TARGET_FOLDER is not set.')
        # targetFolder = self.getBaseDir() + os.sep + componentTargetFolder
        #
        # componentExcludedFiles = configReader.getValue('COMPONENT_EXCLUDED_FILES')
        # projectHelper.failOnNone(componentExcludedFiles, 'the variable COMPONENT_EXCLUDED_FILES is not set.')
        #
        # default_databases = properties.get_property('databases')
        # databases = Ora.nvl(arguments.d, default_databases)
        # Fail.fail_on_invalid_database(arguments.d, properties)
        #
        # default_environment = properties.get_property('default_environment')
        # environment = Ora.nvl(arguments.e, default_environment)
        # Fail.fail_on_invalid_environment(arguments.e, properties)
        #
        # objects = properties.get_property('create_objects')
        #
        # version_database = properties.get_property('version_database')
        #
        # alter_dir = properties.get_property('alter.dir')
        #
        #
        #
        #
        # # create a target folder if not present.
        # # find the version
        # # create the zip file {component_name}_{version}.zip
        # # scan the dat folder
        # # scan the ddl folder
        # # add the script checkversion.sql to the root
        #
        # project = ''
        # version = None
        #
        # if arguments.v:
        #     version = arguments.v
        #
        # current_dir = properties.get_property('current.dir')
        # project_file = properties.get_property('project.file')
        # config_file = File(os.path.join(current_dir, project_file))
        # if not config_file.exists():
        #     database = raw_input('database : ')
        #     project = database + "-db"
        #     host = raw_input('host [localhost] : ')
        #     host = Ora.nvl(host, "localhost")
        #     username = raw_input('username : ')
        #     password = raw_input('password : ')
        #     version = raw_input('version [1.0.0]: ')
        #     version = Ora.nvl(version, "1.0.0")
        #
        #     os.mkdir(project)
        #     template_dir = os.path.join(properties.get_property('plugin.dir'), 'mysql', 'generate', 'templates')
        #     template_file = os.path.join(template_dir, project_file)
        #
        #     f = open(template_file)
        #     stream = f.read()
        #     f.close()
        #     stream = stream.replace('{host}', host)
        #     stream = stream.replace('{database}', database)
        #     stream = stream.replace('{username}', username)
        #     stream = stream.replace('{password}', password)
        #     stream = stream.replace('{version}', version)
        #
        #     config_file = os.path.join(current_dir, project, project_file)
        #     f = open(config_file, 'w')
        #     f.write(stream)
        #     f.close()
        #
        # properties.set_property('alter.dir', os.path.join(current_dir, project, 'alter'))
        # properties.set_property('create.dir', os.path.join(current_dir, project, 'create'))
        #
        # config_file = os.path.join(current_dir, project, project_file)
        # f = open(config_file)
        # data = json.load(f)
        # for key in data.keys():
        #     properties.set_property(key, data[key])
        # f.close()
        #
        # versions = Versions()
        # version_loader = VersionLoader(versions)
        # version_loader.load(properties)
        # versions.sort()
        # version_guesser = VersionGuesser(properties, versions)
        # next_version = version_guesser.guess(version).to_string()
        # version_dir = version_guesser.to_folder(next_version)
        #
        # # create the version folder
        # os.makedirs(version_dir)
        #
        # databases = properties.get_property('databases')
        # version_database = properties.get_property('version_database')
        # default_version = properties.get_property('default_version')
        # environments = properties.get_property('environments')
        # objects = properties.get_property('create_objects')
        #
        # for database in databases:
        #
        #     # create the scheme folder
        #     database_dir = os.path.join(version_dir, database)
        #     os.mkdir(database_dir)
        #
        #     # create the dat folder
        #     dat_dir = os.path.join(database_dir, 'dat')
        #     os.mkdir(dat_dir)
        #
        #     # create the version script in the dat folder
        #     if database == version_database:
        #         version_file = os.path.join(dat_dir, 'version.sql')
        #         f = open(version_file, 'w')
        #
        #         if next_version == default_version:
        #             stream = properties.get_property('version_insert_statement')
        #         else:
        #             stream = properties.get_property('version_update_statement')
        #
        #         stream = stream.replace('<version>', next_version)
        #         f.write(stream)
        #         f.close()
        #
        #         # sqlScript=self.getSqlVersionStatement(versions, version)
        #         # projectHelper.writeFile(datFolder+os.sep+'version.sql', sqlScript)
        #
        #     # create the environment folders in the dat folder
        #     for environment in environments:
        #
        #         os.mkdir(os.path.join(dat_dir, environment))
        #
        #         # create the environment script in the dat folder.
        #         if database == version_database and next_version == default_version:
        #             environment_file = os.path.join(dat_dir, environment, 'environment.sql')
        #
        #             f = open(environment_file, 'w')
        #             stream = properties.get_property('environment_insert_statement')
        #             stream = stream.replace('<environment>', environment)
        #             f.write(stream)
        #             f.close()
        #
        #     # create the ddl folder
        #     ddl_dir = os.path.join(database_dir, 'ddl')
        #     os.mkdir(ddl_dir)
        #
        #     # create the object folders in the ddl folder
        #     for object in objects:
        #         os.mkdir(os.path.join(ddl_dir, object))
        #
        #     # create the template code on create.
        #     if database == version_database and next_version == default_version:
        #         for object in objects:
        #             object_dir = os.path.join(template_dir, object)
        #             if os.path.exists(object_dir):
        #                 files = Files.list(File(object_dir))
        #                 for file in files:
        #                     shutil.copyfile(file.get_url(), os.path.join(ddl_dir, object, file.tail()))
        #
        # print "version " + next_version + " created."
