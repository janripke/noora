#!/usr/bin/env python

import sys
import traceback

def throws():
    raise RuntimeError('error from throws')
    
def nested():
    try:
        throws()
    except:
        cleanup()
        raise

def cleanup():
    raise RuntimeError('error from cleanup')

def main():
    try:
        nested()
        return 0
    except Exception, err:
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
  
      


if __name__ == '__main__':
    unittest.main()
