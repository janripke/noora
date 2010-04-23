#!/usr/bin/env python
import os
import sys
import config
import zipfile

def get_parameters():
  result=[]
  for param in sys.argv:
    result.append(param)
  return result

def is_parameter(parameters,p):
  result=False
  for parameter in parameters:
    if parameter==p:
      result=True
      break
  return result

def find_parameter(parameters,p):
  result=None
  for parameter in parameters:
    if parameter.find(p)!=-1:
      result=parameter
      break
  return result

def get_parameter_value(parameters,p):
  result=None
  parameter=find_parameter(parameters,p)
  
  if parameter:
    result=parameter.split('=')[1]
  return result


def get_parameter_value_from_list(parameters,options):
  result=None
  for option in options:
    result=get_parameter_value(parameters,option)
    if result:
      return result
  return result


def get_parameter(parameters):
  count=0
  for parameter in parameters:
    result=parameter.split('=')
    if len(result)==1 and count!=0: 
      return parameter
    count=count+1
  return None


def get_file_extension(path):
  root,ext=os.path.splitext(path)
  return ext

def is_file_excluded(path):
   result=False

   excluded_files=config.EXCLUDED_FILES
   for excluded_file in excluded_files:
     if get_filename(path)==excluded_file:
       result=True
       return result

   excluded_extensions=config.EXCLUDED_EXTENSIONS
   for extension in excluded_extensions:
     if get_file_extension(path).find(extension)!=-1:
       result=True
       break
   return result
     

def find_files(folder):
  result=[]
  try:
    items=os.listdir(folder)
    for item in items:
      path=folder+os.sep+item
      if os.path.isfile(path):
        if is_file_excluded(path)==False:
          result.append(item)
    result.sort()

  except:
    result=[]

  return result


def is_dir_excluded(folder):
   result=False
   excluded_folders=config.EXCLUDED_FOLDERS
   for excluded_folder in excluded_folders:
     if folder.find(excluded_folder)!=-1:
       result=True
       break
   return result

def find_dirs(folder):
  result=[]
  try:
    items=os.listdir(folder)
    for item in items:
      if os.path.isdir(folder+os.sep+item):
        if is_dir_excluded(item.lower())==False: 
          result.append(item)
    result.sort()
  except:
    result=[]
  return result


def dir_is_not_present(p_folder):
  if os.path.isdir(p_folder):
    result=False
  else:
    result=True
  return result


def dir_is_present(p_folder):
  if os.path.isdir(p_folder):
    result=True
  else:
    result=False
  return  result


def find_files_recursive(folder):
  result=[]
  items=os.listdir(folder)
  for item in items:
    path=folder+os.sep+item
    if os.path.isdir(path):
      sub_items=find_files_recursive(path)
      for sub_item in sub_items:
        result.append(sub_item)
    else:
      result.append(path)
  return result


def find_folders_recursive(folder):
  result=[]
  items=os.listdir(folder)
  for item in items:
    if os.path.isdir(folder+os.sep+item):
      result.append(folder+os.sep+item)
      sub_items=find_folders_recursive(folder+os.sep+item)
      for sub_item in sub_items:
        result.append(sub_item)
  return result

def get_filename(path):
  folder=os.path.dirname(path)
  result=path.replace(folder+os.sep,'')
  return result

def get_file_extension(path):
  result=None
  filename=get_filename(path)
  items=filename.split('.')
  count=len(items)
  if count>=2:
    result=items[count-1]
  return result

def read_file(filename):
  handle=open(filename,'r')
  stream=handle.read()
  handle.close()
  return stream

def write_file(filename,stream):
  handle=open(filename,'w')
  handle.write(stream)
  handle.close()

def copy(source_filename, target_filename):
  stream=read_file(source_filename)
  write_file(target_filename,stream)

def extract(filename):
  folder=os.path.dirname(filename)+os.sep
  file=zipfile.ZipFile(filename,'r')
  for info in file.infolist():
    stream=file.read(info.filename)
    extract_file=folder+info.filename
    extract_folder=os.path.dirname(extract_file)
    if dir_is_not_present(extract_folder):
      os.makedirs(extract_folder)
    write_file(extract_file,stream)

def remove_folder_recursive(path):
  items=find_files_recursive(path)
  for item in items:
    os.remove(item)

  items=find_folders_recursive(path)
  items.reverse()
  for item in items:
    os.rmdir(item)

  os.rmdir(path)


def show_errors():
  try:
    stream=read_file('feedback.log')
    print stream
  except:
    exit(1)



