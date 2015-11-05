from org.noora.web.model.ProjectModel import ProjectModel
from org.noora.web.view.Viewer import Viewer
import web

class Project(Viewer):

  def __init__(self):
    Viewer.__init__(self)

    self.__form = web.form.Form(
      web.form.Textbox('name', web.form.notnull, size=50, description="name"),                                                                                                                                      
      web.form.Button('Add'),
    )

  def getForm(self):
    return self.__form
   
  def GET(self, hashcode):
    render = self.getRenderer().getRender()   
    db = self.getPersister().getDatabase()  
    form = self.getForm()    
    projectModel = ProjectModel(db)    
    projects = projectModel.getProjects(hashcode)          
       
    return render.project(form, projects)

  def POST(self, hashcode):
    render = self.getRenderer().getRender()   
    db = self.getPersister().getDatabase() 
    
    form = self.getForm()
    
    projectModel = ProjectModel(db)    
    projects = projectModel.getProjects(hashcode)    
    
    if not form.validates():
      return render.project(form, projects)
    model = ProjectModel(db)
    model.newProject(hashcode, form.d.name)
    raise web.seeother('/project/'+hashcode)    
