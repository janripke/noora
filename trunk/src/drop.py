#!/usr/bin/env python
import sys
import os
import subprocess
NOORA_DIR=os.path.abspath(os.path.dirname(sys.argv[0]))
DROP_DIR=NOORA_DIR+os.sep+'drop'
BASE_DIR=os.path.abspath('.')
sys.path.append(BASE_DIR)
import config
import utils

SCHEMES=config.SCHEMES
OBJECTS=config.DROP_OBJECTS
ORACLE_USERS=config.ORACLE_USERS
ORACLE_SIDS=config.ORACLE_SIDS
BLOCKED_ORACLE_SIDS=config.BLOCKED_ORACLE_SIDS
DEFAULT_ENVIRONMENT=config.DEFAULT_ENVIRONMENT
ENVIRONMENTS=config.ENVIRONMENTS

def usage():
  print "Noora database installer, drop.py"
  print "drops the database objects of the defined schemes."
  print "-s=  --sid=     required contains the tnsname of the database."
  print "-u=  --scheme=  not required, contains the scheme of "
  print "                the database objects to drop."
  print "-e=  --env=     not required, used for mapping "
  print "                the username and password."


def has_oracle_sid(oracle_sid):
  for allowed_oracle_sid in ORACLE_SIDS:
    if allowed_oracle_sid.lower()==oracle_sid.lower():
      return True
  return False
  
def has_scheme(scheme):
  for default_scheme in SCHEMES:
    if default_scheme.lower()==scheme.lower():
      return True
  return False
  
def has_environment(environment):
  for allowed_environment in ENVIRONMENTS:
    if allowed_environment.lower()==environment.lower():
      return True
  return False

def invalid_oracle_sid(oracle_sid):
  if has_oracle_sid(oracle_sid)==False:
    usage()
    print
    print "the given oracle_sid is not valid for this project."
    exit(1)

def blocked_oracle_sid(oracle_sid):
  for blocked_oracle_sid in BLOCKED_ORACLE_SIDS:
    if blocked_oracle_sid.lower()==oracle_sid.lower():
      usage()
      print
      print "dropping is blocked for the given oracle_sid."
      exit(1)
      
def oracle_sid_not_none(oracle_sid):
  if oracle_sid==None:
    usage()
    print
    print "no oracle_sid was given"
    exit(1)

def get_oracle_sid(parameters):
  oracle_sid=utils.get_parameter_value_from_list(parameters,['-s=','--sid='])
  return oracle_sid

def get_schemes(parameters):
  build_schemes=[]
  build_scheme=utils.get_parameter_value_from_list(parameters,['-u=','--scheme='])
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
    
def get_environment(parameters):
  environment=utils.get_parameter_value_from_list(parameters,['-e=','--env='])    
  if environment==None:
    environment=DEFAULT_ENVIRONMENT
  return environment    
  
def invalid_environment(environment):
  if has_environment(environment)==False:
    usage()
    print
    print "the given environment is not valid for this project."
    exit(1)
    
def environment_not_none(environment):
  if environment==None:
    usage()
    print
    print "no environment was found."
    exit(1)  

def get_oracle_user(scheme,environment):
  result=""
  for user in ORACLE_USERS:
    if user[0]==scheme:
        user_environments=user[1]
        for user_environment in user_environments:
          if user_environment==environment:
            result=user[2]
            break
  return result

def get_oracle_passwd(scheme,environment):
  result=""
  for user in ORACLE_USERS:
    if user[0]==scheme:
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
  script='@'+NOORA_DIR+os.sep+'drop.sql'
  result=subprocess.call(['sqlplus','-l','-s',connect , script, oracle_script,script_param])
  if result!=0:
    utils.show_errors()
    exit(1)

def execute_objects(folder,schema,oracle_sid,oracle_user,oracle_passwd,schema_users):
  files=utils.find_files(folder)
  for file in files:
    url=folder+os.sep+file
    print schema+':'+url.split(NOORA_DIR)[1]
    execute(oracle_sid,oracle_user,oracle_passwd,url,schema_users)

if __name__ == "__main__":
  print ""
  parameters=utils.get_parameters()
  if utils.is_parameter(parameters,'-h'):
    usage()
    exit(1)
  
  oracle_sid=get_oracle_sid(parameters)
  oracle_sid_not_none(oracle_sid)
  invalid_oracle_sid(oracle_sid)
  blocked_oracle_sid(oracle_sid)
  
  schemes=get_schemes(parameters)
  schemes_not_none(schemes)
  invalid_schemes(schemes)
  
  environment=get_environment(parameters)
  environment_not_none(environment)
  invalid_environment(environment)

  #schema_users=get_schema_users()
  
  for scheme in schemes:
    print "dropping scheme '"+scheme+"' in database '"+oracle_sid+"' using environment '"+environment+"'"
    oracle_user=get_oracle_user(scheme,environment)
    oracle_passwd=get_oracle_passwd(scheme,environment)
    for object in OBJECTS:
      
      # ddl objects
      folder=DROP_DIR+os.sep+object
      execute_objects(folder,scheme,oracle_sid,oracle_user,oracle_passwd,'')  


    print "scheme '"+scheme+"' dropped."
