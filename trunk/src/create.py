#!/usr/bin/env python
import sys
import os
import subprocess
INSTALL_DIR=os.path.abspath(os.path.dirname(sys.argv[0]))
POVS_DIR=INSTALL_DIR.split('bin')[0]
BASE_DIR=os.path.abspath('.')
CREATE_DIR=BASE_DIR+os.sep+'create'
sys.path.append(BASE_DIR)
import config
import utils

SCHEMAS=config.SCHEMAS
SCHEMA_OBJECTS=config.CREATE_SCHEMA_OBJECTS
ORACLE_USERS=config.ORACLE_USERS
DEFAULT_ORACLE_SID=config.DEFAULT_ORACLE_SID
DEFAULT_ENVIRONMENT=config.DEFAULT_ENVIRONMENT

def usage():
  print "Noora database installer, create.py"
  print "executes the defined baseline scripts in the create folder"
  print "-sid=[ORACLE_SID]"
  print "-env=[ENVIRONMENT], the defined database environments, see config.ENVIRONMENTS"
  print "    ",config.ENVIRONMENTS

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


# retrieves the oracle schemas in a string.
# remark : the schemas are seperated by ;
def get_schema_users():
  result=""
  for schema in SCHEMAS:
    for oracle_user in ORACLE_USERS:
      if oracle_user[0]==schema:
        result=result+oracle_user[2]+';'
  return result.rstrip(';')

def install_component(url, oracle_sid, oracle_user, oracle_passwd):
  result=subprocess.call(['python',url+os.sep+'setup.py','-sid='+oracle_sid,'-username='+oracle_user,'-password='+oracle_passwd,'-base='+BASE_DIR])
  if result!=0:
    exit(1)

def get_component_folder(url):
  component_filename=utils.get_filename(url)
  component_extension=utils.get_file_extension(url)
  component_name=component_filename.rstrip('.'+component_extension)
  return os.path.dirname(url)+os.sep+component_name


def execute(oracle_sid, oracle_user, oracle_passwd, oracle_script,script_param):
  connect=oracle_user+'/'+oracle_passwd+'@'+oracle_sid
  script='@'+INSTALL_DIR+os.sep+'create.sql'
  result=subprocess.call(['sqlplus','-l','-s',connect , script, oracle_script,script_param])
  if result!=0:
    utils.show_errors()
    exit(1)

def execute_objects(folder,oracle_sid,oracle_user,oracle_passwd,schema_users):
  files=utils.find_files(folder)
  for file in files:
    url=folder+os.sep+file
    if utils.get_file_extension(file).lower()=='zip':
      utils.extract(url)
      extract_folder=get_component_folder(url)
      install_component(extract_folder,oracle_sid,oracle_user,oracle_passwd)
      utils.remove_folder_recursive(extract_folder)  
    else:
      print url.split(BASE_DIR)[1]
      execute(oracle_sid,oracle_user,oracle_passwd,url,schema_users)

def recompile(oracle_sid, oracle_user, oracle_passwd):
   oracle_script=INSTALL_DIR+os.sep+'recompile.sql'
   execute(oracle_sid,oracle_user,oracle_passwd, oracle_script,'')

def get_base_dir():
  return BASE_DIR

if __name__ == "__main__":
  
  print ""
  parameters=utils.get_parameters()

  if utils.is_parameter(parameters,'-h'):
    usage()
    exit(1)

  oracle_sid=get_oracle_sid(parameters)
  environment=get_environment(parameters)

  schema_users=get_schema_users()

  print "creating database "+oracle_sid+" using environment "+environment
  for schema in SCHEMAS:

    oracle_user=get_oracle_user(schema,environment)
    oracle_passwd=get_oracle_passwd(schema,environment)
    for object in SCHEMA_OBJECTS:

      # environment specific ddl objects
      folder=CREATE_DIR+os.sep+schema+os.sep+'ddl'+os.sep+object+os.sep+environment
      execute_objects(folder,oracle_sid,oracle_user,oracle_passwd,schema_users)
      
      # global ddl objects
      folder=CREATE_DIR+os.sep+schema+os.sep+'ddl'+os.sep+object
      execute_objects(folder,oracle_sid,oracle_user,oracle_passwd,schema_users)

    # environment specific dat objects
    folder=CREATE_DIR+os.sep+schema+os.sep+'dat'+os.sep+environment
    execute_objects(folder,oracle_sid,oracle_user,oracle_passwd,schema_users)

    # global dat objects
    folder=CREATE_DIR+os.sep+schema+os.sep+'dat'
    execute_objects(folder,oracle_sid,oracle_user,oracle_passwd,schema_users)

  for schema in SCHEMAS:
    print "compiling schema "+schema
    recompile(oracle_sid,oracle_user,oracle_passwd)

  print "database "+oracle_sid+" created."
