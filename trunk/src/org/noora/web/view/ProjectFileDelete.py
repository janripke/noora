import web
from org.noora.web.model.ProjectFileModel import ProjectFileModel
from org.noora.web.model.ProjectModel import ProjectModel
from org.noora.web.view.Viewer import Viewer

class ProjectFileDelete(Viewer):

  def __init__(self):
    Viewer.__init__(self)


  def GET(self, hashcode):        
    db = self.getPersister().getDatabase() 
    projectFileModel = ProjectFileModel(db)
    projectFile = projectFileModel.getProjectFile(hashcode)
    projectId = projectFile['pjt_id']
    projectModel = ProjectModel(db)
    project = projectModel.getProjectById(projectId)
    
    
    projectFileModel.deleteProjectFile(hashcode)
    raise web.seeother('/project_edit/'+project['hashcode'])