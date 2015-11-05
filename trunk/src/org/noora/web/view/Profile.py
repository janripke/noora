import web
from org.noora.web.model.UserModel import UserModel
from org.noora.web.view.Viewer import Viewer


class Profile(Viewer):

  def __init__(self):
    Viewer.__init__(self)

    self.__form = web.form.Form(
      web.form.Textbox('username', web.form.notnull, size=30, description="username"),      
      web.form.Textbox('email', web.form.notnull, size=30, description="email"),                                                                                              
      web.form.Button('Save'),
    )

  def getForm(self):
    return self.__form


  def GET(self, hashcode):
    db = self.getPersister().getDatabase()
    render = self.getRenderer().getRender()        
    model = UserModel(db)
    post = model.getUser(hashcode)
    form = self.getForm()
    form.fill(post)
    
    if web.ctx.session.username!='':
      return render.profile(post, form)
    
    
    raise web.seeother('/login')


  def POST(self, hashcode):
    render = self.getRenderer().getRender()   
    db = self.getPersister().getDatabase() 
    
    form = self.getForm()
    model = UserModel(db)
    post = model.getUser(hashcode)
    if not form.validates():
        return render.profile(post, form)
    model.updateUser(hashcode, form.d.email)
    raise web.seeother('/')
