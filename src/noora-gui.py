#!/usr/bin/env python
import wx
import gui.TopFrame as TopFrame

modules ={'TopFrame': [1, 'Main frame of the Application', u'TopFrame.py']}

class MyApp(wx.App):
  
  def OnInit(self):
    frame=TopFrame.create(None)
    #frame = wx.Frame(None, -1, "Hello from wxPython")
    frame.Show()
    self.SetTopWindow(frame)
    return True

app = MyApp(0)
app.MainLoop()
