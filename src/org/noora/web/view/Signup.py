import web
from org.noora.web.model.UserModel import UserModel
from org.noora.web.view.Viewer import Viewer


class Signup(Viewer):

  def __init__(self):
    Viewer.__init__(self)
    
    self.__form = web.form.Form(
      web.form.Textbox('username', web.form.notnull, size=30, description="username"),
      web.form.Password('password', web.form.notnull, size=30, description="password"),
      web.form.Textbox('email', web.form.notnull, size=30, description="email"),
      web.form.Button('Sign up'),
    )

  def getForm(self):
    return self.__form

  def GET(self, referral=None):
    render = self.getRenderer().getRender()
    form = self.getForm()
    return render.signup(form)

  def POST(self):
    render = self.getRenderer().getRender()   
    db = self.getPersister().getDatabase() 
    form = self.getForm()
    if not form.validates():
      return render.signup(form)
       
    model = UserModel(db)
    model.newUser(form.d.username, form.d.password, form.d.email)
    
    raise web.seeother('/')
