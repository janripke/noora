

import wx

class LabelText:
    '''
    This class contains a pair of a label and text field
    '''
    
    def _init_controls (self, parent, pos, labelWidth, textWidth, label, value):
        
        labelPos = wx.Point (pos.x, pos.y + 4);
        textPos = wx.Point (pos.x + labelWidth + 4, pos.y)
        
        self.labelid = wx.NewId()
        self.labelName = label + '_label'
        self.textid = wx.NewId()
        self.textName = label + '_text'
        
        self.label = wx.StaticText(id=self.labelid, label=label,
                                   name=self.labelName, parent=parent, 
                                   pos=labelPos,
                                   size=wx.Size(labelWidth, 13), style=0)

        self.text = wx.TextCtrl(id=self.textid,
                                name=self.textName, parent=parent,
                                pos=textPos, size=wx.Size(textWidth, 21),
                                style=0, value=value)
        
        
    def __init__(self, parent, pos, labelWidth, textWidth, label, value):
        self._init_controls(parent, pos, labelWidth, textWidth, label, value)
        