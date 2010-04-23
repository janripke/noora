#!/usr/bin/env python
import os
import sys

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


def get_file_extension(path):
  root,ext=os.path.splitext(path)
  return ext     

def find_files(folder):
  result=[]
  try:
    items=os.listdir(folder)
    for item in items:
      path=folder+os.sep+item
      if os.path.isfile(path):
        result.append(item)
    result.sort()

  except:
    result=[]

  return result


def find_dirs(folder):
  result=[]
  try:
    items=os.listdir(folder)
    for item in items:
      if os.path.isdir(folder+os.sep+item):
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



def parent_folder(folder):
  result=""
  folder_list=folder.split(os.sep)
  folder_count=len(folder_list)
  for i in range(folder_count-1):
    result=result+folder_list[i]+os.sep
  return result.rstrip(os.sep)

def find_file_backwards(folder,filename):
  result=None
  items=os.listdir(folder)
  for item in items:
    path=folder+os.sep+item
    if os.path.isfile(path) and item==filename:
      result=path

  if result==None:
    upper_folder=parent_folder(folder)
    result=find_file(upper_folder, filename)    

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


def show_errors():
  try:
    stream=read_file('feedback.log')
    print stream
  except:
    exit(1)

