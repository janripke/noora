#!/usr/bin/env python
import sys
import os
import subprocess
NOORA_DIR=os.path.abspath(os.path.dirname(sys.argv[0]))
BASE_DIR=os.path.abspath('.')
CREATE_DIR=BASE_DIR+os.sep+'create'
sys.path.append(BASE_DIR)
import config
import utils

SCHEMES=config.SCHEMES
OBJECTS=config.CREATE_OBJECTS
ORACLE_USERS=config.ORACLE_USERS
ORACLE_SIDS=config.ORACLE_SIDS
DEFAULT_ENVIRONMENT=config.DEFAULT_ENVIRONMENT
ENVIRONMENTS=config.ENVIRONMENTS

def usage():
  print "Noora database installer, create.py"
  print "executes the defined baseline scripts in the create folder"
  print "-s= --sid=     required contains the tnsname of the database."
  print "-u= --scheme=  not required, contains the scheme of "
  print "               the database objects to drop."
  print "-e= --env=     not required, used for mapping "
  print "               the username and password."
  print "-nocompile     not required, disable the compilation of "
  print "               packages, triggers and views."

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
  script='@'+NOORA_DIR+os.sep+'create.sql'
  result=subprocess.call(['sqlplus','-l','-s',connect , script, oracle_script,script_param])
  if result!=0:
    utils.show_errors()
    exit(1)

def execute_objects(folder,oracle_sid,oracle_user,oracle_passwd,script_param):
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
      execute(oracle_sid,oracle_user,oracle_passwd,url,script_param)

def recompile(oracle_sid, oracle_user, oracle_passwd):
   oracle_script=NOORA_DIR+os.sep+'recompile.sql'
   execute(oracle_sid,oracle_user,oracle_passwd, oracle_script,'')

if __name__ == "__main__":
  
  print ""
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
    print "creating scheme '"+scheme+"' in database '"+oracle_sid+"' using environment '"+environment+"'"
    oracle_user=get_oracle_user(scheme,environment)
    oracle_passwd=get_oracle_passwd(scheme,environment)
    for object in OBJECTS:

      # environment specific ddl objects
      folder=CREATE_DIR+os.sep+scheme+os.sep+'ddl'+os.sep+object+os.sep+environment
      execute_objects(folder,oracle_sid,oracle_user,oracle_passwd,'')
      
      # global ddl objects
      folder=CREATE_DIR+os.sep+scheme+os.sep+'ddl'+os.sep+object
      execute_objects(folder,oracle_sid,oracle_user,oracle_passwd,'')

    # environment specific dat objects
    folder=CREATE_DIR+os.sep+scheme+os.sep+'dat'+os.sep+environment
    execute_objects(folder,oracle_sid,oracle_user,oracle_passwd,'')

    # global dat objects
    folder=CREATE_DIR+os.sep+scheme+os.sep+'dat'
    execute_objects(folder,oracle_sid,oracle_user,oracle_passwd,'')
    
    print "scheme '"+scheme+"' created."

  if utils.is_parameter(parameters,'-nocompile')==False:
    for scheme in schemes:
      print "compiling scheme '"+scheme+"' in database '"+oracle_sid+"' using environment '"+environment+"'"
      oracle_user=get_oracle_user(scheme,environment)
      oracle_passwd=get_oracle_passwd(scheme,environment)
      recompile(oracle_sid,oracle_user,oracle_passwd)
      print "scheme '"+scheme+"' compiled."

