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
OBJECTS=config.CREATE_OBJECTS
VERSIONS=config.VERSIONS
ENVIRONMENTS=config.ENVIRONMENTS

def usage():
  print "NoOra database installer, build.py"
  print "creates installation scripts"
  print "-u= --scheme=  not required, contains the scheme."
  print "-v= --verion=  not required, contains the version."


def has_scheme(scheme):
  for default_scheme in SCHEMES:
    if default_scheme.lower()==scheme.lower():
      return True
  return False

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

def has_version(version):
  for allowed_version in VERSIONS:
    if allowed_version.lower()==version.lower():
      return True
  return False 

def get_versions(parameters):
  build_versions=[]
  build_version=utils.get_parameter_value_from_list(parameters,['-v=','--version='])
  if build_version==None:
    build_versions=VERSIONS
  else:
    build_versions.append(build_version)
  return build_versions

def invalid_versions(versions):
  for version in versions:
    if has_version(version)==False:
      usage()
      print
      print "the given version is not valid for this project."
      exit(1)

def get_build_folder(version):
  create_version=VERSIONS[0]
  if create_version==version:
    version_folder=BASE_DIR+os.sep+'create'
  else:
    version_folder=BASE_DIR+os.sep+'alter'+os.sep+version
  return version_folder

def invalid_build_folder(build_folder):
  if utils.dir_is_not_present(build_folder):
    usage()
    print
    print "build folder is not present."
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

  schemes=get_schemes(parameters)
  invalid_schemes(schemes)
  versions=get_versions(parameters)
  invalid_versions(versions)



  for version in versions:
    build_folder=get_build_folder(version)
    invalid_build_folder(build_folder)

    
    install_scripts=[]
    for scheme in schemes:

      print "building scheme '"+scheme+"' for version '"+version+"'"
      for object in OBJECTS:  
        for environment in ENVIRONMENTS:          

          # environment specific ddl objects
          folder=build_folder+os.sep+scheme+os.sep+'ddl'+os.sep+object+os.sep+environment
          files=utils.find_files(folder)
          if len(files)!=0:
            filename='install.sql'
            url=folder+os.sep+filename

            stream=''          
            if os.path.isfile(url):
              stream=utils.read_file(url)

            scripts=stream.split(chr(10))
            for file in files:
              scripts=append_not_present(scripts,'prompt '+folder.split(BASE_DIR)[1]+os.sep+file)
              scripts=append_not_present(scripts,'@@'+file)

            synchronized_scripts=scripts
            for script in scripts:
              if script.startswith('prompt '):
                if is_item_not_present(files,script.replace('prompt '+folder.split(BASE_DIR)[1]+os.sep,'')):
                  synchronized_scripts.remove(script)
              if script.startswith('@@'):
                if is_item_not_present(files,script.replace('@@','')):
                  synchronized_scripts.remove(script)
              
            stream = chr(10).join(synchronized_scripts)              
            utils.write_file(url,stream)
            print url
            install_scripts=append_not_present(install_scripts,'@@ddl/'+object+'/&ENVIRONMENT/install.sql')          

        # global ddl objects
        folder=build_folder+os.sep+scheme+os.sep+'ddl'+os.sep+object
        files=utils.find_files(folder)
        if len(files)!=0:
          filename='install.sql'
          url=folder+os.sep+filename
        
          stream=''          
          if os.path.isfile(url):
            stream=utils.read_file(url)

          scripts=stream.split(chr(10))
          for file in files:
            scripts=append_not_present(scripts,'prompt '+folder.split(BASE_DIR)[1]+os.sep+file)
            scripts=append_not_present(scripts,'@@'+file)

          synchronized_scripts=scripts
          for script in scripts:
            if script.startswith('prompt '):
              if is_item_not_present(files,script.replace('prompt '+folder.split(BASE_DIR)[1]+os.sep,'')):
                synchronized_scripts.remove(script)
            if script.startswith('@@'):
              if is_item_not_present(files,script.replace('@@','')):
                print "removed "+script
                synchronized_scripts.remove(script)
           
          stream = chr(10).join(synchronized_scripts)              
 
          utils.write_file(url,stream)
          print url
          install_scripts=append_not_present(install_scripts,'@@ddl/'+object+'/install.sql')

      for environment in ENVIRONMENTS:
 
        # environment specific dat objects
        folder=build_folder+os.sep+scheme+os.sep+'dat'+os.sep+environment
        files=utils.find_files(folder)

        if len(files)!=0:
          filename='install.sql'
          url=folder+os.sep+filename
        
          stream=''          
          if os.path.isfile(url):
            stream=utils.read_file(url)

          scripts=stream.split(chr(10))
          for file in files:
            scripts=append_not_present(scripts,'prompt '+folder.split(BASE_DIR)[1]+os.sep+file)
            scripts=append_not_present(scripts,'@@'+file)

          synchronized_scripts=scripts
          for script in scripts:
            if script.startswith('prompt '):
              if is_item_not_present(files,script.replace('prompt '+folder.split(BASE_DIR)[1]+os.sep,'')):
                synchronized_scripts.remove(script)
            if script.startswith('@@'):
              if is_item_not_present(files,script.replace('@@','')):
                synchronized_scripts.remove(script)
              
          stream = chr(10).join(synchronized_scripts)             
 
          utils.write_file(url,stream)
          print url
          install_scripts=append_not_present(install_scripts,'@@dat/&ENVIRONMENT/install.sql')

      # global dat objects
      folder=build_folder+os.sep+scheme+os.sep+'dat'
      files=utils.find_files(folder)

      if len(files)!=0:
        filename='install.sql'
        url=folder+os.sep+filename
      
        stream=''          
        if os.path.isfile(url):
          stream=utils.read_file(url)

        scripts=stream.split(chr(10))
        for file in files:
          scripts=append_not_present(scripts,'prompt '+folder.split(BASE_DIR)[1]+os.sep+file)
          scripts=append_not_present(scripts,'@@'+file)

        synchronized_scripts=scripts
        for script in scripts:
          if script.startswith('prompt '):
            if is_item_not_present(files,script.replace('prompt '+folder.split(BASE_DIR)[1]+os.sep,'')):
              synchronized_scripts.remove(script)
          if script.startswith('@@'):
            if is_item_not_present(files,script.replace('@@','')):
              synchronized_scripts.remove(script)
              
        stream = chr(10).join(synchronized_scripts)            
 
        utils.write_file(url,stream)
        print url
        install_scripts=append_not_present(install_scripts,'@@dat/install.sql')

    # create install_scheme.sql script
    install_scheme=utils.read_file(NOORA_DIR+os.sep+'install_scheme.sql')
    if len(install_scripts)!=0:
      stream=''
      url=build_folder+os.sep+scheme+os.sep+'install_scheme.sql'
      for item in install_scripts:
        stream=stream+item+chr(10)
      install_scheme=install_scheme.replace('<scripts>',stream)
      utils.write_file(url,install_scheme)
      print url



