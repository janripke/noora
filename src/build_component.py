#!/usr/bin/env python
import sys
import os
import subprocess
import shutil
import zipfile
INSTALL_DIR=os.path.abspath(os.path.dirname(sys.argv[0]))
POVS_DIR=INSTALL_DIR.split('bin')[0]
BASE_DIR=os.path.abspath('.')+os.sep
M_CR=chr(13)
M_LF=chr(10)
M_QUOTE=chr(39)
sys.path.append(BASE_DIR)
import config
import utils

SCHEMAS=config.SCHEMAS
SCHEMA_OBJECTS=config.CREATE_SCHEMA_OBJECTS
SOURCE_OBJECTS=config.CREATE_SOURCE_OBJECTS
COMPONENT_NAME=config.COMPONENT_NAME
COMPONENT_EXCLUDED_FILES=config.COMPONENT_EXCLUDED_FILES
COMPONENT_CREATE_VERSION=config.COMPONENT_CREATE_VERSION
COMPONENT_RELEASE_FOLDER=config.COMPONENT_RELEASE_FOLDER

def usage():
  print "Noora database installer, build_compent.py"
  print "creates a database independend component."
  print "options:"
  print "-version=[VERSION], required, the version to use."
  
def invalid_build_version(build_version):
  if build_version==None:
    usage()
    print
    print "error: invalid build version"
    exit(1) 

def get_base_dir():
  return BASE_DIR+os.sep

def get_schema_create_dir():
  return get_base_dir()+'create'+os.sep

def get_schema_alter_dir():
  return get_base_dir()+'alter'+os.sep

def get_schema_dir(build_version):
  schema_dir=None
  if build_version==COMPONENT_CREATE_VERSION:
    schema_dir=get_schema_create_dir()
  else:
    schema_dir=get_schema_alter_dir()+build_version+os.sep
  return schema_dir

def get_source_dir():
  return get_base_dir()+'src'+os.sep

def schema_dir_not_present(build_version):
  schema_dir=get_schema_dir(build_version)
  if utils.dir_is_not_present(schema_dir):
    usage()
    print
    print "error: schema folder is not present"
    exit(1)

def source_dir_not_present():
  source_dir=get_source_dir()
  if utils.dir_is_not_present(source_dir):
    usage()
    print
    print "error: source folder is not present"
    exit(1)


def get_build_version(parameters):
  build_version=utils.get_parameter_value(parameters,'-version=')
  return build_version 


def get_base_dir():
  return BASE_DIR

def get_install_dir():
  return INSTALL_DIR+os.sep

def get_releases_dir():
  return get_base_dir()+COMPONENT_RELEASE_FOLDER+os.sep

def get_build_dir(build_version):
  return get_releases_dir()+COMPONENT_NAME+'_'+build_version+os.sep

def file_is_not_excluded(file):
  result=True
  excluded_files=COMPONENT_EXCLUDED_FILES
  for excluded_file in excluded_files:
    if excluded_file==file:
      result=False
      break
  return result


if __name__ == "__main__":
  
  print ""
  parameters=utils.get_parameters()

  if utils.is_parameter(parameters,'-h'):
    usage()
    exit(1)

  build_version=get_build_version(parameters)
  invalid_build_version(build_version)

  schema_dir_not_present(build_version)
  source_dir_not_present()  
  
  print "creating component with version "+build_version

  build_folder=get_build_dir(build_version)

  # compress the build
  releases_dir=get_releases_dir()
  if utils.dir_is_not_present(releases_dir):
    os.makedirs(releases_dir)
  zip_folder=releases_dir
  print "zip_folder",zip_folder
  zip_file=zip_folder+COMPONENT_NAME+'_'+build_version+'.zip'
  print zip_file.split(get_base_dir())[1]
  zip_handle=zipfile.ZipFile(zip_file,'w')

  for schema in SCHEMAS:

    for object in SCHEMA_OBJECTS:

      # ddl objects
      folder=get_schema_dir(build_version)+schema+os.sep+'ddl'+os.sep+object
      target_folder=COMPONENT_NAME+'_'+build_version+os.sep+'ddl'+os.sep+object+os.sep

      files=utils.find_files(folder)
      for file in files:
        if file_is_not_excluded(file):
          source_file=folder+os.sep+file
          target_file=target_folder+file
          print target_file
          zip_handle.write(source_file,target_file,zipfile.ZIP_DEFLATED)

    for object in SOURCE_OBJECTS:

      # ddl objects
      folder=get_source_dir()+schema+os.sep+object
      target_folder=COMPONENT_NAME+'_'+build_version+os.sep+'ddl'+os.sep+object+os.sep

      files=utils.find_files(folder)
      for file in files:
        if file_is_not_excluded(file):
          source_file=folder+os.sep+file
          target_file=target_folder+file
          print target_file
          zip_handle.write(source_file,target_file,zipfile.ZIP_DEFLATED)
  
    # global dat files
    folder=get_schema_dir(build_version)+schema+os.sep+'dat'
    target_folder=COMPONENT_NAME+'_'+build_version+os.sep+'dat'+os.sep

    files=utils.find_files(folder)
    for file in files:
      if file_is_not_excluded(file):
        source_file=folder+os.sep+file
        target_file=target_folder+file
        print target_file
        zip_handle.write(source_file,target_file,zipfile.ZIP_DEFLATED)

    # add component_utils.py
    source_folder=get_install_dir()
    filename='component_utils.py'
    source_file=source_folder+filename
    target_folder=COMPONENT_NAME+'_'+build_version+os.sep
    target_file=target_folder+filename
    print target_file
    zip_handle.write(source_file,target_file,zipfile.ZIP_DEFLATED)

    # add setup.py
    source_folder=get_install_dir()
    filename='setup.py'
    source_file=source_folder+filename
    target_folder=COMPONENT_NAME+'_'+build_version+os.sep
    target_file=target_folder+filename
    print target_file
    zip_handle.write(source_file,target_file,zipfile.ZIP_DEFLATED)

    # add setup.sql
    source_folder=get_install_dir()
    filename='setup.sql'
    source_file=source_folder+filename
    target_folder=COMPONENT_NAME+'_'+build_version+os.sep
    target_file=target_folder+filename
    print target_file
    zip_handle.write(source_file,target_file,zipfile.ZIP_DEFLATED)

    # create and add component.py
    source_folder=get_releases_dir()
    source_file=source_folder+"component.py"
    lines='COMPONENT_NAME='+M_QUOTE+COMPONENT_NAME+M_QUOTE+M_CR+M_LF+'COMPONENT_VERSION='+M_QUOTE+build_version+M_QUOTE+M_CR+M_LF+'COMPONENT_CREATE_VERSION='+M_QUOTE+COMPONENT_CREATE_VERSION+M_QUOTE
    utils.write_file(source_file,lines)

    target_folder=COMPONENT_NAME+'_'+build_version+os.sep
    target_file=target_folder+'component.py'
    
    print target_file
    zip_handle.write(source_file,target_file,zipfile.ZIP_DEFLATED)
    os.remove(source_file)

  zip_handle.close()
  print "component for version "+build_version+" created."
