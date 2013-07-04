
import wx
import wx.lib.filebrowsebutton

__revision__ = "$Revision$"

[wxID_PROJECTGROUP, 
 wxID_PROJECTDIR, 
 wxID_PROJECTDIRLABEL,
] = [wx.NewId() for _init_ctrls in range(3)]

class Project:
    '''
    Create and manage the Project settings.
    Contains a directory chooser widget to locate the root directory of the noora project
    that you want to use
    '''
    
    def __init_controls(self, parent):
        
        self.__parent = parent
               
        # not all wx implementations (e.g. wxGTK) will support children _inside_ the static box so
        # we make them siblings of the static box instead.
        
        self.ProjectGroup = wx.StaticBox(id=wxID_PROJECTGROUP, label='Project', 
                                         name='ProjectGroup', parent=parent, 
                                         pos=wx.Point(8, 16), size=wx.Size(320, 104),
                                         style=0)

        #self.projectDirLabel = wx.StaticText(id=wxID_PROJECTDIRLABEL, label='Project home directory:',
        #                                     name='ProjectHomeLabel', parent=parent,
        #                                     pos=wx.Point(16, 32), size=wx.Size(64, 13),
        #                                     style=0)

        self.projectDir = wx.lib.filebrowsebutton.DirBrowseButton(buttonText='Browse',
                                                                  dialogTitle='Choose directory',
                                                                  id=wxID_PROJECTDIR,
                                                                  labelText='',
                                                                  newDirectory=False,
                                                                  parent=parent, 
                                                                  pos=wx.Point(24, 56),
                                                                  size=wx.Size(296, 48),
                                                                  startDirectory='.',
                                                                  style=wx.TAB_TRAVERSAL,
                                                                  toolTip='Type directory name or browse to select')
        self.projectDir.SetLabel('')
        self.projectDir.SetValue('')
        self.projectDir.SetName('projectDir')
        self.projectDir.SetToolTipString('choose project directory')
        # self.projectDir.Bind(WX_EVTBUTTON,)

    def __init__(self, parent):
        self.__init_controls(parent)
