import web
from org.noora.web.model.UserModel import UserModel
from org.noora.web.model.GroupModel import GroupModel
from org.noora.web.view.Viewer import Viewer

class Login(Viewer):
  
  

  def __init__(self):
    Viewer.__init__(self)
    
    self.__form = web.form.Form(
      web.form.Textbox('username',  web.form.notnull, size=30, description="username"),     
      web.form.Password('password', web.form.notnull, size=30, description="password"),
      web.form.Button('Sign in'),
    )

  def getForm(self):
    return self.__form

  def GET(self):
    render = self.getRenderer().getRender()
    form = self.getForm()
        
    return render.login(form,'')

  def POST(self):
    render = self.getRenderer().getRender()   
    db = self.getPersister().getDatabase()    
    form = self.getForm()
    if not form.validates():
      return render.login(form,'')

    model = UserModel(db)
    result = model.login(form.d.username, form.d.password)
    if result!='':      
      user = model.getUser(result)
      groupModel = GroupModel(db)
      group = groupModel.getGroup(user['grp_id'])
      web.ctx.session.username = form.d.username    
      web.ctx.session.hashcode = result
      web.ctx.session.usergroup = group['usergroup']
      web.ctx.session.referralindex = 0    
      raise web.seeother('/')
    else:      
      return render.login(form,'invalid username or password')
    

