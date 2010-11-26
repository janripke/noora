#!/usr/bin/env python
import wx

import gui.TopFrame

modules = {'TopFrame': [1, 'Main frame of the Application', u'gui/TopFrame.py']}

class NooraGuiApp(wx.App):
  
  def OnInit(self):
    self.main = gui.TopFrame.TopFrame(None)
    self.main.Show()
    self.SetTopWindow(self.main)
    return True

def main():
    application = NooraGuiApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()
