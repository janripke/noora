#!/usr/bin/env python
import sys
import os
import subprocess
import stat
INSTALL_DIR=os.path.abspath(os.path.dirname(sys.argv[0]))
POVS_DIR=INSTALL_DIR.split('bin')[0]
BASE_DIR=os.path.abspath('.')
sys.path.append(BASE_DIR)
import config
import utils
import version_utils

SCHEMAS=config.SCHEMAS
OBJECTS=config.CREATE_SCHEMA_OBJECTS
ENVIRONMENTS=config.ENVIRONMENTS
VERSION_SCHEMA=config.VERSION_SCHEMA
DEFAULT_VERSION=config.DEFAULT_VERSION
VERSION_UPDATE_STATEMENT=config.VERSION_UPDATE_STATEMENT

def usage():
  print "Noora database installer, prepare.py"
  print "creates the fixed folder structure of the next version"
  print "options:"
  print "-version=[VERSION], not required, the version to prepare"

def help_on_version_present(version):
  print ""
  print "version "+version+" is already present."

def get_alter_dir():
  alter_dir=get_base_dir()+os.sep+'alter'
  return alter_dir

def get_base_dir():
  return BASE_DIR

def get_version_dir(version):
  version_dir=get_alter_dir()+os.sep+version
  return version_dir

# checks if the version is already present
def version_is_present(version):
  result=False
  folder_versions=utils.find_dirs(get_alter_dir())
  for folder_version in folder_versions:
    if folder_version==version:
      result=True
      break
  return result

def get_next_version(parameters):  
  version=utils.get_parameter_value(parameters,'-version=')
  if version==None:
    version=config.DEFAULT_VERSION
    folder_versions=utils.find_dirs(get_alter_dir())
    folder_versions=version_utils.sort_as_versions(folder_versions)
    if len(folder_versions)!=0:

      last_version=folder_versions[len(folder_versions)-1]
      last_major=last_version.split('.')[0]
      last_minor=last_version.split('.')[1]
      last_build=last_version.split('.')[2]
      next_build=str(int(last_build)+1)
      version=last_major+'.'+last_minor+'.'+next_build
  return version


def get_sql_update_database_version(version):
  stream=VERSION_UPDATE_STATEMENT
  stream=stream.replace('<version>',version)
  return stream

if __name__ == "__main__":

  parameters=utils.get_parameters()
  version=get_next_version(parameters)
  if version_is_present(version):
    help_on_version_present(version)
    exit(1) 

  # create the version folder
  version_dir=get_version_dir(version)
  os.mkdir(version_dir)
  
  for schema in SCHEMAS:

    # create the schema folder
    schema_folder=get_version_dir(version)+os.sep+schema
    os.mkdir(schema_folder)

    # create the dat folder
    dat_folder=schema_folder+os.sep+'dat'
    os.mkdir(dat_folder)

    # create the version script in the dat folder
    if schema==VERSION_SCHEMA:
      sql_script=get_sql_update_database_version(version)
      utils.write_file(dat_folder+os.sep+'version.sql', sql_script)

    # create the environment folders in the dat folder
    for environment in ENVIRONMENTS:
      os.mkdir(dat_folder+os.sep+environment)

    # create the ddl folder
    ddl_folder=schema_folder+os.sep+'ddl'
    os.mkdir(ddl_folder)

    # create the object folders in the ddl folder
    for object in OBJECTS:
      os.mkdir(ddl_folder+os.sep+object)

  print "version "+version+" created."

