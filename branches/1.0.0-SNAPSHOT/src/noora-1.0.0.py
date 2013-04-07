#!/usr/bin/env python

__revision__ = "$Revision: 141 $"
__version__  = "1.0.0"

from org.noora.app.NoOraApp import NoOraApp
from org.noora.io.NoOraError import NoOraError
import sys


if __name__ == "__main__":

  try:
    
    app = NoOraApp(sys.argv)
    
    app.initialize()
    app.run()
    app.terminate()
  
  except NoOraError as e:
    usermsg = e.getUserReason()
    if not usermsg:
      print "error: {0}".format(e.getMessage())
    else:
      print "error: {0}".format(usermsg)
    print   "  reasons: {0}".format(e.getDiagnostics())
    exit(1)
  except Exception as e:
    print "internal error: {0}".format(e)
    exit(1)
    
  exit(0)
  
