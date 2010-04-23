#!/usr/bin/env python
import sys
import os
import subprocess
INSTALL_DIR=os.path.abspath(os.path.dirname(sys.argv[0]))
POVS_DIR=INSTALL_DIR.split('bin')[0]
BASE_DIR=os.path.abspath('.')
sys.path.append(BASE_DIR)
import config
import utils
DEFAULT_ORACLE_SID=config.DEFAULT_ORACLE_SID
DEFAULT_ENVIRONMENT=config.DEFAULT_ENVIRONMENT

SCHEMAS=config.SCHEMAS
ORACLE_USERS=config.ORACLE_USERS


def usage():
  print ""
  print "usage : unittest.py -sid=[ORACLE_SID] -env=[ENVIRONMENT]"
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

def execute(oracle_sid, oracle_user, oracle_passwd, oracle_script):
  connect=oracle_user+'/'+oracle_passwd+'@'+oracle_sid
  script='@'+INSTALL_DIR+os.sep+'update.sql'
  result=subprocess.call(['sqlplus','-l','-s',connect , script, oracle_script])
  if result!=0:
    utils.show_errors()
    exit(1)

def unittest(oracle_sid, oracle_user, oracle_passwd):
   oracle_script=INSTALL_DIR+os.sep+'unittest.sql'
   execute(oracle_sid,oracle_user,oracle_passwd, oracle_script)


if __name__ == "__main__":

  parameters=utils.get_parameters()
  
  if utils.is_parameter(parameters,'-h'):
    usage()
    exit(1)

  oracle_sid=get_oracle_sid(parameters)
  environment=get_environment(parameters)

  for schema in SCHEMAS:

    oracle_user=get_oracle_user(schema,environment)
    oracle_passwd=get_oracle_passwd(schema,environment)

    print "executing unit tests for schema "+schema
    unittest(oracle_sid,oracle_user,oracle_passwd);
