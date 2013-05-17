#!/usr/bin/env python
import wx

import gui.MainFrame as MainFrame

modules = {'TopFrame': [1, 'Main frame of the Application', u'gui/TopFrame.py']}

class NooraGuiApp(wx.App):
  def __init__(self, redirect=False, filename=None):
    wx.App.__init__(self, redirect, filename)

  def OnInit(self):
    appTitle='NoOra'
    self.main = MainFrame.MainFrame(self,appTitle)
    self.main.SetSize((600,500))
    self.main.CenterOnScreen()
    self.SetTopWindow(self.main)
    self.main.Show(True)    
    return True

def main():
    application = NooraGuiApp()
    application.MainLoop()

if __name__ == '__main__':
    main()
