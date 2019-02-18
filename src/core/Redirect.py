import wx


class Redirect(object):
  def __init__(self, control):
    self.out=control

  def write(self,string):
    #self.out.AppendText(string)
    wx.CallAfter(self.out.AppendText, string)
