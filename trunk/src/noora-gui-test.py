#!/usr/bin/env python
import wx

import gui.MainFrame as MainFrame

modules = {'TopFrame': [1, 'Main frame of the Application', u'gui/TopFrame.py']}

class NooraGuiApp(wx.App):
  
  def OnInit(self):
    appTitle='NoOra'
    self.main = MainFrame.MainFrame(self,appTitle)
    self.main.SetSize((600,600))
    self.main.CenterOnScreen()
    self.SetTopWindow(self.main)
    self.main.Show(True)    
    return True

def main():
    application = NooraGuiApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()
