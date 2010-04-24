#!/usr/bin/env python

def get_major_part(str):
  return int(str.split('.')[0])

def get_minor_part(str):
  return int(str.split('.')[1])

def get_revision_part(str):
  return int(str.split('.')[2])

def resolve_major_part(item):
  major_part=item/10000
  return major_part

def resolve_major_rest(item):
  major_rest=item%10000
  return major_rest

def resolve_minor_part(item):
  major_rest=resolve_major_rest(item)
  minor_part=major_rest/1000
  return minor_part

def resolve_minor_rest(item):
  major_rest=resolve_major_rest(item)  
  minor_rest=major_rest%1000
  return minor_rest

def resolve_revision_part(item):
  minor_rest=resolve_minor_rest(item)
  revision_part=minor_rest/10
  return revision_part

def get_weight_list(versions):
  items=[]
  for version in versions:
    major_part=get_major_part(version)
    minor_part=get_minor_part(version)
    revision_part=get_revision_part(version)
    items.append((10*revision_part)+(1000*minor_part)+(10000*major_part))
  return items

def reverse_weight_list(versions):
  items=[]
  for version in versions:
    major_part=resolve_major_part(version)
    minor_part=resolve_minor_part(version)
    revision_part=resolve_revision_part(version)
    items.append(str(major_part)+"."+str(minor_part)+"."+str(revision_part))
  return items

def sort_as_versions(versions):
  items=get_weight_list(versions)
  items.sort()
  items=reverse_weight_list(items)     
  return items


