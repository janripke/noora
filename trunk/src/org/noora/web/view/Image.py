import web
import os

class Image:
  
  def GET(self, name):
    ext = name.split(".")[-1]  # Gather extension

    cType = {
        "png":"images/png",
        "jpg":"images/jpeg",
        "gif":"images/gif",
        "ico":"images/x-icon"            }

    if name in os.listdir('images'):  # Security
      web.header("Content-Type", cType[ext])  # Set the Header
      return open('images/%s' % name, "rb").read()  # Notice 'rb' for reading images
      raise web.notfound()
