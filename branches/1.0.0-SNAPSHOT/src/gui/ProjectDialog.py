
import wx
import core.CommandDispatcher as Dispatcher
import gui.panels.DirectoryPicker as DirPicker
import gui.panels.ChoicePanel as Choice

DIALOG_TYPE_NEW = 1
DIALOG_TYPE_OPEN = 2

class ProjectDialog(wx.Dialog):

    #def onGenerateProject(self, event):
        #command = Dispatcher.CommandDispatcher();
        
        
    def __init__(self, parent, id, title, dialogtype):
        
        wx.Dialog.__init__(self, parent, id, title, size=(350, 300))

        sizer = wx.BoxSizer(wx.VERTICAL)

        if dialogtype == DIALOG_TYPE_NEW:
            self.__button = wx.Button(self,-1,'Generate');
            sizer.Add(DirPicker.DirectoryPicker(self,wx.NewId()))
            sizer.Add(Choice.ChoicePanel(self,wx.NewId(),'Database',['Oracle','sqlite']))
            sizer.Add(self.__button, 0, wx.ALL | wx.ALIGN_CENTER)
            #wx.EVT_BUTTON(self, self.__button.GetId(), self.onGenerateProject)
            
        self.SetSizer(sizer)
