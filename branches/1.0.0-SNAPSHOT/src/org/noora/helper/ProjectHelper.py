from org.noora.io.File import File

class ProjectHelper(object):

  def __init__(self):
    pass
    
#---------------------------------------------------------
  def isProjectDir(self, path):
    if path:
      projdir = File(path)
    
      if projdir.isDirectory():
        if File("project-conf.xml").exists() or File("project.conf").exists():
          return True
        
    return False
    
        