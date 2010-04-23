#!/usr/bin/env python
import sys
import os
import subprocess
NONA_DIR=os.path.abspath(os.path.dirname(sys.argv[0]))
BASE_DIR=os.path.abspath('.')
sys.path.append(BASE_DIR)
import config
import utils

SCHEMAS=config.SCHEMAS
ORACLE_USERS=config.ORACLE_USERS
DEFAULT_ORACLE_SID=config.DEFAULT_ORACLE_SID
DEFAULT_ENVIRONMENT=config.DEFAULT_ENVIRONMENT

def usage():
  print ""
  print "usage : install_schema.py"
  print "  -sid=[ORACLE_SID], the oracle sid to use."
  print "                     if none given the default oracle sid is used."
  print "  -env=[ENVIRONMENT], the defined database environments"
  print "                      if none is given the default environment is used."
  print "                      see config.ENVIRONMENTS."
  print "                      ",config.ENVIRONMENTS
  print "  -schema=[SCHEMA], the schema to use, "
  print "                    if none is given all the defined schemas are build."
  print "                    see config.schemas."
  print "                    ",config.SCHEMAS



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

def get_install_schemas(parameters):
  build_schemas=[]
  build_schema=utils.get_parameter_value(parameters,'-schema=')
  if build_schema==None:
    build_schemas=SCHEMAS
  else:
    build_schemas.append(build_schema)
  return build_schemas

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


def get_install_folder(parameters):
  install_folder=utils.get_parameter(parameters)
  return install_folder

def install_folder_not_none(install_folder):
  if install_folder==None:
    usage()
    print
    print "error: no install folder was given"
    exit(1) 


def invalid_install_folder(install_folder):
  if utils.dir_is_not_present(install_folder):
    usage()
    print "error: invalid install folder, folder not present"
    exit(1)

def execute(oracle_sid, oracle_user, oracle_passwd, oracle_script,script_param):
  connect=oracle_user+'/'+oracle_passwd+'@'+oracle_sid
  script='@'+NONA_DIR+os.sep+'create.sql'
  print script
  result=subprocess.call(['sqlplus','-l','-s',connect , script, oracle_script,script_param])
  if result!=0:
    utils.show_errors()
    exit(1)

def recompile(oracle_sid, oracle_user, oracle_passwd):
   oracle_script=NONA_DIR+os.sep+'recompile.sql'
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
  install_schemas=get_install_schemas(parameters)
  install_folder=get_install_folder(parameters)

  install_folder_not_none(install_folder)
  invalid_install_folder(install_folder)


  print "creating database "+oracle_sid+" using environment "+environment
  for schema in install_schemas:

    oracle_user=get_oracle_user(schema,environment)
    oracle_passwd=get_oracle_passwd(schema,environment)

    os.chdir(install_folder+os.sep+schema)
    oracle_script='install_schema.sql'
    print oracle_script
    os.chdir('..'+os.sep+'..')
    #execute(oracle_sid,oracle_user,oracle_passwd,oracle_script,environment)
    
  for schema in SCHEMAS:
    print "compiling schema "+schema
    recompile(oracle_sid,oracle_user,oracle_passwd)

  print "database "+oracle_sid+" created."
