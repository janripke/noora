import web
from org.noora.web.model.ProjectModel import ProjectModel
from org.noora.web.view.Viewer import Viewer

class ProjectDelete(Viewer):

  def __init__(self):
    Viewer.__init__(self)


  def GET(self, hashcode):        
    db = self.getPersister().getDatabase() 
    model = ProjectModel(db)
    model.deleteProject(hashcode)
    raise web.seeother('/project/'+web.ctx.session.hashcode)