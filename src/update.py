#!/usr/bin/env python
import sys
import os
import subprocess
INSTALL_DIR=os.path.abspath(os.path.dirname(sys.argv[0]))
POVS_DIR=INSTALL_DIR.split('bin')[0]
BASE_DIR=os.path.abspath('.')
ALTER_DIR=BASE_DIR+os.sep+'alter'
sys.path.append(BASE_DIR)
import config
import utils
import version_utils

SCHEMAS=config.SCHEMAS
OBJECTS=config.CREATE_SCHEMA_OBJECTS
ORACLE_USERS=config.ORACLE_USERS
CHECK_VERSION_SCHEMA=config.CHECK_VERSION_SCHEMA
DEFAULT_ORACLE_SID=config.DEFAULT_ORACLE_SID
DEFAULT_ENVIRONMENT=config.DEFAULT_ENVIRONMENT
VERSION_SELECT_STATEMENT=config.VERSION_SELECT_STATEMENT
ENVIRONMENT_SELECT_STATEMENT=config.ENVIRONMENT_SELECT_STATEMENT

def usage():
  print "Noora database installer, update.py"
  print "executes the defined update scripts in the alter folders."
  print "options:"
  print "-version=[VERSION]" 
  print "-sid=[ORACLE_SID]"
  print "-env=[ENVIRONMENT], the defined database environments, see config.ENVIRONMENTS"
  print "    ",config.ENVIRONMENTS

def invalid_version(version):
  if version==None:
    usage()
    print
    print "error: invalid version"
    exit(1) 

def get_oracle_sid(parameters):
  oracle_sid=utils.get_parameter_value(parameters,'-sid=')
  if oracle_sid==None:
    oracle_sid=DEFAULT_ORACLE_SID
  return oracle_sid

def get_environment(parameters):
  environment=utils.get_parameter_value(parameters,'-env=')
  if environment==None:
    environment=DEFAULT_ENVIRONMENT
  return environment

def get_version(parameters):
  version=utils.get_parameter_value(parameters,'-version=')
  return version

def get_oracle_user(schema,environment):
  result=""
  for user in ORACLE_USERS:
    if user[0]==schema:
        user_environments=user[1]
        for user_environment in user_environments:
          if user_environment==environment:
            result=user[2]
            break
  return result


def get_oracle_passwd(schema,environment):
  result=""
  for user in ORACLE_USERS:
    if user[0]==schema:
       user_environments=user[1]
       for user_environment in user_environments:
         if user_environment==environment:
           result=user[3]
           break
  return result


def execute(oracle_sid, oracle_user, oracle_passwd, oracle_script, param1,param2):
  connect=oracle_user+'/'+oracle_passwd+'@'+oracle_sid
  script='@'+INSTALL_DIR+os.sep+'update.sql'
  result=subprocess.call(['sqlplus','-l','-s',connect , script, oracle_script, param1,param2])
  if result!=0:
    utils.show_errors()
    exit(1)


def get_previous_version(version):
  previous_version='1.0.0'
  folder=ALTER_DIR
  versions=utils.find_dirs(folder)  
  versions=version_utils.sort_as_versions(versions)
  versions.insert(0,previous_version) 
  for i in range(len(versions)):
    if versions[i]==version:
      previous_version=versions[i-1]
      break

  return previous_version

  
def check_version(oracle_sid,oracle_user,oracle_passwd,previous_version,version_select_statement):
   oracle_script=INSTALL_DIR+os.sep+'checkversion.sql'
   execute(oracle_sid,oracle_user,oracle_passwd, oracle_script,previous_version,version_select_statement)

def check_environment(oracle_sid,oracle_user,oracle_passwd,environment,environment_select_statement):
   oracle_script=INSTALL_DIR+os.sep+'checkenvironment.sql'
   execute(oracle_sid,oracle_user,oracle_passwd, oracle_script,environment,environment_select_statement)
   
def install_component(url, oracle_sid, oracle_user, oracle_passwd):
  result=subprocess.call(['python',url+os.sep+'setup.py','-sid='+oracle_sid,'-username='+oracle_user,'-password='+oracle_passwd,'-base='+BASE_DIR])
  if result!=0:
    exit(1)

def get_component_folder(url):
  component_filename=utils.get_filename(url)
  component_extension=utils.get_file_extension(url)
  component_name=component_filename.rstrip('.'+component_extension)
  return os.path.dirname(url)+os.sep+component_name

def execute_objects(folder,oracle_sid,oracle_user,oracle_passwd):
  files=utils.find_files(folder)
  for file in files:
    url=folder+os.sep+file
    if utils.get_file_extension(file).lower()=='zip':
      utils.extract(url)
      extract_folder=get_component_folder(url)
      install_component(extract_folder,oracle_sid,oracle_user,oracle_passwd)
      utils.remove_folder_recursive(extract_folder)  
    else:
      print url.split(ALTER_DIR)[1]
      execute(oracle_sid,oracle_user,oracle_passwd,url,'','')

def recompile(oracle_sid, oracle_user, oracle_passwd):
   oracle_script=INSTALL_DIR+os.sep+'recompile.sql'
   execute(oracle_sid,oracle_user,oracle_passwd, oracle_script,'','')

if __name__ == "__main__":

  print ""
  parameters=utils.get_parameters()

  if utils.is_parameter(parameters,'-h'):
    usage()
    exit(1)

  oracle_sid=get_oracle_sid(parameters)
  environment=get_environment(parameters)
  version=get_version(parameters)
  previous_version=get_previous_version(version)

  invalid_version(version)
  oracle_user=get_oracle_user(CHECK_VERSION_SCHEMA,environment)
  oracle_passwd=get_oracle_passwd(CHECK_VERSION_SCHEMA,environment)
  check_version(oracle_sid,oracle_user,oracle_passwd,previous_version,VERSION_SELECT_STATEMENT)
  check_environment(oracle_sid,oracle_user,oracle_passwd,environment,ENVIRONMENT_SELECT_STATEMENT)

  print "updating database "+oracle_sid+" using environment "+environment+" to version "+version
  for schema in SCHEMAS:

    oracle_user=get_oracle_user(schema,environment)
    oracle_passwd=get_oracle_passwd(schema,environment)
    for object in OBJECTS:
      
      # environment specific ddl objects
      folder=ALTER_DIR+os.sep+version+os.sep+schema+os.sep+'ddl'+os.sep+object+os.sep+environment
      execute_objects(folder,oracle_sid,oracle_user,oracle_passwd) 

      # global ddl objects
      folder=ALTER_DIR+os.sep+version+os.sep+schema+os.sep+'ddl'+os.sep+object
      execute_objects(folder,oracle_sid,oracle_user,oracle_passwd) 

    # environment specific dat objects
    folder=ALTER_DIR+os.sep+version+os.sep+schema+os.sep+'dat'+os.sep+environment
    execute_objects(folder,oracle_sid,oracle_user,oracle_passwd) 

    # global dat objects
    folder=ALTER_DIR+os.sep+version+os.sep+schema+os.sep+'dat'
    execute_objects(folder,oracle_sid,oracle_user,oracle_passwd) 

  for schema in SCHEMAS:
    print "compiling schema "+schema
    recompile(oracle_sid,oracle_user,oracle_passwd)


  print "database "+oracle_sid+" updated to version "+version
