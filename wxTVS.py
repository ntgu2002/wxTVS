import wx
import math
#from wx.lib.pubsub import pub
from pubsub import pub

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

max_NumTVS = 5
TVS_type = ['XXXXXX' for i in range(max_NumTVS)]
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
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        self.sizer_Main = wx.BoxSizer(wx.VERTICAL)

        # 1-srt (Сaption Open/Save buttons)
        self.Label_OpenSave = wx.StaticText(self, -1, "Open/Save AZ map:", (0, 0), (240, 20), wx.ALIGN_LEFT)
        self.sizer_Main.Add(self.Label_OpenSave, 0, wx.LEFT | wx.RIGHT | wx.UP | wx.EXPAND, 5)

        # 2-srt (Open/Save buttons)
        self.Btn_Open = wx.Button(self, -1, "Open", (0, 0), (100, 27))
        self.Btn_Save = wx.Button(self, -1, "Save", (0, 0), (100, 27))
        self.Btn_Open.Bind(wx.EVT_BUTTON, self.Click_Btn_Open)
        self.Btn_Save.Bind(wx.EVT_BUTTON, self.Click_Btn_Save)
        self.sizer_OpenSaveBtn = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_OpenSaveBtn.Add(self.Btn_Open, 1, wx.ALL | wx.ALIGN_CENTER | wx.EXPAND, 0)
        self.sizer_OpenSaveBtn.Add(self.Btn_Save, 1, wx.ALL | wx.ALIGN_CENTER | wx.EXPAND, 0)
        self.sizer_Main.Add(self.sizer_OpenSaveBtn, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)

        # 3-srt (Empty)
        self.sizer_Main.AddSpacer(20)

        # 4-srt (Number of assemblies with SpinCtrl)
        self.maxSpinCtrl_NumTVS = max_NumTVS
        self.Label_NumTVS = wx.StaticText(self, -1, "Number of assemblies:", (0, 0), (140, 20), wx.ALIGN_LEFT)
        self.SpinCtrl_NumTVS = wx.SpinCtrl(self, -1, "", (0, 0), (100, 20), min=1, max=self.maxSpinCtrl_NumTVS, initial=3)
        self.SpinCtrl_NumTVS.Bind(wx.EVT_SPINCTRL, self.Click_SpinCtrl_NumTVS)
        self.sizer_NumTVS = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_NumTVS.Add(self.Label_NumTVS, 1, wx.ALL | wx.ALIGN_LEFT, 0)
        self.sizer_NumTVS.Add(self.SpinCtrl_NumTVS, 1, wx.ALL | wx.EXPAND, 0)
        self.sizer_Main.Add(self.sizer_NumTVS, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)

        # 5-srt (Empty)
        self.sizer_Main.AddSpacer(6)

        # 6-srt TextCtrl with names of TVSs
        #str_TVS_name = ['XXXXXXX' for i in range(self.maxSpinCtrl_NumTVS)]
        TVS_type[0] = 'E495A18'
        TVS_type[1] = 'E460A06'
        TVS_type[2] = 'E445A22'
        self.TextCtrl_TVS_name = [0 for i in range(self.maxSpinCtrl_NumTVS)]
        self.Btn_EditTVS_name = [0 for i in range(self.maxSpinCtrl_NumTVS)]
        self.sizer_TVS_name = [0 for i in range(self.maxSpinCtrl_NumTVS)]
        self.TVSid = [0 for i in range(self.maxSpinCtrl_NumTVS)]

        for i in range(self.maxSpinCtrl_NumTVS):
            self.TVSid[i] = wx.NewId()
            self.TextCtrl_TVS_name[i] = wx.TextCtrl(self, self.TVSid[i], TVS_type[i], (0, 0), (120, 20))
            self.TextCtrl_TVS_name[i].Bind(wx.EVT_TEXT, self.OnKeyTyped_TVS_name)
            self.Btn_EditTVS_name[i] = wx.Button(self, -1, "Edit..", (0, 0), (100, 27))
            self.sizer_TVS_name[i] = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer_TVS_name[i].Add(self.TextCtrl_TVS_name[i], 1, wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 0)
            self.sizer_TVS_name[i].AddSpacer(20)
            self.sizer_TVS_name[i].Add(self.Btn_EditTVS_name[i], 1, wx.ALL | wx.EXPAND, 0)
            self.sizer_Main.Add(self.sizer_TVS_name[i], 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        # Hide extra TVSs
        for i in range(self.SpinCtrl_NumTVS.GetValue(), self.maxSpinCtrl_NumTVS):
            self.sizer_TVS_name[i].Hide(self.TextCtrl_TVS_name[i])
            self.sizer_TVS_name[i].Hide(self.Btn_EditTVS_name[i])

        # 7-srt (Empty)
        self.sizer_Main.AddSpacer(20)

        self.SetSizer(self.sizer_Main)

        self.Layout()



    def Click_Btn_Open(self, event):
        Open_Dialog = wx.FileDialog(None, 'Choose a file', '', '', '*.*', wx.FD_OPEN)
        with Open_Dialog as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                print(dlg.GetPath())

    def Click_Btn_Save(self, event):
        Open_Dialog = wx.FileDialog(None, 'Choose a file', '', '', '*.*', wx.FD_SAVE)
        with Open_Dialog as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                print(dlg.GetPath())
                with open(dlg.GetPath(), 'w') as file:
                    for row in map_year:
                        file.writelines(row)
                        file.writelines('\n')

    def Click_SpinCtrl_NumTVS(self, event):
        for i in range(self.SpinCtrl_NumTVS.GetValue()):
            self.sizer_TVS_name[i].Show(self.TextCtrl_TVS_name[i])
            self.sizer_TVS_name[i].Show(self.Btn_EditTVS_name[i])
            self.sizer_TVS_name[i].Layout()
        for i in range(self.SpinCtrl_NumTVS.GetValue(), self.maxSpinCtrl_NumTVS):
            self.sizer_TVS_name[i].Hide(self.TextCtrl_TVS_name[i])
            self.sizer_TVS_name[i].Hide(self.Btn_EditTVS_name[i])
            self.sizer_TVS_name[i].Layout()
        self.Layout()

        #print('Publish something via pubsub')
        #anObj = dict(a=456, b='abc')
        pub.sendMessage('Control Panel Options', arg1=self.SpinCtrl_NumTVS.GetValue(), arg2=TVS_type)

    def OnKeyTyped_TVS_name(self, event):
        print(event.GetId())
        print(event.GetString())
        if event.GetId() == self.TVSid[1]:
            print('SECOND!!')


#    def GetNumTVS(self):
#        NumTVS = self.SpinCtrl_NumTVS.GetValue()
#        return NumTVS

class SelectObject(object):
    def __init__(self, btn, clickXY, NumTVS):
        self.SelectedTVS = [0, 0]
        self.button = btn
        self.NumTVS = NumTVS
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


    def TVS_change(self, *args, **kwargs):
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

                        # Modification MAP_YEAR
                        if self.button == 'left':
                            if map_year[dRow][dCol] == '1':
                                map_year[dRow] = map_year[dRow][:dCol] + '2' + map_year[dRow][(dCol + 1):]
                            elif map_year[dRow][dCol] == '2':
                                map_year[dRow] = map_year[dRow][:dCol] + '3' + map_year[dRow][(dCol + 1):]
                            elif map_year[dRow][dCol] == '3':
                                map_year[dRow] = map_year[dRow][:dCol] + '1' + map_year[dRow][(dCol + 1):]

                        # Modification MAP_TYPE
                        elif self.button == 'right':
                            if map_type[dRow][dCol] == '1':
                                if self.NumTVS > 1: map_type[dRow] = map_type[dRow][:dCol] + '2' + map_type[dRow][(dCol + 1):]
                                else:               map_type[dRow] = map_type[dRow][:dCol] + '1' + map_type[dRow][(dCol + 1):]
                            elif map_type[dRow][dCol] == '2':
                                if self.NumTVS > 2: map_type[dRow] = map_type[dRow][:dCol] + '3' + map_type[dRow][(dCol + 1):]
                                else:               map_type[dRow] = map_type[dRow][:dCol] + '1' + map_type[dRow][(dCol + 1):]
                            elif map_type[dRow][dCol] == '3':
                                if self.NumTVS > 3: map_type[dRow] = map_type[dRow][:dCol] + '4' + map_type[dRow][(dCol + 1):]
                                else:               map_type[dRow] = map_type[dRow][:dCol] + '1' + map_type[dRow][(dCol + 1):]
                            elif map_type[dRow][dCol] == '4':
                                if self.NumTVS > 4: map_type[dRow] = map_type[dRow][:dCol] + '5' + map_type[dRow][(dCol + 1):]
                                else:               map_type[dRow] = map_type[dRow][:dCol] + '1' + map_type[dRow][(dCol + 1):]
                            elif map_type[dRow][dCol] == '5':
                                map_type[dRow] = map_type[dRow][:dCol] + '1' + map_type[dRow][(dCol + 1):]


        self.button = ''

    def test_map(self):
        if map_type[dRow][dCol] == '1':
            map_type[dRow] = map_type[dRow][:dCol] + '2' + map_type[dRow][(dCol + 1):]


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
                self.txtTypeX[dRow][dCol] = dx - TVS_r + TVS_r/3.3
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
                FontType = wx.Font(wx.FontInfo(9).Bold())
                gc.SetFont(FontType, 'navy')
                if col == '1':
                    gc.DrawText(TVS_type[0], self.txtTypeX[dRow][dCol], self.txtTypeY[dRow][dCol])
                elif col == '2':
                    gc.DrawText(TVS_type[1], self.txtTypeX[dRow][dCol], self.txtTypeY[dRow][dCol])
                elif col == '3':
                    gc.DrawText(TVS_type[2], self.txtTypeX[dRow][dCol], self.txtTypeY[dRow][dCol])
                elif col == '4':
                    gc.DrawText(TVS_type[3], self.txtTypeX[dRow][dCol], self.txtTypeY[dRow][dCol])
                elif col == '5':
                    gc.DrawText(TVS_type[4], self.txtTypeX[dRow][dCol], self.txtTypeY[dRow][dCol])

                dCol += 1
            dRow += 1

class clAZonePanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.SetBackgroundColour('WHITE')
        self.NumTVS = 3     # initial (default) value number of TVSs = 3
        self.TVSss_type = ['XXXXX1', 'XXXXX2', 'XXXXX3', 'XXXXX4', 'XXXXX5']
        # Events by Paint, LeftMouseClick, ..
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClick_Lbtn)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnClick_Rbtn)
        # Pub Sub method getting values from Control Panel
        pub.subscribe(self.ListenerControlPanel, 'Control Panel Options')

    def ListenerControlPanel(self, arg1, arg2=None):
        self.NumTVS = arg1
        print(self.NumTVS)
        if arg2:
            self.TVSss_type = arg2
            for i in range(len(arg2)):
                print(self.TVSss_type[i])


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
        print('TVS number:', SelectObject('left', clickXY, self.NumTVS).TVS_pos(), 'was selected')
        # Define clicked TVS
        SelectObject('left', clickXY, self.NumTVS).TVS_change()
        # Painting through Buffer
        self.InitBuffer()

    def OnClick_Rbtn(self, evt):
        # Define Click position
        clickXY = [evt.GetPosition()[0], evt.GetPosition()[1]]
        print('TVS number:', SelectObject('right', clickXY, self.NumTVS).TVS_pos(), 'was selected')
        # Define clicked TVS
        SelectObject('right', clickXY, self.NumTVS).TVS_change()
        # Painting through Buffer
        self.InitBuffer()


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, 'Active Zone VVER maker', size=(1290, 1010))

        #ControlPanel = clControlPanel(self, -1, size=(240, 1010), style=wx.SUNKEN_BORDER)
        ControlPanel = clControlPanel(self)
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