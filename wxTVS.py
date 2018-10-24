import wx
import math

TVS_SIZE = 32
map = [
    '-----------------',  # 1
    '---------111111--',  # 2
    '-------111111111-',  # 3
    '------1111111111-',  # 4
    '-----11111111111-',  # 5
    '----111111111111-',  # 6
    '---1111112111111-',  # 7
    '--11111111111111-',  # 8
    '--1111132311111--',  # 9
    '-11111111111111--',  # 10
    '-1111111111111---',  # 11
    '-111111111111----',  # 12
    '-11111111111-----',  # 13
    '-1111111111------',  # 14
    '-111111111-------',  # 15
    '--111111---------',  # 16
    '-----------------'  # 17
]

class clControlPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        btn = wx.Button(self, label="Control")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btn, 0, wx.ALL, 10)
        self.SetSizer(sizer)

class SelectObject(object):
    def __init__(self, clickXY):
        clickX = clickXY[0]
        clickY = clickXY[1]
        cL = [0 for i in range(6)]
        points = paintTVS(TVS_SIZE).Points()

        dRow = 0
        for row in map:
            dCol = 0
            for col in row:
                for i in range(6):
                    if i == 5:
                        cL[i] = (points[dRow][dCol][i][0]-clickX)*(points[dRow][dCol][0][1]-points[dRow][dCol][i][1])-\
                                (points[dRow][dCol][0][0]-points[dRow][dCol][i][0])*(points[dRow][dCol][i][1]-clickY)
                    else:
                        cL[i] = (points[dRow][dCol][i][0]-clickX)*(points[dRow][dCol][i+1][1]-points[dRow][dCol][i][1])-\
                                (points[dRow][dCol][i+1][0]-points[dRow][dCol][i][0])*(points[dRow][dCol][i][1]-clickY)
                if cL[0] < 0 and cL[1] < 0 and cL[2] < 0 and cL[3] < 0 and cL[4] < 0 and cL[5] < 0:
                    self.SelectedTVS = [dRow, dCol]
                    #print('TVS number:', self.SelectedTVS, 'was selected')
                dCol += 1
            dRow += 1

    def TVS_pos(self):
        return self.SelectedTVS

    def TVS_change_pos(self):
        dRow = self.SelectedTVS[0]
        dCol = self.SelectedTVS[1]
        map[dRow] = map[dRow][:dCol] + '2' + map[dRow][(dCol + 1):]

class paintTVS(object):
    def __init__(self, radius):
        TVS_r = radius
        TVS_R = 2 * TVS_r / math.sqrt(3)
        offset = 8 * TVS_r
        dx = 0 - offset
        dy = TVS_R
        self.pointsTVS = [[0 for i in range(40)] for j in range(40)]
        # AZ map

        dRow = 0
        for row in map:
            dCol = 0
            for col in row:
                self.pointsTVS[dRow][dCol] = [(dx + TVS_r, dy + TVS_R / 2), (dx + TVS_r, dy - TVS_R / 2), (dx + 0, dy - TVS_R),
                                              (dx - TVS_r, dy - TVS_R / 2), (dx - TVS_r, dy + TVS_R / 2), (dx + 0, dy + TVS_R)]
                dx += TVS_r * 2
                dCol += 1
            dRow += 1
            dy += TVS_R * 2 - TVS_R / 2
            dx = TVS_r * dRow - offset


    def Points(self):
        return self.pointsTVS

    def Render(self, gc):
        #dc.Clear()
        path = [[0 for i in range(40)] for j in range(40)]
        dRow = 0
        for row in map:
            dCol = 0
            for col in row:
                if col == '1':
                    gc.SetPen(wx.Pen("navy", 1))
                    gc.SetBrush(wx.Brush("pink"))
                    #gc.DrawPolygon(self.pointsTVS[dRow][dCol])
                elif col == '2':
                    gc.SetPen(wx.Pen("navy", 1))
                    gc.SetBrush(wx.Brush("green"))
                    #gc.DrawPolygon(self.pointsTVS[dRow][dCol])
                elif col == '3':
                    gc.SetPen(wx.Pen("navy", 1))
                    gc.SetBrush(wx.Brush("pink"))
                    #gc.DrawPolygon(self.pointsTVS[dRow][dCol])
                else:
                    gc.SetPen(wx.Pen("navy", 1, wx.PENSTYLE_TRANSPARENT))
                    gc.SetBrush(wx.Brush(wx.Colour(255, 255, 255, 0)))
                path[dRow][dCol] = gc.CreatePath()
                for i in range(6):
                    path[dRow][dCol].AddLineToPoint(self.pointsTVS[dRow][dCol][i])
                path[dRow][dCol].CloseSubpath()
                gc.DrawPath(path[dRow][dCol])
                dCol += 1
            dRow += 1

class clAZonePanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.SetBackgroundColour("WHITE")
        # Events by Paint, LeftMouseClick, ..
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnButtonClick)

    def InitBuffer(self):
        # Create Buffer Bitmap
        w, h = self.GetClientSize()
        self.Buffer = wx.Bitmap(w, h)
        # Create BufferedDC
        dc = wx.BufferedDC(wx.ClientDC(self), self.Buffer)
        dc.Clear()
        # Create GraphicsContext
        gc = wx.GraphicsContext.Create(dc)
        # Painting in GraphicsContext
        paintTVS(TVS_SIZE).Render(gc)

    def OnPaint(self, evt):
        # Painting through Buffer
        self.InitBuffer()

    def OnButtonClick(self, evt):
        # Define Click position
        clickXY = [evt.GetPosition()[0], evt.GetPosition()[1]]
        print('TVS number:', SelectObject(clickXY).TVS_pos(), 'was selected')
        # Define clicked TVS
        SelectObject(clickXY).TVS_change_pos()
        # Painting through Buffer
        self.InitBuffer()


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, 'Active Zone VVER maker', size=(1290, 1010))

        ControlPanel = clControlPanel(self, -1, size=(240, 1010), style=wx.SUNKEN_BORDER)
        AZonePanel = clAZonePanel(self, -1, size=(1050, 1010), style=wx.SUNKEN_BORDER)

        sizerFrame = wx.BoxSizer(wx.HORIZONTAL)
        sizerFrame.Add(ControlPanel, 0, wx.EXPAND)
        sizerFrame.Add(AZonePanel, 1, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(sizerFrame)
        self.Layout()

if  __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()