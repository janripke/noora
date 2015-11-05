from org.noora.web.model.Model import Model
from org.noora.web.model.UserModel import UserModel
import hashlib
import web
import datetime

class ProjectModel(Model):
  def __init__(self, db=None):
    Model.__init__(self, db)

  def getProjects(self, hashcode):
    db = self.getDatabase()
    
    userModel = UserModel(db)
    user=userModel.getUser(hashcode)
    
    return db.query('select * from projects where usr_id=' + str(user['id']))

  def newProject(self, hashcode, name):
    db = self.getDatabase()

    userModel = UserModel(db)
    user=userModel.getUser(hashcode)
    
    now = datetime.datetime.now()
    currentUser = web.ctx.session.username
    
    m = hashlib.md5()
    m.update(hashcode + name)  
    hashcode = str(m.hexdigest())    
          
    db.insert('projects', name=name, hashcode=hashcode, usr_id=user['id'], created_at=now, created_by=currentUser, updated_at=now, updated_by=currentUser)

  def getProject(self, hashcode):
    db = self.getDatabase()
    try:
      return db.select('projects', where='hashcode=$hashcode', vars=locals())[0]
    except IndexError:
      return None
    
  def getProjectById(self, id):
    db = self.getDatabase()
    try:
      return db.select('projects', where='id=$id', vars=locals())[0]
    except IndexError:
      return None    

  def updateProject(self, hashcode, name):
    db = self.getDatabase()
    
    now = datetime.datetime.now()
    currentUser = web.ctx.session.username    
    db.update('projects', where="hashcode=$hashcode", vars=locals(), name=name,updated_at=now, updated_by=currentUser)  

  def deleteProject(self, hashcode):
    db = self.getDatabase()
    db.delete('projects', where="hashcode=$hashcode", vars=locals())

  