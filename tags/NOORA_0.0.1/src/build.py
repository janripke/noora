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
SCHEMA_OBJECTS=config.CREATE_SCHEMA_OBJECTS
VERSIONS=config.VERSIONS
ENVIRONMENTS=config.ENVIRONMENTS

def usage():
  print ""
  print "usage : build.py "
  print "  -version=[VERSION], required, the version folder to scan."
  print "  -schema=[SCHEMA], the schema to use, "
  print "               if none is given all the defined schemas are build."
  print "               see config.schemas."
  print "              ",config.SCHEMAS


def get_build_schemas(parameters):
  build_schemas=[]
  build_schema=utils.get_parameter_value_from_list(parameters,['-s=','-schema='])
  if build_schema==None:
    build_schemas=SCHEMAS
  else:
    build_schemas.append(build_schema)
  return build_schemas

def get_version(parameters):
  version=utils.get_parameter_value_from_list(parameters,['-v=','-version='])
  return version

def has_version(p_version):
  for version in VERSIONS:
    if version==p_version:
      return True
  return False

def invalid_version(p_version):
  if has_version(p_version)==False:
    usage()
    print
    print "error: an invalid version was given"
    exit(1)

def get_build_folder(p_version):
  if p_version==VERSIONS[0]:
    result='create'
  else:
    result='alter'+os.sep+p_version
  return result

def invalid_build_folder(build_folder):
  if utils.dir_is_not_present(build_folder):
    usage()
    print
    print "error: invalid build folder, folder not present"
    exit(1)

def version_not_none(version):
  if version==None:
    usage()
    print
    print "error: no version was given"
    exit(1)

def is_item_not_present(p_items, p_item):
  result=True
  for item in p_items:
    if item==p_item:
      result=False
      break
  return result


def append_not_present(p_items, p_item):
  result=p_items
  if is_item_not_present(p_items, p_item):
    result.append(p_item)
  return result


if __name__ == "__main__":

  print
  parameters=utils.get_parameters()

  if utils.is_parameter(parameters,'-h'):
    usage()
    exit(1)

  build_schemas=get_build_schemas(parameters)
  version=get_version(parameters)
  version_not_none(version)
  invalid_version(version)
  build_folder=get_build_folder(version)
  invalid_build_folder(build_folder)

  install_scripts=[]
  for schema in build_schemas:
    for object in SCHEMA_OBJECTS:  
      for environment in ENVIRONMENTS:

        # environment specific ddl objects
        folder=build_folder+os.sep+schema+os.sep+'ddl'+os.sep+object+os.sep+environment
        files=utils.find_files(folder)
        if len(files)!=0:
          filename='install.sql'
          url=folder+os.sep+filename

          stream=''          
          if os.path.isfile(url):
            stream=utils.read_file(url)

          scripts=stream.split(chr(10))
          for file in files:
            scripts=append_not_present(scripts,'@@'+file)

          synchronized_scripts=scripts
          for script in scripts:
            if is_item_not_present(files,script.replace('@@','')):
              synchronized_scripts.remove(script)
              
          stream = chr(10).join(synchronized_scripts)              
          utils.write_file(url,stream)
          print url
          install_scripts=append_not_present(install_scripts,'@@ddl/'+object+'/&ENVIRONMENT/install.sql')          

      # global ddl objects
      folder=build_folder+os.sep+schema+os.sep+'ddl'+os.sep+object
      files=utils.find_files(folder)
      if len(files)!=0:
        filename='install.sql'
        url=folder+os.sep+filename
        
        stream=''          
        if os.path.isfile(url):
          stream=utils.read_file(url)

        scripts=stream.split(chr(10))
        for file in files:
          scripts=append_not_present(scripts,'@@'+file)

        synchronized_scripts=scripts
        for script in scripts:
          if is_item_not_present(files,script.replace('@@','')):
            synchronized_scripts.remove(script)
           
        stream = chr(10).join(synchronized_scripts)              
 
        utils.write_file(url,stream)
        print url
        install_scripts=append_not_present(install_scripts,'@@ddl/'+object+'/install.sql')

    for environment in ENVIRONMENTS:

      # environment specific dat objects
      folder=build_folder+os.sep+schema+os.sep+'dat'+os.sep+environment
      files=utils.find_files(folder)

      if len(files)!=0:
        filename='install.sql'
        url=folder+os.sep+filename
        
        stream=''          
        if os.path.isfile(url):
          stream=utils.read_file(url)

        scripts=stream.split(chr(10))
        for file in files:
          scripts=append_not_present(scripts,'@@'+file)

        synchronized_scripts=scripts
        for script in scripts:
          if is_item_not_present(files,script.replace('@@','')):
            synchronized_scripts.remove(script)
              
        stream = chr(10).join(synchronized_scripts)             
 
        utils.write_file(url,stream)
        print url
        install_scripts=append_not_present(install_scripts,'@@dat/&ENVIRONMENT/install.sql')

    # global dat objects
    folder=build_folder+os.sep+schema+os.sep+'dat'
    files=utils.find_files(folder)

    if len(files)!=0:
      filename='install.sql'
      url=folder+os.sep+filename
      
      stream=''          
      if os.path.isfile(url):
        stream=utils.read_file(url)

      scripts=stream.split(chr(10))
      for file in files:
        scripts=append_not_present(scripts,'@@'+file)

      synchronized_scripts=scripts
      for script in scripts:
        if is_item_not_present(files,script.replace('@@','')):
          synchronized_scripts.remove(script)
              
      stream = chr(10).join(synchronized_scripts)            
 
      utils.write_file(url,stream)
      print url
      install_scripts=append_not_present(install_scripts,'@@dat/install.sql')

  # create install_schema.sql script
  install_schema=utils.read_file(NONA_DIR+os.sep+'install_schema.sql')
  if len(install_scripts)!=0:
    stream=''
    url=build_folder+os.sep+schema+os.sep+'install_schema.sql'
    for item in install_scripts:
      stream=stream+item+chr(10)
    install_schema=install_schema.replace('<scripts>',stream)
    utils.write_file(url,install_schema)
    print url,'created.'



