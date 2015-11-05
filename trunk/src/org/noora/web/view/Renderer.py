import web



t_globals = {
    'datestr': web.datestr
}


class Renderer:

    def __init__(self):      
      #self.__render = web.template.render('templates', base='base', globals=t_globals)      
      self.__render = web.template.render('templates', base='base', globals={'session': web.ctx.session})
      
    def setRender(self, render):
      self.__render = render
      
    def getRender(self):
      return self.__render


