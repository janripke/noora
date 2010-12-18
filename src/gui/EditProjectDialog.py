import wx
import panels.CancelFinishPanel     as CancelFinishPanel
import panels.HeaderPanel           as HeaderPanel
import gui.Settings                 as Settings


class EditProjectDialog(wx.Dialog):

    def getProjectControl(self):
      return self.__projectControl
    
    def getProject(self):
      projectControl=self.getProjectControl()
      return projectControl.getValue()
    




        
    def __init__(self, parent, id, title, url):
        
        wx.Dialog.__init__(self, parent, id, title, style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.__headerPanel = HeaderPanel.HeaderPanel(self, -1,"NoOra Project","Edit the NoOra Project configuration file")    
        self.__projectControl=wx.TextCtrl(self,-1,style=wx.TE_MULTILINE)
        self.__spacerPanel = wx.Panel(self,-1)
        self.__cancelFinishControl=CancelFinishPanel.CancelFinishPanel(self,-1)
        sizer.Add(self.__headerPanel,0,wx.EXPAND)   
        sizer.Add(self.__spacerPanel,0,wx.EXPAND)
        sizer.Add(self.__projectControl,1,wx.EXPAND)
        sizer.Add(self.__spacerPanel,0,wx.EXPAND)
        sizer.Add(self.__cancelFinishControl,0,wx.ALIGN_RIGHT)
                
        self.SetSizer(sizer)
        self.SetMinSize((500,600))
        
        
        
        
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=Settings.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.OnFinish, id=Settings.ID_FINISH)
        
       
        handle=open(url,'rb')
        stream=handle.read()
        handle.close()
        self.__projectControl.AppendText(stream)
        

    def OnCancel(self, evt):
      self.EndModal(Settings.ID_CANCEL)
      self.Close() 
      
    def OnFinish(self, evt): 
      self.EndModal(Settings.ID_FINISH)          
      self.Close() 

  