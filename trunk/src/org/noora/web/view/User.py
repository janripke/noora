from org.noora.web.model.UserModel import UserModel
from org.noora.web.view.Viewer import Viewer
import web

class User(Viewer):

  def __init__(self):
    Viewer.__init__(self)

   
  def GET(self):
    render = self.getRenderer().getRender()   
    db = self.getPersister().getDatabase()  
    userModel = UserModel(db)    
    users = userModel.getUsers()          
       
    return render.user(users)

  def POST(self):
    render = self.getRenderer().getRender()   
    db = self.getPersister().getDatabase() 
    #form = self.getForm()
    #if not form.validates():
    #  return render.site(form)
    #model = SiteModel(db)
    #model.newSite(form.d.name, form.d.url, form.d.delay,form.d.delay_unit, form.d.paylimit, form.d.paylimit_currency)
    #raise web.seeother('/site')