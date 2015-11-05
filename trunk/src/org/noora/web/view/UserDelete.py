import web
from org.noora.web.model.UserModel import UserModel
from org.noora.web.view.Viewer import Viewer

class UserDelete(Viewer):

  def __init__(self):
    Viewer.__init__(self)


  def GET(self, hashcode):        
    db = self.getPersister().getDatabase() 
    model = UserModel(db)
    model.deleteUser(hashcode)
    raise web.seeother('/user')