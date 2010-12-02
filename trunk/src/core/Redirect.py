

class Redirect:
  def __init__(self, control):
    self.out=control

  def write(self,string):
    self.out.AppendText(string)
