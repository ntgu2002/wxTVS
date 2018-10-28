import wx
import math

AZ_dimension = 17
TVS_SIZE = 32
map_year = [
    '-----------------',  # 1
    '---------111111--',  # 2
    '-------111111111-',  # 3
    '------1111111111-',  # 4
    '-----11111111111-',  # 5
    '----111111111111-',  # 6
    '---1111111111111-',  # 7
    '--11111111111111-',  # 8
    '--1111111111111--',  # 9
    '-11111111111111--',  # 10
    '-1111111111111---',  # 11
    '-111111111111----',  # 12
    '-11111111111-----',  # 13
    '-1111111111------',  # 14
    '-111111111-------',  # 15
    '--111111---------',  # 16
    '-----------------'  # 17
]

TVS_type = ['U49G6', 'U49Z4', 'U44Z4']
map_type = [
    '-----------------',  # 1
    '---------111111--',  # 2
    '-------111111111-',  # 3
    '------1111111111-',  # 4
    '-----11111111111-',  # 5
    '----111111111111-',  # 6
    '---1111111111111-',  # 7
    '--11111111111111-',  # 8
    '--1111111111111--',  # 9
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

        sizer_Main = wx.BoxSizer(wx.VERTICAL)
        Label_AZ_modification = wx.StaticText(self, -1, "AZ modification", (0, 0), (240, 20), wx.ALIGN_CENTER)
        sizer_Main.Add(Label_AZ_modification, 0, wx.ALL, 5)

        sizer_TVS_type = wx.BoxSizer(wx.HORIZONTAL)
        valList_TVS_type = ["Don't change", 'U49G6', 'U49Z4', 'U44Z4']
        Label_TVS_type = wx.StaticText(self, -1, "Select one:")
        List_TVS_type = wx.Choice(self, -1, (0, 0), (110, 25), choices = valList_TVS_type)
        List_TVS_type.SetSelection(0)
        sizer_TVS_type.Add(Label_TVS_type, 0, wx.ALL, 5)
        sizer_TVS_type.Add(List_TVS_type, 0, wx.ALL, 5)
        sizer_Main.Add(sizer_TVS_type, 0, wx.ALL, 5)

        self.SetSizer(sizer_Main)

class SelectObject(object):
    def __init__(self, btn, clickXY):
        self.SelectedTVS = [0, 0]
        self.button = btn
        clickX = clickXY[0]
        clickY = clickXY[1]
        cL = [0 for i in range(6)]
        points = paintTVS(TVS_SIZE).Points()

        dRow = 0
        for row in map_year:
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
                dCol += 1
            dRow += 1

    def TVS_pos(self):
        if self.SelectedTVS != [0, 0]:
            return self.SelectedTVS

    def TVS_symetry(self):
        Cn = int(AZ_dimension/2)
        Sym = [0 for i in range(29)]
        k=0
        Sym[0] = [Cn, Cn], [Cn, Cn]
        for j in range(Cn-1):
            for i in range(1, Cn-j):
                k+=1
                Sym[k] = [Cn+j, Cn-j-i], [Cn-j, Cn+j+i], [Cn-i, Cn-j], [Cn+i, Cn+j],  [Cn-j-i, Cn+i], [Cn+j+i, Cn-i]
        return Sym


    def TVS_change(self):
        dRow = self.SelectedTVS[0]
        dCol = self.SelectedTVS[1]
        TVS_index = [dRow, dCol]
        Cn = int(AZ_dimension / 2)

        if self.SelectedTVS != [0, 0]:  # test if click on somewhere but no on TVS
            Sym = self.TVS_symetry()    # call TVS_symetry function
            for i in range(len(Sym)):   # walk by all Sym koeff list
                if TVS_index in Sym[i]:         # looking up Symetry
                    for SymIndex in Sym[i]:     # get indexes of all symetry TVS from list
                        dRow = SymIndex[0]
                        dCol = SymIndex[1]
                        if self.button == 'left':
                            if map_year[dRow][dCol] == '1':
                                map_year[dRow] = map_year[dRow][:dCol] + '2' + map_year[dRow][(dCol + 1):]
                            elif map_year[dRow][dCol] == '2':
                                map_year[dRow] = map_year[dRow][:dCol] + '3' + map_year[dRow][(dCol + 1):]
                            elif map_year[dRow][dCol] == '3':
                                map_year[dRow] = map_year[dRow][:dCol] + '1' + map_year[dRow][(dCol + 1):]
                        elif self.button == 'right':
                            if map_type[dRow][dCol] == '1':
                                map_type[dRow] = map_type[dRow][:dCol] + '2' + map_type[dRow][(dCol + 1):]
                            elif map_type[dRow][dCol] == '2':
                                map_type[dRow] = map_type[dRow][:dCol] + '3' + map_type[dRow][(dCol + 1):]
                            elif map_type[dRow][dCol] == '3':
                                map_type[dRow] = map_type[dRow][:dCol] + '1' + map_type[dRow][(dCol + 1):]
        self.button = ''

class paintTVS(object):
    def __init__(self, radius):
        TVS_r = radius
        self.TVS_r = radius
        TVS_R = 2 * TVS_r / math.sqrt(3)
        offset = 8 * TVS_r
        dx = 0 - offset
        dy = TVS_R
        self.pointsTVS = [[0 for i in range(AZ_dimension)] for j in range(AZ_dimension)]
        self.txtYearX = [[0 for i in range(AZ_dimension)] for j in range(AZ_dimension)]
        self.txtYearY = [[0 for i in range(AZ_dimension)] for j in range(AZ_dimension)]
        self.txtTypeX = [[0 for i in range(AZ_dimension)] for j in range(AZ_dimension)]
        self.txtTypeY = [[0 for i in range(AZ_dimension)] for j in range(AZ_dimension)]
        # AZ map_year

        dRow = 0
        for row in map_year:
            dCol = 0
            for col in row:
                self.pointsTVS[dRow][dCol] = [(dx + TVS_r, dy + TVS_R / 2), (dx + TVS_r, dy - TVS_R / 2), (dx + 0, dy - TVS_R),
                                              (dx - TVS_r, dy - TVS_R / 2), (dx - TVS_r, dy + TVS_R / 2), (dx + 0, dy + TVS_R)]
                self.txtYearX[dRow][dCol] = dx - TVS_r + TVS_r/5
                self.txtYearY[dRow][dCol] = dy - TVS_R/2 - TVS_R/15
                self.txtTypeX[dRow][dCol] = dx - TVS_r + TVS_r/2.4
                self.txtTypeY[dRow][dCol] = dy-5
                dx += TVS_r * 2
                dCol += 1
            dRow += 1
            dy += TVS_R * 2 - TVS_R / 2
            dx = TVS_r * dRow - offset


    def Points(self):
        return self.pointsTVS

    def Render(self, gc):
        path = [[0 for i in range(AZ_dimension)] for j in range(AZ_dimension)]

        # Change TVS year by color and text
        dRow = 0
        for row in map_year:
            dCol = 0
            for col in row:
                # Draw TVS
                if col == '1':
                    gc.SetPen(wx.Pen('navy', 1))
                    gc.SetBrush(wx.Brush(wx.Colour(185, 225, 185)))
                elif col == '2':
                    gc.SetPen(wx.Pen('navy', 1))
                    gc.SetBrush(wx.Brush(wx.Colour(225, 225, 120)))
                elif col == '3':
                    gc.SetPen(wx.Pen('navy', 1))
                    gc.SetBrush(wx.Brush(wx.Colour(250, 180, 255)))
                else:
                    gc.SetPen(wx.Pen('navy', 1, wx.PENSTYLE_TRANSPARENT))
                    gc.SetBrush(wx.Brush(wx.Colour(255, 255, 255, 0)))

                path[dRow][dCol] = gc.CreatePath()
                for i in range(6):
                    path[dRow][dCol].AddLineToPoint(self.pointsTVS[dRow][dCol][i])
                path[dRow][dCol].CloseSubpath()
                gc.DrawPath(path[dRow][dCol])

                # Draw Text - Year
                gc.SetFont(wx.Font(wx.FontInfo(9).Bold()), 'navy')
                if col == '1':
                    gc.DrawText('1', self.txtYearX[dRow][dCol], self.txtYearY[dRow][dCol])
                elif col == '2':
                    gc.DrawText('2', self.txtYearX[dRow][dCol], self.txtYearY[dRow][dCol])
                elif col == '3':
                    gc.DrawText('3', self.txtYearX[dRow][dCol], self.txtYearY[dRow][dCol])

                dCol += 1
            dRow += 1

        # Change TVS type text
        dRow = 0
        for row in map_type:
            dCol = 0
            for col in row:
                # Draw Text - Type
                FontType = wx.Font(wx.FontInfo(10).Bold())
                gc.SetFont(FontType, 'navy')
                if col == '1':
                    gc.DrawText(TVS_type[0], self.txtTypeX[dRow][dCol], self.txtTypeY[dRow][dCol])
                elif col == '2':
                    gc.DrawText(TVS_type[1], self.txtTypeX[dRow][dCol], self.txtTypeY[dRow][dCol])
                elif col == '3':
                    gc.DrawText(TVS_type[2], self.txtTypeX[dRow][dCol], self.txtTypeY[dRow][dCol])

                dCol += 1
            dRow += 1

class clAZonePanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.SetBackgroundColour('WHITE')
        # Events by Paint, LeftMouseClick, ..
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClick_Lbtn)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnClick_Rbtn)

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

    def OnClick_Lbtn(self, evt):
        # Define Click position
        clickXY = [evt.GetPosition()[0], evt.GetPosition()[1]]
        print('TVS number:', SelectObject('left', clickXY).TVS_pos(), 'was selected')
        # Define clicked TVS
        SelectObject('left', clickXY).TVS_change()
        # Painting through Buffer
        self.InitBuffer()

    def OnClick_Rbtn(self, evt):
        # Define Click position
        clickXY = [evt.GetPosition()[0], evt.GetPosition()[1]]
        print('TVS number:', SelectObject('right', clickXY).TVS_pos(), 'was selected')
        # Define clicked TVS
        SelectObject('right', clickXY).TVS_change()
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