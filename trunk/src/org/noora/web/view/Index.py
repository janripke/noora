from org.noora.web.view.Viewer import Viewer
import web

class Index(Viewer):

  def __init__(self):
    Viewer.__init__(self)


  def GET(self):
    render = self.getRenderer().getRender()   
    #db = self.getPersister().getDatabase()    
    #homePath=str(web.ctx.homepath)
    #parameters = web.input()
    #for p in parameters:
    #  if p == 'referral':
    #    web.ctx.session.referral=parameters['referral']
    
    #blogModel = BlogModel(db)
    #posts = blogModel.getPosts()

    return render.index()
