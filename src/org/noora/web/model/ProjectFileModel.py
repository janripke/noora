from org.noora.web.model.Model import Model
from org.noora.web.model.ProjectModel import ProjectModel
import hashlib
import web
import datetime

class ProjectFileModel(Model):
  def __init__(self, db=None):
    Model.__init__(self, db)

  def getProjectFiles(self, hashcode):
    db = self.getDatabase()
    
    projectModel = ProjectModel(db)
    project=projectModel.getProject(hashcode)
    
    return db.query('select * from projectfiles where pjt_id=' + str(project['id']))

  def getProjectFile(self, hashcode):
    db = self.getDatabase()
    try:
      return db.select('projectfiles', where='hashcode=$hashcode', vars=locals())[0]
    except IndexError:
      return None


  def newProjectFile(self, hashcode, filename):
    db = self.getDatabase()
 
    projectModel = ProjectModel(db)
    project=projectModel.getProject(hashcode)
     
    now = datetime.datetime.now()
    currentUser = web.ctx.session.username
     
    m = hashlib.md5()
    m.update(hashcode + filename)  
    hashcode = str(m.hexdigest())    
           
    db.insert('projectfiles', filename=filename, hashcode=hashcode, pjt_id=project['id'], created_at=now, created_by=currentUser, updated_at=now, updated_by=currentUser)

  def deleteProjectFile(self, hashcode):
    db = self.getDatabase()
    db.delete('projectfiles', where="hashcode=$hashcode", vars=locals())

 
#   def getProject(self, hashcode):
#     db = self.getDatabase()
#     try:
#       return db.select('projects', where='hashcode=$hashcode', vars=locals())[0]
#     except IndexError:
#       return None


  