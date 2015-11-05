import web
from org.noora.web.view.Viewer import Viewer


class Logout(Viewer):

  def __init__(self):
    Viewer.__init__(self)
    
  def GET(self):    
    web.ctx.session.username = ''    
    web.ctx.session.hashcode = ''
    web.ctx.session.usergroup = 'none'
    raise web.seeother('/')
