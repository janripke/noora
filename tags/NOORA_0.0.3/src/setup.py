#!/usr/bin/env python
import sys
import os
import subprocess
import component_utils as utils
import component

INSTALL_DIR=os.path.abspath(os.path.dirname(sys.argv[0]))
OBJECTS=['usr','dbl','dir','seq','syn','tab','cst','vw','prc','pkg','jar','trg','idx','gra']
COMPONENT_NAME=component.COMPONENT_NAME
COMPONENT_VERSION=component.COMPONENT_VERSION
COMPONENT_CREATE_VERSION=component.COMPONENT_CREATE_VERSION

def usage():
  print ""
  print "usage : setup.py -sid=[ORACLE_SID] -username=[username] -password=[password] [-base=]"
  print ""

def no_oracle_sid(oracle_sid):
  if oracle_sid==None:
    usage()
    print
    print "error: no oracle sid given."
    exit(1) 

def no_oracle_user(oracle_user):
  if oracle_user==None:
    usage()
    print
    print "error: no oracle user given."
    exit(1) 

def no_oracle_passwd(oracle_passwd):
  if oracle_passwd==None:
    usage()
    print
    print "error: no oracle password given."
    exit(1) 

def get_oracle_sid(parameters):
  oracle_sid=utils.get_parameter_value(parameters,'-sid=')
  return oracle_sid

def get_username(parameters):
  username=utils.get_parameter_value(parameters,'-username=')
  return username

def get_password(parameters):
  password=utils.get_parameter_value(parameters,'-password=')
  return password

def get_base_folder(parameters):
  base_folder=utils.get_parameter_value(parameters,'-base=')
  return base_folder

def get_sql_version_script(component_name,component_version,component_create_version):
  if component_version==component_create_version:
    stream=config.COMPONENT_INSERT_STATEMENT
  else:
    stream=config.COMPONENT_UPDATE_STATEMENT
  stream=stream.replace('<version>',component_version)
  stream=stream.replace('<name>',component_name)
  return stream
   
    

def execute(oracle_sid, oracle_user, oracle_passwd, oracle_script):
  connect=oracle_user+'/'+oracle_passwd+'@'+oracle_sid
  script='@'+INSTALL_DIR+os.sep+'setup.sql'
  result=subprocess.call(['sqlplus','-l','-s',connect , script, oracle_script])
  if result!=0:
    utils.show_errors()
    exit(1)


if __name__ == "__main__":
  
  print ""
  parameters=utils.get_parameters()

  if utils.is_parameter(parameters,'-h'):
    usage()
    exit(1)

  oracle_sid=get_oracle_sid(parameters)
  oracle_user=get_username(parameters)
  oracle_passwd=get_password(parameters)

  no_oracle_sid(oracle_sid)
  no_oracle_user(oracle_user)
  no_oracle_passwd(oracle_passwd)

  base_folder=get_base_folder(parameters)
  if base_folder!=None:
    sys.path.append(base_folder)
    import config
    dat_folder=INSTALL_DIR+os.sep+'dat'+os.sep
    if utils.dir_is_not_present(dat_folder):
      os.mkdir(dat_folder)
    sql_script=get_sql_version_script(COMPONENT_NAME,COMPONENT_VERSION,COMPONENT_CREATE_VERSION)
    utils.write_file(dat_folder+'version.sql', sql_script)


  print "installing component "+component.COMPONENT_NAME+'_'+component.COMPONENT_VERSION


  for object in OBJECTS:
      
    # ddl objects
    folder=INSTALL_DIR+os.sep+'ddl'+os.sep+object
    files=utils.find_files(folder)
    for file in files:
      oracle_script=folder+os.sep+file
      print oracle_script.split(INSTALL_DIR)[1]
      execute(oracle_sid,oracle_user,oracle_passwd,oracle_script)

  # global dat files
  folder=INSTALL_DIR+os.sep+'dat'
  files=utils.find_files(folder)
  for file in files:
    oracle_script=folder+os.sep+file
    print oracle_script.split(INSTALL_DIR)[1]
    execute(oracle_sid,oracle_user,oracle_passwd,oracle_script)


  print "component "+component.COMPONENT_NAME+'_'+component.COMPONENT_VERSION+" created."
