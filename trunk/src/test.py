#!/usr/bin/env python
versions=['1.0.0','1.0.1','1.0.3']

previous_version=None
version='1.0.0'
index=versions.index(version)
if index>0:
  previous_version=versions[index-1]

print 'previous version:',previous_version