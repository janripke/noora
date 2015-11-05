from org.noora.web.model.Model import Model
from org.noora.web.model.GroupModel import GroupModel
import hashlib
import web
import datetime

class UserModel(Model):
  def __init__(self, db=None):
    Model.__init__(self, db)

  def getUsers(self):
    db = self.getDatabase()
    return db.query('select * from users order by username')


  def newUser(self, username, password, email):
    db = self.getDatabase()
    groupModel = GroupModel(db)
    group=groupModel.getGroupByName('user')

    m = hashlib.md5()
    m.update(username)  
    hashcode = str(m.hexdigest())
    now = datetime.datetime.now()
    currentUser = web.ctx.session.username    
    
    password = hashlib.md5(password).hexdigest()
          
    db.insert('users', username=username, password=password, email=email,grp_id=group['id'],hashcode=hashcode, created_at=now, created_by=currentUser, updated_at=now, updated_by=currentUser)

  def getUser(self, hashcode):
    db = self.getDatabase()
    try:
      return db.select('users', where='hashcode=$hashcode', vars=locals())[0]
    except IndexError:
      return None

  def login(self, username, password):
    db = self.getDatabase()
    try:
      user = db.select('users', where='username=$username', vars=locals())[0]    
      if hashlib.md5(password).hexdigest() == user['password']:
        return user['hashcode']
    except:
      return ''
    return ''
  
  def updateUser(self, hashcode, email):
    db = self.getDatabase()
    
    now = datetime.datetime.now()
    currentUser = web.ctx.session.username    
    db.update('users', where="hashcode=$hashcode", vars=locals(), email=email,updated_at=now, updated_by=currentUser)  

  def countUsers(self):
    db = self.getDatabase()        
    return db.query('select count(0) as cnt from users')[0]    
  
  def deleteUser(self, hashcode):
    db = self.getDatabase()
    db.delete('users', where="hashcode=$hashcode", vars=locals())

  