#!/usr/bin/env python

import os
import subprocess

class StartupInfoFactory:
  def __init__(self):
    pass
  
  @staticmethod
  def newStartupInfo():
    startupInfo=None
    if os.name=='nt':    
      startupInfo=subprocess.STARTUPINFO()
      #USESHOWWINDOW
      startupInfo.dwFlags |=1
      #SW_HIDE
      startupInfo.wShowWindow=0
    return startupInfo