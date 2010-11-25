

import wx

class LabelText:
    '''
    This class contains a pair of a label and text field
    '''
    
    def _init_controls (self, parent, pos, labelWidth, textWidth, name, value):
        
        labelPos = wx.Point (pos.x, pos.y + 4);
        textPos = wx.Point (pos.x + labelWidth + 4, pos.y)
        
        self.labelid = wx.NewId()
        self.labelName = name + '_label'
        self.textid = wx.NewId()
        self.textName = name + '_text'
        
        self.databaseLabel = wx.StaticText(id=self.labelid, label=name,
                                           name=self.labelName, parent=parent, 
                                           pos=labelPos,
                                           size=wx.Size(labelWidth, 13), style=0)

        self.databaseText = wx.TextCtrl(id=self.textid,
                                        name=self.textName, parent=parent,
                                        pos=textPos, size=wx.Size(textWidth, 21),
                                        style=0, value=value)
        
        


    def __init__(self, parent, pos, labelWidth, textWidth, name, value):
        self._init_controls(parent, pos, labelWidth, textWidth, name, value)
        