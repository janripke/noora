from org.noora.io.File import File

class ProjectHelper(object):

  def __init__(self):
    pass
    
#---------------------------------------------------------
  def isProjectDir(self, path):
    if path:
      projdir = File(path)
    
      if projdir.isDirectory():
        if File("{0}/project-config.xml".format(path)).exists() or \
           File("{0}/project.conf".format(path)).exists():
          return True
        
    return False
    
        