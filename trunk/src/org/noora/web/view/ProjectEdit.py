import web
import os
from org.noora.web.model.ProjectModel import ProjectModel
from org.noora.web.model.ProjectFileModel import ProjectFileModel
from org.noora.web.view.Viewer import Viewer
from org.noora.io.Path import Path
from org.noora.io.File import File
from org.noora.io.Files import Files

class ProjectEdit(Viewer):

  def __init__(self):
    Viewer.__init__(self)

    self.__form = web.form.Form(
      #web.form.Textbox('name', web.form.notnull, size=30, description="name"),  
      web.form.File(name='upload'),
      web.form.Button('Save'),
    )
    
    self.__actionForm = web.form.Form(
      web.form.Dropdown('command', description="command", args=[] ),
      web.form.Dropdown('host', description="host", args=[] ),
      web.form.Dropdown('database', description="database", args=[] ),
      web.form.Dropdown('environment', description="environment", args=[] ),
      web.form.Dropdown('version', description="version", args=[] ),
      web.form.Button('Execute'),
                                  
    )

  def getForm(self):
    return self.__form
  
  def getActionForm(self):
    return self.__actionForm

  def GET(self, hashcode):
    
    db = self.getPersister().getDatabase()
    render = self.getRenderer().getRender()        
    projectModel = ProjectModel(db)
    project = projectModel.getProject(hashcode)
    
    projectFileModel = ProjectFileModel(db)
    projectFiles = projectFileModel.getProjectFiles(hashcode)
    
    form = self.getForm()
    form.fill(project)                  
    
    #folder = File(Path.path('projects',hashcode))
    #files = Files.list(folder, True)
    #actionForm = self.getActionForm()
    #commands = ['drop','create','update','recreate']
    #hosts = ['localhost']
    #databases = ['orcl']
    #environments = ['dev','test','uat','prod']
    #versions = ['1.0.0']
    
    #actionForm.command.args=commands  
    #actionForm.host.args=hosts
    #actionForm.database.args=databases
    #actionForm.environment.args=environments
    #actionForm.version.args=versions
    
    return render.project_edit(project, form, projectFiles)





  def POST(self, hashcode):
    render = self.getRenderer().getRender()   
    db = self.getPersister().getDatabase() 
    
    form = self.getForm()
    
    
    #if not form.validates():
    #    return render.project_edit(project, form)
      
    x = web.input(upload={})
    
    
    folder = File(Path.path('projects',hashcode))
    if not folder.exists():
      os.makedirs(Path.path(folder.getPath(),folder.getName()))    
                    
    fout = open(Path.path('projects',hashcode ,x.upload.filename),'wb') # creates the file where the uploaded file should be stored
    fout.write(x.upload.file.read()) # writes the uploaded file to the newly created file.
    fout.close() # closes the file, u
    
    projectFileModel = ProjectFileModel(db)
    projectFileModel.newProjectFile(hashcode, x.upload.filename)
    
    #projectModel = ProjectModel(db)
    #project = projectModel.getProject(hashcode)
    #projectModel.updateProject(hashcode, form.d.name)
    raise web.seeother('/project_edit/'+hashcode)
