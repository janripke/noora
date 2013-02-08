import wx

class AbstractFrame(wx.Frame):
        
    def __init__(self, parent, title):
        
        if isinstance(parent,wx.Frame):        
            wx.Frame.__init__(self, parent, -1, title)
        else:
            wx.Frame.__init__(self,None,-1,title)
            