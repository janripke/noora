#!/usr/bin/env python
import sys
import os
import subprocess
__revision__ = "$Revision$"


NOORA_DIR=os.path.abspath(os.path.dirname(sys.argv[0]))
BASE_DIR=os.path.abspath('.')
sys.path.append(BASE_DIR)
import config
import utils
import version_utils

SCHEMES=config.SCHEMES
OBJECTS=config.CREATE_OBJECTS
ORACLE_USERS=config.ORACLE_USERS
ORACLE_SIDS=config.ORACLE_SIDS
DEFAULT_ENVIRONMENT=config.DEFAULT_ENVIRONMENT
ENVIRONMENTS=config.ENVIRONMENTS
VERSIONS=config.VERSIONS

def usage():
  print "Noora database installer, recreate.py"
  print "recreates the database objects of the defined schemes."
  
  print "-s= --sid=     required contains the tnsname of the database."
  print "-u= --scheme=  not required, contains the scheme of "
  print "               the database objects to drop."
  print "-e= --env=     not required, used for mapping "
  print "               the username and password."
  print "-nocompile     not required, disable the compilation of "
  print "               packages, triggers and views."  
  print "-m= --max=     not required, after the given version recreation will stop."
  print "-test          not required, executes the defined unit tests after recreation."

def revision():
  print "Noora database installer, recreate.py"
  print "revision :",__revision__

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
  
def has_version(version):
  for allowed_version in VERSIONS:
    if allowed_version.lower()==version.lower():
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

def get_scheme(parameters):
  scheme=utils.get_parameter_value_from_list(parameters,['-u=','--scheme='])
  return scheme
  
def invalid_scheme(scheme):
  if has_scheme(scheme)==False:
    usage()
    print
    print "the given schema is not valid for this project."
    exit(1)
    
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
    
def get_schemes(parameters):
  build_schemes=[]
  build_scheme=utils.get_parameter_value_from_list(parameters,['-u=','--scheme='])
  if build_scheme==None:
    build_schemes=SCHEMES
  else:
    build_schemes.append(build_scheme)
  return build_schemes    
    
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


def get_max_version(parameters):
  max_version=utils.get_parameter_value_from_list(parameters,['-m=','--max='])
  return max_version

def invalid_max_version(max_version):
  if has_version(max_version)==False:
    usage()
    print
    print "the given max version is not valid for this project."
    exit(1)


"""
Returns a list of the given list items, terminated by the given p_item.
The result is a shortened list of the given list.
If p_item is not found in the given list, the original list is returned.

items      : a list
p_item     ; the termination discriminator of the list.
returns    : the terminated list.
"""
def get_sub_list(items,p_item):
  sub_list=[]
  for item in items:
    sub_list.append(item)
    if item==p_item:
      break
  return sub_list

    
def drop_database(oracle_sid, scheme, environment):
  if scheme==None:
    result=subprocess.call(['python',NOORA_DIR+os.sep+'drop.py','--sid='+oracle_sid,'--env='+environment])
    if result!=0:
      exit(1)    
  else:
    result=subprocess.call(['python',NOORA_DIR+os.sep+'drop.py','--sid='+oracle_sid,'--scheme='+scheme,'--env='+environment])
    if result!=0:
      exit(1)


def create_database(oracle_sid, scheme, environment):
  if scheme==None:
    result=subprocess.call(['python',NOORA_DIR+os.sep+'create.py','--sid='+oracle_sid,'--env='+environment,'-nocompile'])
    if result!=0:
      exit(1)
  else:      
    result=subprocess.call(['python',NOORA_DIR+os.sep+'create.py','--sid='+oracle_sid,'--scheme='+scheme,'--env='+environment,'-nocompile'])
    if result!=0:
      exit(1)


def update_database(oracle_sid, scheme, environment, max_version):
  create_version=VERSIONS[0]
  versions=VERSIONS
  versions.remove(create_version)  
  versions=get_sub_list(versions,max_version)
  for version in versions:
    if scheme==None:
      result=subprocess.call(['python',NOORA_DIR+os.sep+'update.py','--version='+version,'--sid='+oracle_sid,'--env='+environment,'-nocompile'])        
      if result!=0:
        exit(1)
    else:
      result=subprocess.call(['python',NOORA_DIR+os.sep+'update.py','--version='+version,'--sid='+oracle_sid,'--scheme='+scheme,'--env='+environment,'-nocompile'])
      if result!=0:
        exit(1)

def unittest(oracle_sid, scheme, environment):
  if scheme==None:
    result=subprocess.call(['python',NOORA_DIR+os.sep+'unittest.py','--sid='+oracle_sid,'--env='+environment])
    if result!=0:
      exit(1)
  else:
    result=subprocess.call(['python',NOORA_DIR+os.sep+'unittest.py','--sid='+oracle_sid,'--scheme='+scheme,'--env='+environment])
    if result!=0:
      exit(1)
    
def execute(oracle_sid, oracle_user, oracle_passwd, oracle_script, param1, param2):
  connect=oracle_user+'/'+oracle_passwd+'@'+oracle_sid
  script='@'+NOORA_DIR+os.sep+'update.sql'
  result=subprocess.call(['sqlplus','-l','-s',connect , script, oracle_script, param1,param2])
  if result!=0:
    utils.show_errors()
    exit(1)

def recompile(oracle_sid, oracle_user, oracle_passwd):
   oracle_script=NOORA_DIR+os.sep+'recompile.sql'
   execute(oracle_sid,oracle_user,oracle_passwd, oracle_script,'','')



if __name__ == "__main__":

  parameters=utils.get_parameters()
  if utils.is_parameter(parameters,'-h'):
    usage()
    exit(1)

  if utils.is_parameter(parameters,'-r'):
    revision()
    exit(1)

  oracle_sid=get_oracle_sid(parameters)
  oracle_sid_not_none(oracle_sid)
  invalid_oracle_sid(oracle_sid)
  
  scheme=get_scheme(parameters)
  if scheme!=None:
    invalid_scheme(scheme)
  
  schemes=get_schemes(parameters)
  schemes_not_none(schemes)
  invalid_schemes(schemes)
  
  environment=get_environment(parameters)
  environment_not_none(environment)
  invalid_environment(environment)

  max_version=get_max_version(parameters)
  if max_version!=None:
    invalid_max_version(max_version)

  drop_database(oracle_sid,scheme,environment)
  create_database(oracle_sid,scheme,environment)
  update_database(oracle_sid,scheme,environment,max_version)
  
  if utils.is_parameter(parameters,'-nocompile')==False:
    for scheme in schemes:
      print "compiling scheme '"+scheme+"' in database '"+oracle_sid+"' using environment '"+environment+"'"
      oracle_user=get_oracle_user(scheme,environment)
      oracle_passwd=get_oracle_passwd(scheme,environment)
      recompile(oracle_sid, oracle_user, oracle_passwd)
      print "scheme '"+scheme+"' compiled."


  if utils.is_parameter(parameters,'-test'):
    for scheme in schemes:
      unittest(oracle_sid, scheme, environment)
