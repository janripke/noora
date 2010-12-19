import wx
import panels.CancelFinishPanel     as CancelFinishPanel
import panels.HeaderPanel           as HeaderPanel
import gui.Settings                 as Settings
import core.ConfigReader            as ConfigReader


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
        #self.__projectControl=wx.TextCtrl(self,-1,style=wx.TE_MULTILINE)
        self.__projectControl=wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_VRULES|wx.LC_HRULES)
        self.__projectControl.InsertColumn(0, 'Keyword')
        self.__projectControl.InsertColumn(1, 'Value')

        self.__cancelFinishControl=CancelFinishPanel.CancelFinishPanel(self,-1)
        sizer.Add(self.__headerPanel,0,wx.EXPAND)   
        sizer.Add(self.__projectControl,1,wx.EXPAND|wx.ALL,5)
        sizer.Add(self.__cancelFinishControl,0,wx.ALIGN_RIGHT|wx.ALL,5)
                
        self.SetSizer(sizer)
        self.SetMinSize((500,600))
        
        
        
        
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=Settings.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.OnFinish, id=Settings.ID_FINISH)
        
        configReader=ConfigReader.ConfigReader(url)
        lines=configReader.getLines()
        for line in lines:
          
          if (line.startswith("#")!=True) and (len(line.strip(" "))!=0):
            
            keyword=line.split('=')[0]
            values=line.split('=')[1::]
            value='='.join(values)

            itemCount=self.__projectControl.GetItemCount()
            self.__projectControl.InsertStringItem(itemCount, keyword)
            self.__projectControl.SetStringItem(itemCount, 1, value)
          
            
        self.__projectControl.SetColumnWidth(-1,-1)  
        self.__projectControl.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)  
            

    def OnCancel(self, evt):
      self.EndModal(Settings.ID_CANCEL)
      self.Close() 
      
    def OnFinish(self, evt): 
      self.EndModal(Settings.ID_FINISH)          
      self.Close() 

  