import wx

class frameclass(wx.Frame):

    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,"InTouch Registrator", size=(700,500))
        panel = wx.Panel(self)

        button = wx.Button(panel, label="exit", pos=(50,50))
        self.Bind(wx.EVT_BUTTON, self.closebutton, button)

        self.Bind(wx.EVT_CLOSE, self.closewindow)

        status = self.CreateStatusBar()
        menubar = wx.MenuBar()
        first = wx.Menu()
        second = wx.Menu()
        first.Append(wx.NewId(), 'New Window', 'This is a new window')
        first.Append(wx.NewId(), 'Open', 'This will open a new window')
        menubar.Append(first, "File")
        menubar.Append(second, "Edit")
        self.SetMenuBar(menubar)

        wx.StaticText(panel, -1, "This is Static Text", pos=(100,100))

        spinner = wx.SpinCtrl(panel,-1,"Interval", (500,40), (60,-1))
        spinner.SetRange(1,100)
        spinner.SetValue(30)

        textentry = wx.TextCtrl(panel, -1, "What's your Name?", (400,300))

        wx.CheckBox(panel, -1, "Apples", (500,300), (160,-1))
        wx.CheckBox(panel, -1, "Bananas", (500,320), (160,-1))
        wx.CheckBox(panel, -1, "Oranges", (500,340), (160,-1))
        
##
##        custom = wx.StaticText(panel, -1, "CUSTOM TEXT whoohoo", pos=(150,150), size=(260,-1))
##        custom.SetForegroundColour('white')
##        custom.SetBackgroundColour('blue')

##        box = wx.MessageDialog(None, 'Do you like Ben Franklin?', 'important question', wx.YES_NO)
##        answer = box.ShowModal()
##        box.Destroy()

##        box = wx.MessageDialog(None, 'You DO like Ben Franklin' , 'important question', wx.OK)
##        answer = box.ShowModal()
##        box.Destroy()
##
##        box = wx.TextEntryDialog(None, "What's your Name?", "Answer the below question", "default text")
##        if box.ShowModal() == wx.ID_OK:
##            answer = box.GetValue()
##            print answer

##        wx.StaticText(panel, -1, answer, (10,10))
        
##        box = wx.SingleChoiceDialog(None, 'What\'s your favorite food?', 'Food Picker',
##                                    ['Carrots','Spinach','Brocoli'])
##        if box.ShowModal() == wx.ID_OK:
##            answer = box.GetStringSelection()
##            print answer

    def closebutton(self, event):
        self.Close(True)

    def closewindow(self, event):
        self.Destroy()

if __name__=='__main__':
    app=wx.PySimpleApp()
    frame=frameclass(parent=None,id=-1)
    frame.Show()
    app.MainLoop()
    
