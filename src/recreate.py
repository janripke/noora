#!/usr/bin/env python
import sys
import os
import subprocess
__version__ = "$Revision: $"


INSTALL_DIR=os.path.abspath(os.path.dirname(sys.argv[0]))
POVS_DIR=INSTALL_DIR.split('bin')[0]
BASE_DIR=os.path.abspath('.')
ALTER_DIR=BASE_DIR+os.sep+'alter'
sys.path.append(BASE_DIR)
import config
import utils
import version_utils

DEFAULT_ORACLE_SID=config.DEFAULT_ORACLE_SID
DEFAULT_ENVIRONMENT=config.DEFAULT_ENVIRONMENT
BLOCKED_ENVIRONMENTS=config.BLOCKED_ENVIRONMENTS

def usage():
  print ""
  print "usage : recreate.py"
  print "-sid=[ORACLE_SID], the oracle sid to use."
  print "-env=[ENVIRONMENT], the defined database environments, see config.ENVIRONMENTS"
  print "    ",config.ENVIRONMENTS
  print "-max=[MAX_VERSION], after this version recreation will stop."
  print "-test, execute unittests after recreation."

def version():
  print ""
  print "pyois   : recreate.py"
  print "version :",__version__

def check_blocked_environments(environment):
  for blocked_environment in BLOCKED_ENVIRONMENTS:
    if environment.lower()==blocked_environment.lower():
      print "recreation is not allowed for this environment."
      exit(1) 
 
"""
Returns the oracle_sid from the command line list parameters.
When no sid is given, the default oracle sid in config.py is used.

parameters : the command line list.
returns    : the oracle sid.
"""
def get_oracle_sid(parameters):
  oracle_sid=utils.get_parameter_value(parameters,'-sid=')
  if oracle_sid==None:
    oracle_sid=DEFAULT_ORACLE_SID
  return oracle_sid


"""
Returns the database environment from the command line list parameters.
When no environment is given, the default environment in config.py is used.
The environment option is used to install environment specific scripts.

parameters : the command line list.
returns    : the environment.
"""
def get_environment(parameters):
  environment=utils.get_parameter_value(parameters,'-env=')
  if environment==None:
    environment=DEFAULT_ENVIRONMENT
  return environment


"""
Returns the max version from the command line list parameters.
The max version option is used to terminate the installation after the given version is installed.
This is the version given in the alter folder.

parameters : the command line list.
returns    : the max version.
"""
def get_max_version(parameters):
  max_version=utils.get_parameter_value(parameters,'-max=')
  return max_version


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

    
def drop_database(oracle_sid,environment):
  result=subprocess.call(['python',INSTALL_DIR+os.sep+'drop.py','-sid='+oracle_sid,'-env='+environment])
  if result!=0:
    exit(1)


def create_database(oracle_sid, environment):
  result=subprocess.call(['python',INSTALL_DIR+os.sep+'create.py','-sid='+oracle_sid,'-env='+environment])
  if result!=0:
    exit(1)


def update_database(oracle_sid, environment,max_version):
  folder=ALTER_DIR
  versions=utils.find_dirs(folder)
  versions=version_utils.sort_as_versions(versions)
  versions=get_sub_list(versions,max_version)
  for version in versions:
    result=subprocess.call(['python',INSTALL_DIR+os.sep+'update.py','-version='+version,'-sid='+oracle_sid,'-env='+environment])
    if result!=0:
      exit(1)


def replace_source(oracle_sid, environment):
  result=subprocess.call(['python',INSTALL_DIR+os.sep+'replace_source.py','-sid='+oracle_sid,'-env='+environment])
  if result!=0:
    exit(1)


def unittest(oracle_sid,environment):
  result=subprocess.call(['python',INSTALL_DIR+os.sep+'unittest.py','-sid='+oracle_sid,'-env='+environment])
  if result!=0:
    exit(1)

if __name__ == "__main__":

  parameters=utils.get_parameters()
  if utils.is_parameter(parameters,'-h'):
    usage()
    exit(1)

  if utils.is_parameter(parameters,'-v'):
    version()
    exit(1)

  oracle_sid=get_oracle_sid(parameters)
  environment=get_environment(parameters)
  max_version=get_max_version(parameters)
  check_blocked_environments(environment)

  drop_database(oracle_sid,environment)
  create_database(oracle_sid,environment)
  update_database(oracle_sid,environment,max_version)
  

  print ""
  if utils.is_parameter(parameters,'-test'):
    unittest(oracle_sid,environment)
