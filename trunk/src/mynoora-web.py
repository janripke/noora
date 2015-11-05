import web
from org.noora.web.view.Index import Index
from org.noora.web.view.Image import Image
from org.noora.web.view.Login import Login
from org.noora.web.view.Logout import Logout
from org.noora.web.view.Profile import Profile
from org.noora.web.view.User import User
from org.noora.web.view.UserDelete import UserDelete
from org.noora.web.view.UserEdit import UserEdit
from org.noora.web.view.Signup import Signup
from org.noora.web.view.Project import Project
from org.noora.web.view.ProjectEdit import ProjectEdit
from org.noora.web.view.ProjectDelete import ProjectDelete
from org.noora.web.view.ProjectFileDelete import ProjectFileDelete
from org.noora.web.view.Upload import Upload
### Url mappings

urls = (
    '/', 'Index',
    '/images/(.*)', 'Image',
    '/login', 'Login',
    '/logout', 'Logout',
    '/profile/(.+)', 'Profile',
    '/user', 'User',
    '/user_delete/(.+)','UserDelete',
    '/user_edit/(.+)','UserEdit',
    '/signup', 'Signup',
    '/project/(.+)', 'Project', 
    '/project_edit/(.+)','ProjectEdit',
    '/project_delete/(.+)','ProjectDelete',
    '/upload','Upload',
    '/projectfile_delete/(.+)','ProjectFileDelete',
)

def session_hook():  
  web.ctx.session = session
  web.template.Template.globals['session'] = session
    

app = web.application(urls, globals())
#session = web.session.Session(app, web.session.DiskStore('sessions'), initializer = {'count': 0, 'login': 0, 'privilege': 0,'username': "",'hashcode': "",'usergroup': "",'referralindex': 0,'referral': ""})

db = web.database(dbn='mysql', host='localhost', user='apps', pw='apps', db='orcl')
store = web.session.DBStore(db, 'sessions')
session = web.session.Session(app, store, initializer={'count': 0, 'login': 0, 'privilege': 0,'username': "",'hashcode': "",'usergroup': "",'referralindex': 0,'referral': ""})



app.add_processor(web.loadhook(session_hook))



if __name__ == '__main__':
    app.run()