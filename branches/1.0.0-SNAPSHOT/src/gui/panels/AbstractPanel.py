import wx

class AbstractPanel(wx.Panel):

    def __init__(self,parent, id):
        wx.Panel.__init__(self,parent, id)
        
