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
  print "creates the folder structure of the given version"
  print "remarks : the given version must be present in config.VERSIONS
  print "          the first version in config.VERSIONS is considered as the baseline (create)."
  print "          the folder structure is only created when the version folder is not already present."
  print "-v= --version= required, contains the version to create."
  print "-s= --scheme=  not required, contains the scheme to create. "

def has_scheme(scheme):
  for default_scheme in SCHEMES:
    if default_scheme.lower()==scheme.lower():
      return True
  return False
    
def has_version(version):
  for allowed_version in VERSIONS:
    if allowed_version.lower()==version.lower():
      return True
  return False 

def get_schemes(parameters):
  build_schemes=[]
  build_scheme=utils.get_parameter_value_from_list(parameters,['-s=','--scheme='])
  if build_scheme==None:
    build_schemes=SCHEMES
  else:
    build_schemes.append(build_scheme)
  return build_schemes
  
def invalid_schemes(schemes):
  for scheme in schemes:
    if has_scheme(scheme)==False:
      usage()
      print
      print "the given schema is not valid for this project."
      exit(1)

def schemes_not_none(schemes):
  if schemes==None:
    usage()
    print
    print "no scheme was found."
    exit(1)

def invalid_version(version):
  if has_version(version)==False:
    usage()
    print
    print "the given version is not valid for this project."
    exit(1)
    
def version_not_none(version):
  if version==None:
    usage()
    print
    print "no version was given."
    exit(1)

def get_version(parameters):
  version=utils.get_parameter_value_from_list(parameters,['-v=','--version='])
  return version    

def version_folder_present(version_folder):
  if utils.dir_is_present(version_folder):
    usage()
    print
    print "version folder is already present."
    exit(1)

def get_version_folder(version):
  create_version=VERSIONS[0]
  if create_version==version:
    version_folder=BASE_DIR+os.sep+'create'
  else:
    version_folder=BASE_DIR+os.sep+'alter'+os.sep+version
  return version_folder

def get_sql_version_statement(version):
  create_version=VERSIONS[0]
  if create_version==version:
    stream=VERSION_INSERT_STATEMENT
  else:
    stream=VERSION_UPDATE_STATEMENT
  stream=stream.replace('<version>',version)
  return stream

if __name__ == "__main__":

  print ""
  parameters=utils.get_parameters()

  if utils.is_parameter(parameters,'-h'):
    usage()
    exit(1)
      
  schemes=get_schemes(parameters)
  schemes_not_none(schemes)
  invalid_schemes(schemes)
      
  version=get_version(parameters)
  version_not_none(version)
  invalid_version(version)

  version_folder=get_version_folder(version)
  version_folder_present(version)

  # create the version folder
  os.mkdir(version_folder)
  
  for scheme in schemes:

    # create the scheme folder
    scheme_folder=version_folder+os.sep+scheme
    os.mkdir(scheme_folder)

    # create the dat folder
    dat_folder=scheme_folder+os.sep+'dat'
    os.mkdir(dat_folder)

    # create the version script in the dat folder
    if scheme==VERSION_SCHEME:
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

