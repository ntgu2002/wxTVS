import wx
import math

TVS_SIZE = 32

class clControlPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        btn = wx.Button(self, label="Control")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btn, 0, wx.ALL, 10)
        self.SetSizer(sizer)

class SelectObject(object):
    def __init__(self, clickX, clickY):
        self.select = True
        cL = [0 for i in range(6)]
        points = paintTVS(TVS_SIZE).Points()
        for i in range(6):
            if i == 5:
                cL[i] = (points[i][0]-clickX)*(points[0][1]-points[i][1])-(points[0][0]-points[i][0])*(points[i][1]-clickY)
            else:
                cL[i] = (points[i][0]-clickX)*(points[i+1][1]-points[i][1])-(points[i+1][0]-points[i][0])*(points[i][1]-clickY)
        if cL[0] and cL[1] and cL[2] and cL[3] and cL[4] and cL[5] < 0:
            print('INSIDE!')
        else:
            print('out')

#    def FindTVS(self, clickX, clickY):
#        print('Click Event!!!', clickX, clickY)

class paintTVS(object):
    def __init__(self, radius):
        TVS_r = radius
        TVS_R = 2 * TVS_r / math.sqrt(3)
        dx = TVS_R
        dy = TVS_R
        self.points = [(dx + TVS_r, dy + TVS_R / 2), (dx + TVS_r, dy - TVS_R / 2), (dx + 0, dy - TVS_R),
                       (dx - TVS_r, dy - TVS_R / 2), (dx - TVS_r, dy + TVS_R / 2), (dx + 0, dy + TVS_R)]

    def Points(self):
        return self.points

    def Render(self, gc):
        gc.SetPen(wx.Pen("navy", 1))
        gc.SetBrush(wx.Brush("pink"))
        path = gc.CreatePath()
        for i in range(6):
            path.AddLineToPoint(self.points[i])
        path.CloseSubpath()
        gc.DrawPath(path)


class clAZonePanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.SetBackgroundColour("WHITE")
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        # Create paint DC
        dc = wx.PaintDC(self)
        # Create graphics context from it
        gc = wx.GraphicsContext.Create(dc)
        if gc:
            paintTVS(TVS_SIZE).Render(gc)
            self.Bind(wx.EVT_LEFT_DOWN, self.OnButtonClicked)

    def OnButtonClicked(self, evt):
        clickX = evt.GetPosition()[0]
        clickY = evt.GetPosition()[1]
        #print('Click Event!!!', clickX, clickY)
        #evt.Skip()
        SelectObject(clickX, clickY)

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, 'Active Zone VVER maker', size=(1000, 800))

        ControlPanel = clControlPanel(self, -1, style=wx.SUNKEN_BORDER)
        AZonePanel = clAZonePanel(self, -1, style=wx.SUNKEN_BORDER)

        sizerFrame = wx.BoxSizer(wx.HORIZONTAL)
        sizerFrame.Add(ControlPanel, 1, wx.EXPAND)
        sizerFrame.Add(AZonePanel, 4, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(sizerFrame)
        self.Layout()

if  __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()