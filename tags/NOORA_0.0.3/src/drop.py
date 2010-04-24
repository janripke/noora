#!/usr/bin/env python
import sys
import os
import subprocess
INSTALL_DIR=os.path.abspath(os.path.dirname(sys.argv[0]))
DROP_DIR=INSTALL_DIR+os.sep+'drop'
POVS_DIR=INSTALL_DIR.split('bin')[0]
BASE_DIR=os.path.abspath('.')
sys.path.append(BASE_DIR)
import config
import utils

SCHEMAS=config.SCHEMAS
OBJECTS=config.DROP_OBJECTS
ORACLE_USERS=config.ORACLE_USERS
DEFAULT_ORACLE_SID=config.DEFAULT_ORACLE_SID
DEFAULT_ENVIRONMENT=config.DEFAULT_ENVIRONMENT
BLOCKED_ENVIRONMENTS=config.BLOCKED_ENVIRONMENTS

def usage():
  print ""
  print "usage : drop.py -sid=[ORACLE_SID] -env=[ENVIRONMENT]"
  print "-env=[ENVIRONMENT], the defined database environments, see config.ENVIRONMENTS"
  print "    ",config.ENVIRONMENTS


def check_blocked_environments(environment):
  for blocked_environment in BLOCKED_ENVIRONMENTS:
    if environment.lower()==blocked_environment.lower():
      print "recreation is not allowed for this environment."
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


def execute(oracle_sid, oracle_user, oracle_passwd, oracle_script,script_param):
  connect=oracle_user+'/'+oracle_passwd+'@'+oracle_sid
  script='@'+INSTALL_DIR+os.sep+'drop.sql'
  result=subprocess.call(['sqlplus','-l','-s',connect , script, oracle_script,script_param])
  if result!=0:
    utils.show_errors()
    exit(1)

def get_base_dir():
  return BASE_DIR

def get_povs_dir():
  return POVS_DIR


def execute_objects(folder,schema,oracle_sid,oracle_user,oracle_passwd,schema_users):
  files=utils.find_files(folder)
  for file in files:
    url=folder+os.sep+file
    if utils.get_file_extension(file).lower()=='zip':
      utils.extract(url)
      extract_folder=get_component_folder(url)
      install_component(extract_folder,oracle_sid,oracle_user,oracle_passwd)
      utils.remove_folder_recursive(extract_folder)  
    else:
      print schema+':'+url.split(get_povs_dir())[1]
      execute(oracle_sid,oracle_user,oracle_passwd,url,schema_users)

if __name__ == "__main__":
  print ""
  parameters=utils.get_parameters()
  if utils.is_parameter(parameters,'-h'):
    usage()
    exit(1)
  oracle_sid=get_oracle_sid(parameters)
  environment=get_environment(parameters)
  check_blocked_environments(environment)

  schema_users=get_schema_users()
  
  print "dropping database "+oracle_sid+" using environment "+environment
 
  for schema in SCHEMAS:

    oracle_user=get_oracle_user(schema,environment)
    oracle_passwd=get_oracle_passwd(schema,environment)

    for object in OBJECTS:
      
      # ddl objects
      folder=DROP_DIR+os.sep+object
      execute_objects(folder,schema,oracle_sid,oracle_user,oracle_passwd,schema_users)  


  print "database "+oracle_sid+" dropped."
