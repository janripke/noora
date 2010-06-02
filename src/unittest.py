#!/usr/bin/env python
import sys
import os
import subprocess
NOORA_DIR=os.path.abspath(os.path.dirname(sys.argv[0]))
BASE_DIR=os.path.abspath('.')
sys.path.append(BASE_DIR)
import config
import utils

SCHEMES=config.SCHEMES
ORACLE_USERS=config.ORACLE_USERS
ORACLE_SIDS=config.ORACLE_SIDS
DEFAULT_ENVIRONMENT=config.DEFAULT_ENVIRONMENT
ENVIRONMENTS=config.ENVIRONMENTS

def usage():
  print "Noora database installer, unittest.py."
  print "executes unit tests. Uses the noora unit test framework."
  print "remarks : a unit test is always a package. A package that start with UT_ is considered"
  print "          as a unit test. Excluded are the packages UT_ASSERT and UT_RUN."

  print "-s= --sid=     required contains the tnsname of the database."
  print "-u= --scheme=  not required, contains the scheme of "
  print "               the unit tests to execute."
  print "-e= --env=     not required, used for mapping "
  print "               the username and password."

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


def execute(oracle_sid, oracle_user, oracle_passwd, oracle_script):
  connect=oracle_user+'/'+oracle_passwd+'@'+oracle_sid
  script='@'+NOORA_DIR+os.sep+'update.sql'
  result=subprocess.call(['sqlplus','-l','-s',connect , script, oracle_script])
  if result!=0:
    utils.show_errors()
    exit(1)

def unittest(oracle_sid, oracle_user, oracle_passwd):
   oracle_script=NOORA_DIR+os.sep+'unittest.sql'
   execute(oracle_sid,oracle_user,oracle_passwd, oracle_script)


if __name__ == "__main__":

  parameters=utils.get_parameters()
  
  if utils.is_parameter(parameters,'-h'):
    usage()
    exit(1)

  oracle_sid=get_oracle_sid(parameters)
  oracle_sid_not_none(oracle_sid)
  invalid_oracle_sid(oracle_sid)
  
  schemes=get_schemes(parameters)
  schemes_not_none(schemes)
  invalid_schemes(schemes)
  
  environment=get_environment(parameters)
  environment_not_none(environment)
  invalid_environment(environment)

  for scheme in schemes:
    print "executing unit tests for scheme '"+scheme+"' in database '"+oracle_sid+"' using environment '"+environment+"'"
    oracle_user=get_oracle_user(scheme,environment)
    oracle_passwd=get_oracle_passwd(scheme,environment)
    unittest(oracle_sid,oracle_user,oracle_passwd)
    print "unit tests for scheme '"+scheme+"' executed."
