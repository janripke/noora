#!/usr/bin/env python
#Boa:App:NooraGUIApp

import wx

import gui.TopFrame as TopFrame

modules ={'TopFrame': [1, 'Main frame of the Application', u'TopFrame.py']}

class NooraGuiApp(wx.App):
    def OnInit(self):
        self.main = TopFrame.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():
    application = NooraGuiApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()
