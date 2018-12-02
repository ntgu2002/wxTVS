import wx
import math
from pubsub import pub
from wx.lib.floatcanvas import NavCanvas, FloatCanvas
import wx.grid
import wx.lib.agw.pycollapsiblepane

AZ_dimension = 17
max_NumTVS   = 5
init_NumTVS  = 3
max_NumPIN   = 8
init_NumPIN  = 4

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

TVS_dimension = 23
map_PIN_type = [0 for i in range(max_NumTVS)]
for i in range(max_NumTVS):
    map_PIN_type[i] = [
        '-----------------------',  # 1
        '-----------11111111111-',  # 2
        '----------111111111111-',  # 3
        '---------1111111111111-',  # 4
        '--------11111111111111-',  # 5
        '-------111111191111111-',  # 6
        '------1111191111911111-',  # 7
        '-----11111111111111111-',  # 8
        '----111191119111191111-',  # 9
        '---1111111111191111111-',  # 10
        '--11111119111111111111-',  # 11
        '-111119111191111911111-',  # 12
        '-11111111111191111111--',  # 13
        '-1111111911111111111---',  # 14
        '-111191111911191111----',  # 15
        '-11111111111111111-----',  # 16
        '-1111191111911111------',  # 17
        '-111111191111111-------',  # 18
        '-11111111111111--------',  # 19
        '-1111111111111---------',  # 20
        '-111111111111----------',  # 21
        '-11111111111-----------',  # 22
        '-----------------------'  # 23
]

max_Material = 30
num_Materials = 3
MaxNucl = 30
Material = [0 for i in range(max_Material)]
TmpMaterial = [0 for i in range(max_Material)]
for i in range(max_Material):
    Material[i] = {'Name': '', 'Den': '', 'Tmp': '', 'Burn': False, 'NNucl': 0, 'Inv': ['' for i in range(MaxNucl)], 'Val': ['' for i in range(MaxNucl)]}
    TmpMaterial[i] = {'Name': '', 'Den': '', 'Tmp': '', 'Burn': False, 'NNucl': 0, 'Inv': ['' for i in range(MaxNucl)], 'Val': ['' for i in range(MaxNucl)]}

Material[0]['Name'] = 'ZrNb_clad'
Material[0]['Den'] = '-6.55'
Material[0]['Tmp'] = '613'
Material[0]['Burn'] = False
Material[0]['NNucl'] = 2
Material[0]['Inv'][0] = '40000.06c'
Material[0]['Inv'][1] = '41093.06c'
Material[0]['Val'][0] = '-0.99'
Material[0]['Val'][1] = '-0.01'

Material[1]['Name'] = 'Moderator'
Material[1]['Den'] = '-0.7122'
Material[1]['Tmp'] = '573'
Material[1]['Burn'] = False
Material[1]['NNucl'] = 2
Material[1]['Inv'][0] = '1001.03c'
Material[1]['Inv'][1] = '8016.03c'
Material[1]['Val'][0] = '2'
Material[1]['Val'][1] = '1'

Material[2]['Name'] = 'Fuel-4.4%'
Material[2]['Den'] = '-10.5'
Material[2]['Tmp'] = '900'
Material[2]['Burn'] = True
Material[2]['NNucl'] = 5
Material[2]['Inv'][0] = '92238.09c'
Material[2]['Inv'][1] = '92236.09c'
Material[2]['Inv'][2] = '92235.09c'
Material[2]['Inv'][3] = '92234.09c'
Material[2]['Inv'][4] = '8016.09c'
Material[2]['Val'][0] = '-0.842116'
Material[2]['Val'][1] = '-0.000178'
Material[2]['Val'][2] = '-0.038783'
Material[2]['Val'][3] = '-0.000345'
Material[2]['Val'][4] = '-0.118577'



class TVSsize(object):
    def __init__(self):
        self.r = 35
        self.R = 2 * self.r / math.sqrt(3)
        self.color_year = ['SPRING GREEN', 'YELLOW', 'PINK']

class PINsize(object):
    def __init__(self):
        self.r = 23
        self.R = 2 * self.r / math.sqrt(3)
        self.color_type = ['SPRING GREEN', 'YELLOW', 'PINK', 'AQUAMARINE', 'LIGHT BLUE', 'CORAL', 'ORCHID', 'DIM GREY']

class ControlPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, size=(220, 1010))
        self.sizer_Main = wx.BoxSizer(wx.VERTICAL)
        self.sizer_Main.AddSpacer(2)

        # 1-box (Open/Save buttons)
        self.Staticbox_OpenSave = wx.StaticBox(self, -1, label="Open/Save AZ map")
        self.sizer_OpenSave = wx.StaticBoxSizer(self.Staticbox_OpenSave, wx.HORIZONTAL)

        self.Btn_Open = wx.Button(self, -1, "Open")
        self.Btn_Save = wx.Button(self, -1, "Save")
        self.Btn_Open.Bind(wx.EVT_BUTTON, self.click_Btn_Open)
        self.Btn_Save.Bind(wx.EVT_BUTTON, self.click_Btn_Save)

        self.sizer_OpenSave.Add(self.Btn_Open, 1, wx.ALL | wx.ALIGN_CENTER | wx.EXPAND, 5)
        self.sizer_OpenSave.Add(self.Btn_Save, 1, wx.ALL | wx.ALIGN_CENTER | wx.EXPAND, 5)
        self.sizer_Main.Add(self.sizer_OpenSave, 0, wx.ALL | wx.EXPAND, 5)

        # 2-box (Settings: Symmetry, 1/6 Zoom)
        self.Staticbox_Settings = wx.StaticBox(self, -1, label="AZ Settings")
        self.sizer_Settings = wx.StaticBoxSizer(self.Staticbox_Settings, wx.HORIZONTAL)

        self.CheckBox_Symmetry = wx.CheckBox(self, -1, label='Symmetry')
        self.CheckBox_Symmetry.Bind(wx.EVT_CHECKBOX, self.click_CheckBox_Sym)
        self.CheckBox_Symmetry.SetValue(True)
        self.CheckBox_Zoom = wx.CheckBox(self, -1, label='1/6 Zoom')
        self.CheckBox_Zoom.Bind(wx.EVT_CHECKBOX, self.click_CheckBox_Zoom)

        self.sizer_Settings.Add(self.CheckBox_Symmetry, 1, wx.ALL | wx.ALIGN_LEFT, 5)
        self.sizer_Settings.Add(self.CheckBox_Zoom, 1, wx.ALL | wx.ALIGN_LEFT, 5)
        self.sizer_Main.Add(self.sizer_Settings, 0, wx.ALL | wx.EXPAND, 5)


        # 3-box (Assembly types)
        self.Staticbox_AssemblyTypes = wx.StaticBox(self, -1, label="Assembly types")
        self.sizer_AssemblyTypes = wx.StaticBoxSizer(self.Staticbox_AssemblyTypes, wx.VERTICAL)
        self.sizer_NumTVS = wx.BoxSizer(wx.HORIZONTAL)

        self.maxSpinCtrl_NumTVS = max_NumTVS
        self.Label_NumTVS = wx.StaticText(self, -1, "N of Assembly types:", (0, 0), (120, 20), wx.ALIGN_LEFT)
        self.SpinCtrl_NumTVS = wx.SpinCtrl(self, -1, "", (0, 0), (100, 20), min=1, max=self.maxSpinCtrl_NumTVS, initial=init_NumTVS)
        self.SpinCtrl_NumTVS.Bind(wx.EVT_SPINCTRL, self.click_SpinCtrl_NumTVS)

        self.sizer_NumTVS.Add(self.Label_NumTVS, 1, wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 5)
        self.sizer_NumTVS.Add(self.SpinCtrl_NumTVS, 1, wx.ALL | wx.EXPAND, 5)
        self.sizer_AssemblyTypes.Add(self.sizer_NumTVS, 1, wx.ALL | wx.EXPAND, 0)

        self.TVS_type = ['XXXXXX' for i in range(self.maxSpinCtrl_NumTVS)]
        self.TVS_type[0] = 'E495A18'
        self.TVS_type[1] = 'E460A06'
        self.TVS_type[2] = 'E445A22'
        self.TextCtrl_TVS_name = [0 for i in range(self.maxSpinCtrl_NumTVS)]
        #self.Btn_EditTVS_name = [0 for i in range(self.maxSpinCtrl_NumTVS)]
        self.sizer_TVS_name = [0 for i in range(self.maxSpinCtrl_NumTVS)]
        self.TVSid = [0 for i in range(self.maxSpinCtrl_NumTVS)]

        for i in range(self.maxSpinCtrl_NumTVS):
            self.TVSid[i] = wx.NewId()
            self.TextCtrl_TVS_name[i] = wx.TextCtrl(self, self.TVSid[i], self.TVS_type[i], (0, 0), (120, 20), style=wx.TE_PROCESS_ENTER)
            self.TextCtrl_TVS_name[i].Bind(wx.EVT_TEXT_ENTER, self.onKeyTyped_TVS_name)
            #self.Btn_EditTVS_name[i] = wx.Button(self, -1, "Edit..", (0, 0), (60, 27))
            self.sizer_TVS_name[i] = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer_TVS_name[i].Add(self.TextCtrl_TVS_name[i], 0, wx.RIGHT | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 5)
            #self.sizer_TVS_name[i].AddSpacer(20)
            #self.sizer_TVS_name[i].Add(self.Btn_EditTVS_name[i], 0, wx.LEFT | wx.ALIGN_RIGHT, 5)
            self.sizer_TVS_name[i].SetMinSize(120,27)
            #self.sizer_AssemblyTypes.Add(self.sizer_TVS_name[i], 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
            self.sizer_AssemblyTypes.Add(self.sizer_TVS_name[i], 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        # Hide extra TVSs
        for i in range(self.SpinCtrl_NumTVS.GetValue(), self.maxSpinCtrl_NumTVS):
            #self.sizer_Main.Hide(self.sizer_TVS_name[i])
            self.sizer_AssemblyTypes.Hide(self.sizer_TVS_name[i])

        self.sizer_Main.Add(self.sizer_AssemblyTypes, 0, wx.ALL | wx.EXPAND, 5)

        # 4-box (Pin types)
        self.Staticbox_PinTypes = wx.StaticBox(self, -1, label="Pin types")
        self.sizer_PinTypes = wx.StaticBoxSizer(self.Staticbox_PinTypes, wx.VERTICAL)
        self.sizer_NumPIN = wx.BoxSizer(wx.HORIZONTAL)

        self.maxSpinCtrl_NumPIN = max_NumPIN
        self.Label_NumPIN = wx.StaticText(self, -1, "N of pin types:", (0, 0), (120, 20), wx.ALIGN_LEFT)
        self.SpinCtrl_NumPIN = wx.SpinCtrl(self, -1, "", (0, 0), (100, 20), min=1, max=self.maxSpinCtrl_NumPIN, initial=init_NumPIN)
        self.SpinCtrl_NumPIN.Bind(wx.EVT_SPINCTRL, self.click_SpinCtrl_NumPIN)

        self.sizer_NumPIN.Add(self.Label_NumPIN, 1, wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 5)
        self.sizer_NumPIN.Add(self.SpinCtrl_NumPIN, 1, wx.ALL | wx.EXPAND, 5)
        self.sizer_PinTypes.Add(self.sizer_NumPIN, 1, wx.ALL | wx.EXPAND, 0)

        self.PIN_type = ['xxxxxx' for i in range(self.maxSpinCtrl_NumPIN)]
        self.PIN_type[0] = 'p49'
        self.PIN_type[1] = 'p44'
        self.PIN_type[2] = 'p36g5'
        self.PIN_type[3] = 'p36g8'
        self.RadioBtn_PIN_num = [0 for i in range(self.maxSpinCtrl_NumPIN)]
        self.TextCtrl_PIN_name = [0 for i in range(self.maxSpinCtrl_NumPIN)]
        self.Btn_EditPIN_name = [0 for i in range(self.maxSpinCtrl_NumPIN)]
        self.sizer_PIN_name = [0 for i in range(self.maxSpinCtrl_NumPIN)]
        self.PINid = [0 for i in range(self.maxSpinCtrl_NumPIN)]

        for i in range(self.maxSpinCtrl_NumPIN):
            self.PINid[i] = wx.NewId()
            self.RadioBtn_PIN_num[i] = wx.RadioButton(self, self.PINid[i], str(i+1))
            self.RadioBtn_PIN_num[i].Bind(wx.EVT_RADIOBUTTON, self.onRadioBtnPIN_Cliked)
            self.TextCtrl_PIN_name[i] = wx.TextCtrl(self, self.PINid[i], self.PIN_type[i], (0, 0), (93, 20))
            self.TextCtrl_PIN_name[i].Bind(wx.EVT_TEXT, self.onKeyTyped_PIN_name)
            self.TextCtrl_PIN_name[i].Bind(wx.EVT_SET_FOCUS, self.onSetFocus_PIN_name)
            self.Btn_EditPIN_name[i] = wx.Button(self, self.PINid[i], "Edit", (0, 0), (60, 27))
            self.Btn_EditPIN_name[i].Bind(wx.EVT_BUTTON, self.click_Btn_EditPIN)
            self.sizer_PIN_name[i] = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer_PIN_name[i].Add(self.RadioBtn_PIN_num[i], 0, wx.RIGHT | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 3)
            self.sizer_PIN_name[i].Add(self.TextCtrl_PIN_name[i], 0, wx.RIGHT | wx.LEFT | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 0)
            self.sizer_PIN_name[i].Add(self.Btn_EditPIN_name[i], 0, wx.LEFT | wx.ALIGN_RIGHT, 5)
            #self.sizer_PIN_name[i].SetMinSize(190,27)
            self.sizer_PinTypes.Add(self.sizer_PIN_name[i], 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        # Hide extra PINs
        for i in range(self.SpinCtrl_NumPIN.GetValue(), self.maxSpinCtrl_NumPIN):
            self.sizer_PinTypes.Hide(self.sizer_PIN_name[i])

        self.RadioBtn_PIN_num[0].SetValue(True)

        self.sizer_Main.Add(self.sizer_PinTypes, 0, wx.ALL | wx.EXPAND, 5)

        # 5-box (Materials)
        self.Staticbox_Materials = wx.StaticBox(self, -1, label="Materials")
        self.sizer_Materials = wx.StaticBoxSizer(self.Staticbox_Materials, wx.HORIZONTAL)

        self.Btn_EditMat = wx.Button(self, -1, "Edit Materials")
        self.Btn_EditMat.Bind(wx.EVT_BUTTON, self.click_Btn_EditMat)

        self.sizer_Materials.Add(self.Btn_EditMat, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        self.sizer_Main.Add(self.sizer_Materials, 0, wx.ALL | wx.EXPAND, 5)



        self.SetSizer(self.sizer_Main)
        self.Layout()


    def click_Btn_Open(self, event):
        Open_Dialog = wx.FileDialog(None, 'Choose a file', '', '', '*.*', wx.FD_OPEN)
        with Open_Dialog as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                print(dlg.GetPath())

    def click_Btn_Save(self, event):
        Open_Dialog = wx.FileDialog(None, 'Choose a file', '', '', '*.*', wx.FD_SAVE)
        with Open_Dialog as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                print(dlg.GetPath())
                with open(dlg.GetPath(), 'w') as file:
                    # SAVE AZ MAP
                    for i in range(AZ_dimension):
                        for j in range(AZ_dimension):
                            if map_type[i][j] == '-': saveTVStype = '------'
                            else:  saveTVStype = self.TextCtrl_TVS_name[int(map_type[i][j])-1].GetValue()
                            file.write(map_year[i][j]+'_'+saveTVStype+' ')
                        file.writelines('\n')
                    file.writelines('\n')

                    # SAVE TVSs MAP
                    for k in range(self.SpinCtrl_NumTVS.GetValue()):
                        for i in range(TVS_dimension):
                            for j in range(TVS_dimension):
                                file.write(map_PIN_type[k][i][j])
                            file.writelines('\n')
                        file.writelines('\n')

                    # SAVE Materials Data
                    for i in range(max_Material):
                        if Material[i]['Name'] != '':
                            file.write('mat ' + Material[i]['Name'] + '\t' + Material[i]['Den'] + '\t' + 'tmp ' + Material[i]['Tmp'])
                            if Material[i]['Burn'] == True: file.write('\tburn 1')
                            file.write('\n')
                            for j in range(MaxNucl):
                                if Material[i]['Inv'][j] != '':
                                    file.write(Material[i]['Inv'][j] + '\t' + Material[i]['Val'][j] + '\n')
                            file.writelines('\n')


    def click_CheckBox_Sym(self, event):
        pub.sendMessage('CPanel Symmetry', arg1=self.CheckBox_Symmetry.GetValue())

    def click_CheckBox_Zoom(self, event):
        pub.sendMessage('CPanel Zoom', arg1=self.CheckBox_Zoom.GetValue())


    def click_SpinCtrl_NumTVS(self, event):
        for i in range(self.SpinCtrl_NumTVS.GetValue()):
            self.sizer_TVS_name[i].Show(self.TextCtrl_TVS_name[i])
            #self.sizer_TVS_name[i].Show(self.Btn_EditTVS_name[i])
        for i in range(self.SpinCtrl_NumTVS.GetValue(), self.maxSpinCtrl_NumTVS):
            self.sizer_TVS_name[i].Hide(self.TextCtrl_TVS_name[i])
            #self.sizer_TVS_name[i].Hide(self.Btn_EditTVS_name[i])
        #self.Layout()
        pub.sendMessage('CPanel TVS', arg1=self.SpinCtrl_NumTVS.GetValue(), arg2=self.TVS_type)

    def onKeyTyped_TVS_name(self, event):
        #print(event.GetId())
        #print(event.GetString())
        for i in range(max_NumTVS):
            if self.TVSid[i] == event.GetId():
                self.TVS_type[i] = event.GetString()
                pub.sendMessage('CPanel TVS', arg1=self.SpinCtrl_NumTVS.GetValue(), arg2=self.TVS_type)

    def click_SpinCtrl_NumPIN(self, event):
        for i in range(self.SpinCtrl_NumPIN.GetValue()):
            self.sizer_PIN_name[i].Show(self.RadioBtn_PIN_num[i])
            self.sizer_PIN_name[i].Show(self.TextCtrl_PIN_name[i])
            self.sizer_PIN_name[i].Show(self.Btn_EditPIN_name[i])
        for i in range(self.SpinCtrl_NumPIN.GetValue(), self.maxSpinCtrl_NumPIN):
            self.sizer_PIN_name[i].Hide(self.RadioBtn_PIN_num[i])
            self.sizer_PIN_name[i].Hide(self.TextCtrl_PIN_name[i])
            self.sizer_PIN_name[i].Hide(self.Btn_EditPIN_name[i])
            if self.RadioBtn_PIN_num[i].GetValue():
                self.RadioBtn_PIN_num[0].SetValue(True)
        for i in range(self.maxSpinCtrl_NumPIN):
            if self.RadioBtn_PIN_num[i].GetValue():
                self.Selected_PIN = i

        pub.sendMessage('CPanel PIN', arg1=self.SpinCtrl_NumPIN.GetValue(), arg2=[self.Selected_PIN, self.PIN_type])
        self.Layout()

    def onRadioBtnPIN_Cliked(self, event):
        for i in range(self.maxSpinCtrl_NumPIN):
            if self.RadioBtn_PIN_num[i].GetValue():
                self.Selected_PIN = i
        pub.sendMessage('CPanel PIN', arg1=self.SpinCtrl_NumPIN.GetValue(), arg2=[self.Selected_PIN, self.PIN_type])


    def onKeyTyped_PIN_name(self, event):
        pass
        #for i in range(max_NumPIN):
        #    if self.PINid[i] == event.GetId():
        #        self.PIN_type[i] = event.GetString()
        #        pub.sendMessage('CPanel PIN', arg1=self.SpinCtrl_NumPIN.GetValue(), arg2=self.PIN_type)

    def onSetFocus_PIN_name(self, event):
        i = self.PINid.index(event.GetId())
        self.RadioBtn_PIN_num[i].SetValue(True)
        event.Skip()
        self.onRadioBtnPIN_Cliked(event)


    def click_Btn_EditPIN(self, event):
        DialogPIN = PINsEdit(None)
        DialogPIN.CenterOnScreen()
        result = DialogPIN.ShowModal()
        if result == wx.ID_OK:
            print('OK -> close')
        DialogPIN.Destroy()


    def click_Btn_EditMat(self, event):
        DialogMaterial = MaterialEdit(None)
        DialogMaterial.CenterOnScreen()

        result = DialogMaterial.ShowModal()
        if result == wx.ID_OK:
            for i in range(len(TmpMaterial)):
                if TmpMaterial[i]['Name'] != '':
                    mName = TmpMaterial[i]['Name']
                    Material[i]['Name'] = mName
                    mDen = TmpMaterial[i]['Den']
                    Material[i]['Den'] = mDen
                    mTmp = TmpMaterial[i]['Tmp']
                    Material[i]['Tmp'] = mTmp
                    mBurn = TmpMaterial[i]['Burn']
                    Material[i]['Burn'] = mBurn
                    mNNucl = TmpMaterial[i]['NNucl']
                    Material[i]['NNucl'] = mNNucl

                    for j in range(Material[i]['NNucl']):
                        mInv = TmpMaterial[i]['Inv'][j]
                        Material[i]['Inv'][j] = mInv
                    for j in range(Material[i]['NNucl']):
                        mVal = TmpMaterial[i]['Val'][j]
                        Material[i]['Val'][j] = mVal
        DialogMaterial.Destroy()

class PINsEdit(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, title='Material Edit', size=(730, 304), style=wx.DEFAULT_DIALOG_STYLE)

        self.initNumCell = 5
        self.maxNumCell = 30

        sizer_Main = wx.BoxSizer(wx.VERTICAL)
        sizer_NumCell = wx.BoxSizer(wx.HORIZONTAL)
        sizer_Label = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_GeneralCell = wx.BoxSizer(wx.VERTICAL)
        sizer_Color = wx.BoxSizer(wx.HORIZONTAL)

        label_NumCell = wx.StaticText(self, -1, "Number of Cells:", (0, 0), (90, 20), wx.ALIGN_LEFT)
        self.spinCtrl_NumCell = wx.SpinCtrl(self, -1, "", (0, 0), (90, 20), min=1, max=self.maxNumCell, initial=self.initNumCell)
        self.spinCtrl_NumCell.Bind(wx.EVT_SPINCTRL, self.click_SpinCtrl_NumCell)

        label_Material = wx.StaticText(self, -1, "Material:", (0, 0), (90, 20), wx.ALIGN_LEFT)
        label_Radius = wx.StaticText(self, -1, "Radius:", (0, 0), (90, 20), wx.ALIGN_LEFT)


        self.textCtrl_Material = [0 for i in range(self.maxNumCell)]
        self.textCtrl_Radius = [0 for i in range(self.maxNumCell)]
        self.sizer_Cell = [0 for i in range(self.maxNumCell)]

        for i in range(self.maxNumCell):
            self.textCtrl_Material[i] = wx.TextCtrl(self, -1, 'tmp', (0, 0), (90, 20))
            self.textCtrl_Radius[i] = wx.TextCtrl(self, -1, 'tmp', (0, 0), (90, 20))
            #self.TextCtrl_MAT_name[i].Bind(wx.EVT_TEXT, self.onKeyTyped_MAT_name)
            self.sizer_Cell[i] = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer_Cell[i].Add(self.textCtrl_Material[i], 0, wx.RIGHT | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 3)
            self.sizer_Cell[i].Add(self.textCtrl_Radius[i], 0, wx.RIGHT | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 3)
            self.sizer_GeneralCell.Add(self.sizer_Cell[i], 0, wx.ALL | wx.EXPAND, 2)
        # Hide extra Cells
        for i in range(self.spinCtrl_NumCell.GetValue(), self.maxNumCell):
            self.sizer_GeneralCell.Hide(self.sizer_Cell[i])

        label_PinColor = wx.StaticText(self, -1, "PIN Color:", (0, 0), (90, 20), wx.ALIGN_LEFT)
        btn_PinColor = wx.Button(self, -1, "Color", (0, 0), (90, 20))



        sizer_NumCell.Add(label_NumCell, 0, wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 3)
        sizer_NumCell.Add(self.spinCtrl_NumCell, 0, wx.ALL, 3)
        sizer_Label.Add(label_Material, 0, wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 3)
        sizer_Label.Add(label_Radius, 0, wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 3)
        sizer_Color.Add(label_PinColor, 0, wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 3)
        sizer_Color.Add(btn_PinColor, 0, wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 3)

        sizer_Main.Add(sizer_NumCell, 0, wx.ALL, 0)
        sizer_Main.Add(sizer_Label, 0, wx.ALL, 0)
        sizer_Main.Add(self.sizer_GeneralCell, 0, wx.ALL, 0)
        sizer_Main.Add(sizer_Color, 0, wx.ALL, 0)

        self.SetSizer(sizer_Main)
        self.SetSize(self.GetBestSize())



    def click_SpinCtrl_NumCell(self, event):
        self.NumCell = self.spinCtrl_NumCell.GetValue()
        for i in range(self.NumCell):
            self.sizer_Cell[i].Show(self.textCtrl_Material[i])
            self.sizer_Cell[i].Show(self.textCtrl_Radius[i])
        for i in range(self.NumCell,  self.maxNumCell):
            self.sizer_Cell[i].Hide(self.textCtrl_Material[i])
            self.sizer_Cell[i].Hide(self.textCtrl_Radius[i])
            self.textCtrl_Material[i].SetValue('')
            self.textCtrl_Radius[i].SetValue('')

        self.SetSize(self.GetBestSize())
        self.Layout()




class MaterialEdit(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, title='Material Edit', size=(730, 304), style=wx.DEFAULT_DIALOG_STYLE)
        #self.Create(parent, id, title, pos, size, style, name)

        self.MaxNumMaterials = max_Material
        self.NumMaterials = 0
        for j in range(len(Material)):
            if Material[j]['Name'] != '': self.NumMaterials += 1
        self.initMaxNucl = MaxNucl

        # READ Materials in TmpMaterials
        for i in range(len(Material)):
            mName = Material[i]['Name']
            TmpMaterial[i]['Name'] = mName
            mTmp = Material[i]['Tmp']
            TmpMaterial[i]['Tmp'] = mTmp
            mDen = Material[i]['Den']
            TmpMaterial[i]['Den'] = mDen
            mBurn = Material[i]['Burn']
            TmpMaterial[i]['Burn'] = mBurn
            mNNucl = Material[i]['NNucl']
            TmpMaterial[i]['NNucl'] = mNNucl

            for j in range(Material[i]['NNucl']):
                mInv = Material[i]['Inv'][j]
                TmpMaterial[i]['Inv'][j] = mInv
            for j in range(Material[i]['NNucl'], self.initMaxNucl):
                TmpMaterial[i]['Inv'][j] = ''

            for j in range(Material[i]['NNucl']):
                mVal = Material[i]['Val'][j]
                TmpMaterial[i]['Val'][j] = mVal
            for j in range(Material[i]['NNucl'], self.initMaxNucl):
                TmpMaterial[i]['Val'][j] = ''

        for i in range(len(Material), max_Material):
            TmpMaterial[i]['Name'] = ''
            TmpMaterial[i]['Tmp'] = ''
            TmpMaterial[i]['Den'] = ''
            TmpMaterial[i]['Burn'] = ''
            TmpMaterial[i]['Inv'] = ''
            TmpMaterial[i]['Val'] = ''


        MainSizer = wx.BoxSizer(wx.VERTICAL)
        GeneralMaterialSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Materials NAMEs sizer
        self.Staticbox_MAT_names = wx.StaticBox(self, -1, label="Materials")
        self.sizer_MAT_names = wx.StaticBoxSizer(self.Staticbox_MAT_names, wx.VERTICAL)
        sizer_NumMAT = wx.BoxSizer(wx.HORIZONTAL)


        Label_NumMat = wx.StaticText(self, -1, "Number of Materials:", (0, 0), (120, 20), wx.ALIGN_LEFT)
        self.SpinCtrl_NumMat = wx.SpinCtrl(self, -1, "", (0, 0), (50, 20), min=1, max=self.MaxNumMaterials, initial=self.NumMaterials)
        self.SpinCtrl_NumMat.Bind(wx.EVT_SPINCTRL, self.click_SpinCtrl_NumMat)

        sizer_NumMAT.Add(Label_NumMat, 0, wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 3)
        sizer_NumMAT.Add(self.SpinCtrl_NumMat, 0, wx.ALL | wx.EXPAND, 3)
        self.sizer_MAT_names.Add(sizer_NumMAT, 1, wx.ALL | wx.EXPAND, 0)

        self.RadioBtn_MAT_num = [0 for i in range(self.MaxNumMaterials)]
        self.TextCtrl_MAT_name = [0 for i in range(self.MaxNumMaterials)]
        self.sizer_MAT_name = [0 for i in range(self.MaxNumMaterials)]
        self.MATid = [0 for i in range(self.MaxNumMaterials)]

        for i in range(self.MaxNumMaterials):
            self.MATid[i] = wx.NewId()
            self.RadioBtn_MAT_num[i] = wx.RadioButton(self, self.MATid[i])
            self.RadioBtn_MAT_num[i].Bind(wx.EVT_RADIOBUTTON, self.onRadioBtnMAT_Cliked)
            self.TextCtrl_MAT_name[i] = wx.TextCtrl(self, self.MATid[i], Material[i]['Name'], (0, 0), (160, 20))
            self.TextCtrl_MAT_name[i].Bind(wx.EVT_TEXT, self.onKeyTyped_MAT_name)
            self.TextCtrl_MAT_name[i].Bind(wx.EVT_SET_FOCUS, self.onSetFocus_MAT_name)
            self.sizer_MAT_name[i] = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer_MAT_name[i].Add(self.RadioBtn_MAT_num[i], 0, wx.RIGHT | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 3)
            self.sizer_MAT_name[i].Add(self.TextCtrl_MAT_name[i], 0, wx.RIGHT | wx.LEFT | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 0)
            self.sizer_MAT_names.Add(self.sizer_MAT_name[i], 0, wx.ALL | wx.EXPAND, 2)
        # Hide extra MATs
        for i in range(self.SpinCtrl_NumMat.GetValue(), self.MaxNumMaterials):
            self.sizer_MAT_names.Hide(self.sizer_MAT_name[i])


        #Sizers MatOptions
        Staticbox_MAT_options = wx.StaticBox(self, -1, label="Options")
        AllOptionsSizer = wx.StaticBoxSizer(Staticbox_MAT_options, wx.HORIZONTAL)
        OptionsSizer = wx.GridBagSizer(hgap=4, vgap=2)
        NuclideGridSizer = wx.BoxSizer(wx.VERTICAL)

        # Materials Name
        Label_MaterialsName = wx.StaticText(self, -1, "Materials Name:", (0, 0), (130, 20), wx.ALIGN_LEFT)
        self.TextCtrl_MaterialName = wx.TextCtrl(self, -1, 'TEST', (0, 0), (100, 20), wx.TE_READONLY)

        # Materials Density
        Label_MaterialsDens = wx.StaticText(self, -1, "Materials Density:", (0, 0), (130, 20), wx.ALIGN_LEFT)
        self.TextCtrl_MaterialDens = wx.TextCtrl(self, -1, "", (0, 0), (100, 20))
        self.TextCtrl_MaterialDens.Bind(wx.EVT_TEXT, self.onKeyTyped_MAT_density)

        # Materials Temp
        Label_MaterialsTemp = wx.StaticText(self, -1, "Materials Temperature:", (0, 0), (130, 20), wx.ALIGN_LEFT)
        self.TextCtrl_MaterialTemp = wx.TextCtrl(self, -1, "", (0, 0), (100, 20))
        self.TextCtrl_MaterialTemp.Bind(wx.EVT_TEXT, self.onKeyTyped_MAT_temperature)

        # Max Num of Nuclides
        Label_Burnable = wx.StaticText(self, -1, "Burnable material:", (0, 0), (130, 20), wx.ALIGN_LEFT)
        self.CheckBox_Burnable = wx.CheckBox(self, -1)
        self.CheckBox_Burnable.Bind(wx.EVT_CHECKBOX, self.click_CheckBox_Burnable)
        #self.SpinCtrl_MaxNumNucl = wx.SpinCtrl(self, -1, "", (0, 0), (100, 20), min=1, max=self.MaxNumMaterials, initial=self.initMaxNucl)
        #self.SpinCtrl_MaxNumNucl.Bind(wx.EVT_SPINCTRL, self.click_SpinCtrl_MaxNumNucl)


        flagLabel = wx.TOP | wx.DOWN | wx.ALIGN_TOP
        flagCtrl = wx.TOP | wx.DOWN | wx.ALIGN_TOP
        bord = 1
        OptionsSizer.Add(Label_MaterialsName, pos=(0, 0), flag=flagLabel, border=bord)
        OptionsSizer.Add(Label_MaterialsDens, pos=(1, 0), flag=flagLabel, border=bord)
        OptionsSizer.Add(Label_MaterialsTemp, pos=(2, 0), flag=flagLabel, border=bord)
        OptionsSizer.Add(Label_Burnable,    pos=(3, 0), flag=flagLabel, border=bord)
        #OptionsSizer.Add(Label_MaxNumNucl, pos=(3, 0), flag=flagLabel, border=bord)
        OptionsSizer.Add(self.TextCtrl_MaterialName, pos=(0, 1), flag=flagCtrl, border=bord)
        OptionsSizer.Add(self.TextCtrl_MaterialDens, pos=(1, 1), flag=flagCtrl, border=bord)
        OptionsSizer.Add(self.TextCtrl_MaterialTemp, pos=(2, 1), flag=flagCtrl, border=bord)
        OptionsSizer.Add(self.CheckBox_Burnable, pos=(3, 1), flag=flagCtrl, border=bord)
        #OptionsSizer.Add(self.SpinCtrl_MaxNumNucl,   pos=(3, 1), flag=flagCtrl, border=bord)

        # Nuclides Grid
        self.grid = wx.grid.Grid(self, -1, size=(242, 250))
        self.grid.CreateGrid(self.initMaxNucl, 2)
        self.grid.SetColSize(0, 100)
        self.grid.SetColSize(1, 100)
        self.grid.SetColLabelSize(22)
        self.grid.SetColLabelValue(0, "Nuclide")
        self.grid.SetColLabelValue(1, "Value")
        self.grid.SetRowLabelSize(25)
        self.grid.DisableDragGridSize()
        self.grid.DisableDragColSize()
        self.grid.DisableDragRowSize()
        NuclideGridSizer.Add(self.grid, 0, wx.ALL, 0)
        self.grid.SetScrollLineX(0)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.onGrid_Cell_Changed)
        self.grid.Bind(wx.EVT_KEY_DOWN, self.OnKey_Grid)



        AllOptionsSizer.Add(OptionsSizer, 0, wx.ALL, 5)               #AllOptionsSizer
        AllOptionsSizer.Add(NuclideGridSizer, 1, wx.ALL | wx.EXPAND, 5)

        GeneralMaterialSizer.Add(self.sizer_MAT_names, 0, wx.ALL, 5)     #MaterialSizer
        GeneralMaterialSizer.Add(AllOptionsSizer, 0, wx.ALL, 5)

        #Button OK Cancel
        BtnSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)

        MainSizer.Add(GeneralMaterialSizer, 0, wx.ALL | wx.EXPAND, 5)
        MainSizer.Add(BtnSizer, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        self.SetSizer(MainSizer)

        self.SetSize(self.GetBestSize())

        # Read STD or SAVEd Materials
        self.read_std_Materials()

        self.RadioBtn_MAT_num[0].SetValue(True)
        self.CurrentMat = 0
        self.openMaterialsOptions(0)


    def read_std_Materials(self):
        for i in range(self.NumMaterials):
            self.TextCtrl_MAT_name[i].SetValue(Material[i]['Name'])

#    def read_std_MaterialOptions(self):
#        for i in range(self.NumMaterials):
#            self.TextCtrl_MAT_name[i].SetText(Material[i]['Name'])


    def click_SpinCtrl_NumMat(self, event):
        self.NumMaterials = self.SpinCtrl_NumMat.GetValue()
        for i in range(self.NumMaterials):
            self.sizer_MAT_name[i].Show(self.RadioBtn_MAT_num[i])
            self.sizer_MAT_name[i].Show(self.TextCtrl_MAT_name[i])
        for i in range(self.NumMaterials,  self.MaxNumMaterials):
            self.sizer_MAT_name[i].Hide(self.RadioBtn_MAT_num[i])
            self.sizer_MAT_name[i].Hide(self.TextCtrl_MAT_name[i])
            self.TextCtrl_MAT_name[i].SetValue('')
            if self.RadioBtn_MAT_num[i].GetValue():
                self.RadioBtn_MAT_num[0].SetValue(True)
        for i in range(self.MaxNumMaterials):
            if self.RadioBtn_MAT_num[i].GetValue():
                self.Selected_MAT = i

        self.SetSize(self.GetBestSize())
        self.Layout()


    def onSetFocus_MAT_name(self, event):
        self.CurrentMat = self.MATid.index(event.GetId())
        self.RadioBtn_MAT_num[self.CurrentMat].SetValue(True)
        event.Skip()
        self.openMaterialsOptions(self.CurrentMat)


    def onRadioBtnMAT_Cliked(self, event):
        self.CurrentMat = self.MATid.index(event.GetId())
        self.openMaterialsOptions(self.CurrentMat)

        #for j in range(self.SpinCtrl_NumMat.GetValue()):
            #if self.RadioBtn_MAT_num[j].GetValue() == True:  i = j

    def openMaterialsOptions(self, id):
        i = id
        if TmpMaterial[i]['Name'] == '':
            self.TextCtrl_MaterialName.SetValue('')
            self.TextCtrl_MaterialDens.SetValue('')
            self.TextCtrl_MaterialTemp.SetValue('')
            self.CheckBox_Burnable.SetValue(False)
            self.grid.ClearGrid()
        else:
            self.TextCtrl_MaterialName.SetValue(TmpMaterial[i]['Name'])
            self.TextCtrl_MaterialDens.SetValue(TmpMaterial[i]['Den'])
            self.TextCtrl_MaterialTemp.SetValue(TmpMaterial[i]['Tmp'])
            self.CheckBox_Burnable.SetValue(TmpMaterial[i]['Burn'])
            self.grid.ClearGrid()
            for j in range(len(TmpMaterial[i]['Inv'])):
                self.grid.SetCellValue(j, 0, TmpMaterial[i]['Inv'][j])
                self.grid.SetCellValue(j, 1, TmpMaterial[i]['Val'][j])


    def onKeyTyped_MAT_name(self, event):
        i = self.MATid.index(event.GetId())
        TmpMaterial[i]['Name'] = self.TextCtrl_MAT_name[i].GetValue()
        self.TextCtrl_MaterialName.SetValue(TmpMaterial[i]['Name'])


    def onKeyTyped_MAT_density(self, event):
        for j in range(self.SpinCtrl_NumMat.GetValue()):
            if self.RadioBtn_MAT_num[j].GetValue() == True:
                i = j
                TmpMaterial[i]['Den'] = self.TextCtrl_MaterialDens.GetValue()

    def onKeyTyped_MAT_temperature(self, event):
        for j in range(self.SpinCtrl_NumMat.GetValue()):
            if self.RadioBtn_MAT_num[j].GetValue() == True:
                i = j
                TmpMaterial[i]['Tmp'] = self.TextCtrl_MaterialTemp.GetValue()

    def click_CheckBox_Burnable(self, event):
        for j in range(self.SpinCtrl_NumMat.GetValue()):
            if self.RadioBtn_MAT_num[j].GetValue() == True:
                i = j
                TmpMaterial[i]['Burn'] = self.CheckBox_Burnable.GetValue()

    def onGrid_Cell_Changed(self, event):
        row = event.GetRow()
        col = event.GetCol()
        text = self.grid.GetCellValue(row, col)

        for i in range(self.initMaxNucl):
            if self.grid.GetCellValue(i, 0) != '':
                NNucl = i
        NNucl += 1


        #for j in range(self.SpinCtrl_NumMat.GetValue()):
            #if self.RadioBtn_MAT_num[j].GetValue() == True:
                #i = j
        if col == 0:
            TmpMaterial[self.CurrentMat]['Inv'][row] = text
        else:
            TmpMaterial[self.CurrentMat]['Val'][row] = text
        TmpMaterial[self.CurrentMat]['NNucl'] = NNucl

    def OnKey_Grid(self, event):

        print('hi')

        # Get start cell and number of copy rows/cols
        if self.grid.IsSelection():
            self.rowstart = self.grid.GetSelectionBlockTopLeft()[0][0]
            self.colstart = self.grid.GetSelectionBlockTopLeft()[0][1]
            self.rowend = self.grid.GetSelectionBlockBottomRight()[0][0]
            self.colend = self.grid.GetSelectionBlockBottomRight()[0][1]
        else:
            self.rowstart = self.grid.GetGridCursorRow()
            self.colstart = self.grid.GetGridCursorCol()
            self.rowend = self.rowstart
            self.colend = self.colstart
        self.rows = self.rowend - self.rowstart + 1
        self.cols = self.colend - self.colstart + 1

        # If Ctrl+c is pressed...
        if event.ControlDown() and event.GetKeyCode() == 67:
            self.copy()
        # If Ctrl+v is pressed...
        if event.ControlDown() and event.GetKeyCode() == 86:
            self.paste()
        # If del, backspace or Ctrl+x is pressed...
        if event.GetKeyCode() == 127 or event.GetKeyCode() == 8:
            self.delete()
        # Skip other Key events
        if event.GetKeyCode():
            event.Skip()
            #return

        # SAVE All Nuclides like in onGrid_Cell_Changing ut ALL reSave
        for j in range(self.SpinCtrl_NumMat.GetValue()):
            if self.RadioBtn_MAT_num[j].GetValue() == True:
                nMat = j

        for i in range(self.initMaxNucl):
            TmpMaterial[nMat]['Inv'][i] = self.grid.GetCellValue(i, 0)
            TmpMaterial[nMat]['Val'][i] = self.grid.GetCellValue(i, 1)
            if self.grid.GetCellValue(i, 0) != '':
                NNucl = i
        NNucl += 1
        TmpMaterial[self.CurrentMat]['NNucl'] = NNucl


    def copy(self):
        data = ''

        # For each cell in selected range append the cell value
        # in the data variable Tabs '\t' for cols and '\n' for rows
        for r in range(self.rows):
            for c in range(self.cols):
                data += str(self.grid.GetCellValue(self.rowstart + r, self.colstart + c))
                if c < self.cols - 1:
                    data += '\t'
            data += '\n'

        # Create text data object
        clipboard = wx.TextDataObject()

        # Set data object value
        clipboard.SetText(data)

        # Put the data in the clipboard
        wx.TheClipboard.Open()
        wx.TheClipboard.SetData(clipboard)
        wx.TheClipboard.Close()

    def paste(self):
        clipboard = wx.TextDataObject()
        wx.TheClipboard.Open()
        wx.TheClipboard.GetData(clipboard)
        wx.TheClipboard.Close()
        data = clipboard.GetText()

        for y, string in enumerate(data.splitlines()):
            for x, word in enumerate(string.split('\t')):
                if(self.rowstart+y <= 30 and self.colstart+x <= 1):
                    self.grid.SetCellValue(self.rowstart+y, self.colstart+x, word)

    def delete(self):
        # Clear cells contents
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid.SetCellValue(self.rowstart + r, self.colstart + c, '')


class AZonePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        w = 1000
        h = 940
        self.IS_Symmetry = True

        # Add the Canvas
        self.Canvas = FloatCanvas.FloatCanvas(self,-1,(w, h), ProjectionFun = None, Debug = 0, BackgroundColor = 'WHITE')

    def SaveInfoTVS(self, NumTVS, TVS_type):
        self.NumTVS = NumTVS
        self.TVS_type = TVS_type

    def InfoNumTVS(self):
        return self.NumTVS

    def InfoTVStype(self):
        return self.TVS_type

    def SymmetrySave(self, do):
        self.IS_Symmetry = do


    def Zoom(self, do):
        MainTVSs = ((8, 8), (8, 9), (8, 10), (8, 11), (8, 12), (8, 13), (8, 14), (9, 9), (9, 10), (9, 11), (9, 12), (9, 13),
                         (9, 14), (10, 9), (10, 10), (10, 11), (10, 12), (10, 13), (11, 9), (11, 10), (11, 11), (11, 12), (12, 9),
                         (12, 10), (12, 11), (13, 9), (13, 10), (14, 9))
        for row in range(AZ_dimension):
            for col in range(AZ_dimension):
                if do == 'zoomIn':
                    All_index = (row, col)
                    if All_index not in MainTVSs:
                        self.Hex[row][col].Hide()
                        if self.HexTextYear[row][col]: self.HexTextYear[row][col].SetColor('WHITE')
                        if self.HexTextType[row][col]: self.HexTextType[row][col].SetColor('WHITE')
                elif do == 'zoomOut':
                    if map_year[row][col] != '-':
                        self.Hex[row][col].Show()
                        if self.HexTextYear[row][col]: self.HexTextYear[row][col].SetColor('BLACK')
                        if self.HexTextType[row][col]: self.HexTextType[row][col].SetColor('BLACK')

        TVS = TVSsize()
        Csym = int(AZ_dimension / 2)
        if do == 'zoomIn':
            self.Canvas.Zoom(1.8, (TVS.r*2*Csym+TVS.r*Csym+TVS.r*6.5, TVS.R*Csym*3/2+TVS.R*4.5))
        elif do == 'zoomOut':
            self.Canvas.Zoom(1/1.8, (TVS.r * 2 * Csym + TVS.r * Csym, TVS.R * Csym * 3 / 2))

    def DrawMap(self):
        TVS = TVSsize()
        r = TVS.r
        R = TVS.R
        color_year = TVS.color_year
        dx = 0
        dy = 0
        self.Hex = [[0 for i in range(AZ_dimension)] for j in range(AZ_dimension)]
        self.HexTextYear = [['' for i in range(AZ_dimension)] for j in range(AZ_dimension)]
        self.HexTextType = [['' for i in range(AZ_dimension)] for j in range(AZ_dimension)]

        dRow = 0
        for row in map_year:
            dCol = 0
            for col in row:
                # Draw TVS
                Points = [(dx + r, dy + R / 2), (dx + r, dy - R / 2),
                          (dx + 0, dy - R), (dx - r, dy - R / 2),
                          (dx - r, dy + R / 2), (dx + 0, dy + R)]
                if col == '1':
                    self.Hex[dRow][dCol] = self.Canvas.AddPolygon(Points, LineColor='NAVI', FillColor=color_year[0])
                    self.Hex[dRow][dCol].Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.onClick_Lbtn)
                    self.Hex[dRow][dCol].Bind(FloatCanvas.EVT_FC_RIGHT_DOWN, self.onClick_Rbtn)
                    self.Hex[dRow][dCol].Index = (dRow, dCol)
                    self.HexTextYear[dRow][dCol] = self.Canvas.AddText('1', (dx-r*4/5, dy+R/8), Size = 10, Color = 'BLACK',
                                                                       Family = wx.FONTFAMILY_MODERN, Weight = wx.FONTWEIGHT_NORMAL, Position='bl')
                elif col == '2':
                    self.Hex[dRow][dCol] = self.Canvas.AddPolygon(Points, LineColor='NAVI', FillColor=color_year[1])
                    self.Hex[dRow][dCol].Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.onClick_Lbtn)
                    self.Hex[dRow][dCol].Bind(FloatCanvas.EVT_FC_RIGHT_DOWN, self.onClick_Rbtn)
                    self.Hex[dRow][dCol].Index = (dRow, dCol)
                    self.HexTextYear[dRow][dCol] = self.Canvas.AddText('2', (dx-r*4/5, dy+R/8), Size = 10, Color = 'BLACK',
                                                                       Family = wx.FONTFAMILY_MODERN, Weight = wx.FONTWEIGHT_NORMAL, Position='bl')
                elif col == '3':
                    self.Hex[dRow][dCol] = self.Canvas.AddPolygon(Points, LineColor='NAVI', FillColor=color_year[2])
                    self.Hex[dRow][dCol].Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.onClick_Lbtn)
                    self.Hex[dRow][dCol].Bind(FloatCanvas.EVT_FC_RIGHT_DOWN, self.onClick_Rbtn)
                    self.Hex[dRow][dCol].Index = (dRow, dCol)
                    self.HexTextYear[dRow][dCol] = self.Canvas.AddText('3', (dx-r*4/5, dy+R/8), Size = 10, Color = 'BLACK',
                                                                       Family = wx.FONTFAMILY_MODERN, Weight = wx.FONTWEIGHT_NORMAL, Position='bl')
                else:
                    self.Hex[dRow][dCol] = self.Canvas.AddPolygon(Points, LineColor='WHITE', FillColor='WHITE')
                    self.Hex[dRow][dCol].Hide()
                dx += 2 * r
                dCol += 1
            dRow += 1
            dy += R * 2 - R / 2
            dx = r * dRow

        TVS_type = self.InfoTVStype()
        dx = 0
        dy = 0
        dRow = 0
        for row in map_type:
            dCol = 0
            for col in row:
                # Draw TVS
                Points = [(dx + r, dy + R / 2), (dx + r, dy - R / 2),
                          (dx + 0, dy - R), (dx - r, dy - R / 2),
                          (dx - r, dy + R / 2), (dx + 0, dy + R)]
                if col == '1':
                    self.HexTextType[dRow][dCol] = self.Canvas.AddText(str(TVS_type[0]), (dx, dy-R/9), Size = 9, Color = 'BLACK',
                                                                       Family = wx.FONTFAMILY_SWISS, Weight = wx.FONTWEIGHT_BOLD, Position='cc')
                elif col == '2':
                    self.HexTextType[dRow][dCol] = self.Canvas.AddText(str(TVS_type[1]), (dx, dy), Size = 10, Color = 'BLACK',
                                                                       Family = wx.FONTFAMILY_SWISS, Weight = wx.FONTWEIGHT_BOLD, Position='cc')
                elif col == '3':
                    self.HexTextType[dRow][dCol] = self.Canvas.AddText(str(TVS_type[2]), (dx, dy), Size = 10, Color = 'BLACK',
                                                                       Family = wx.FONTFAMILY_SWISS, Weight = wx.FONTWEIGHT_BOLD, Position='cc')
                elif col == '4':
                    self.HexTextType[dRow][dCol] = self.Canvas.AddText(str(TVS_type[3]), (dx, dy), Size = 10, Color = 'BLACK',
                                                                       Family = wx.FONTFAMILY_SWISS, Weight = wx.FONTWEIGHT_BOLD, Position='cc')
                elif col == '5':
                    self.HexTextType[dRow][dCol] = self.Canvas.AddText(str(TVS_type[4]), (dx, dy), Size = 10, Color = 'BLACK',
                                                                       Family = wx.FONTFAMILY_SWISS, Weight = wx.FONTWEIGHT_BOLD, Position='cc')
                dx += 2 * r
                dCol += 1
            dRow += 1
            dy += R * 2 - R / 2
            dx = r * dRow

        # Zoom
        Csym = int(AZ_dimension / 2)
        self.Canvas.Zoom(1, (r*2*Csym+r*Csym, R*Csym*3/2))


    def onClick_Lbtn(self, Hex):
        self.fTVS_change(Hex.Index, 'left')
        print(Hex.Index)

    def onClick_Rbtn(self, Hex):
        self.fTVS_change(Hex.Index, 'right')

    def fTVS_symetry(self):
        Cn = int(AZ_dimension/2)
        Sym = [0 for i in range(29)]
        k=0
        Sym[0] = [[Cn, Cn]]
        for j in range(Cn-1):
            for i in range(1, Cn-j):
                k+=1
                Sym[k] = [[Cn+j, Cn-j-i], [Cn-j, Cn+j+i], [Cn-i, Cn-j], [Cn+i, Cn+j],  [Cn-j-i, Cn+i], [Cn+j+i, Cn-i]]
        return Sym

    def fTVS_change(self, Index, button):
        dRow = Index[0]
        dCol = Index[1]
        TVS_index = [dRow, dCol]

        TVS = TVSsize()
        color_year = TVS.color_year

        NumTVS = self.InfoNumTVS()
        TVS_type = self.InfoTVStype()

        if self.IS_Symmetry:
            Sym = self.fTVS_symetry()    # call fTVS_symetry function
            for i in range(len(Sym)):  # walk by all Sym koeff list
                if TVS_index in Sym[i]:  # looking up Symetry
                    for SymIndex in Sym[i]:  # get indexes of all symetry TVS from list
                        dRow = SymIndex[0]
                        dCol = SymIndex[1]
                        self.ModifyMapYear(button, dRow, dCol, color_year)
                        self.ModifyMapType(button, dRow, dCol, NumTVS, TVS_type)
        else:
            self.ModifyMapYear(button, dRow, dCol, color_year)
            self.ModifyMapType(button, dRow, dCol, NumTVS, TVS_type)

        self.Canvas.Draw(True)


    def ModifyMapYear(self, button, dRow, dCol, color_year):
        # Modification MAP_YEAR
        if button == 'left':
            if map_year[dRow][dCol] == '1':
                Year = self.StdTVS_year(dRow, dCol, color_year, color = 1, Year = 2)
            elif map_year[dRow][dCol] == '2':
                Year = self.StdTVS_year(dRow, dCol, color_year, color=2, Year=3)
            elif map_year[dRow][dCol] == '3':
                Year = self.StdTVS_year(dRow, dCol, color_year, color=0, Year=1)
            map_year[dRow] = map_year[dRow][:dCol] + str(Year) + map_year[dRow][(dCol + 1):]

    def StdTVS_year(self, dRow, dCol, color_year, color, Year):
        self.HexTextYear[dRow][dCol].SetText(str(Year))
        self.Hex[dRow][dCol].SetFillColor(color_year[color])
        return Year

    def ModifyMapType(self, button, dRow, dCol, NumTVS, TVS_type):
        # Modification MAP_TYPE
        if button == 'right':
            if map_type[dRow][dCol] == '1':
                if NumTVS > 1:
                    Type = self.StdTVS_type(dRow, dCol,  TVS_type, N_type=1, Type=2)
                else:
                    Type = self.StdTVS_type(dRow, dCol, TVS_type)
            elif map_type[dRow][dCol] == '2':
                if NumTVS > 2:
                    Type = self.StdTVS_type(dRow, dCol,  TVS_type, N_type=2, Type=3)
                else:
                    Type = self.StdTVS_type(dRow, dCol, TVS_type)
            elif map_type[dRow][dCol] == '3':
                if NumTVS > 3:
                    Type = self.StdTVS_type(dRow, dCol,  TVS_type, N_type=3, Type=4)
                else:
                    Type = self.StdTVS_type(dRow, dCol, TVS_type)
            elif map_type[dRow][dCol] == '4':
                if NumTVS > 4:
                    Type = self.StdTVS_type(dRow, dCol,  TVS_type, N_type=3, Type=4)
                else:
                    Type = self.StdTVS_type(dRow, dCol, TVS_type)
            elif map_type[dRow][dCol] == '5':
                Type = self.StdTVS_type(dRow, dCol, TVS_type)
            map_type[dRow] = map_type[dRow][:dCol] + str(Type) + map_type[dRow][(dCol + 1):]

    def StdTVS_type(self, dRow, dCol, TVS_type, N_type = 0, Type = 1):
        self.HexTextType[dRow][dCol].SetText(TVS_type[N_type])
        return Type


    def modifyTVSname(self):
        TVS_type = self.InfoTVStype()
        dRow = 0
        for row in map_type:
            dCol = 0
            for col in row:
                # Draw TVS
                if col == '1':
                    self.HexTextType[dRow][dCol].SetText(TVS_type[0])
                elif col == '2':
                    self.HexTextType[dRow][dCol].SetText(TVS_type[1])
                elif col == '3':
                    self.HexTextType[dRow][dCol].SetText(TVS_type[2])
                elif col == '4':
                    self.HexTextType[dRow][dCol].SetText(TVS_type[3])
                elif col == '5':
                    self.HexTextType[dRow][dCol].SetText(TVS_type[4])
                dCol += 1
            dRow += 1

        self.Canvas.Draw(True)


class TVSPanel(wx.Panel):
    def __init__(self, parent, InTVS):
        wx.Panel.__init__(self, parent)
        self.InTVS = InTVS
        w = 1000
        h = 940
        self.IS_Symmetry = True

        # Add the Canvas
        self.Canvas = FloatCanvas.FloatCanvas(self,-1,(w, h), ProjectionFun = None, Debug = 0, BackgroundColor = 'WHITE')

    def SaveInfoPIN(self, NumPIN, Selected_PIN, PIN_type):
        self.NumPIN = NumPIN
        self.PIN_type = PIN_type
        self.Selected_PIN = Selected_PIN

    def InfoNumPIN(self):
        return self.NumPIN

    def InfoPINtype(self):
        return self.PIN_type

    def SymmetrySave(self, do):
        self.IS_Symmetry = do

    def Zoom(self, do):
        count = 0
        MainPINs = [[11,11]]
        for i in range(int(TVS_dimension / 2), TVS_dimension):
            for j in range(int(TVS_dimension / 2)+1, TVS_dimension - count):
                MainPINs.append([i, j])
            count += 1

        for row in range(TVS_dimension):
            for col in range(TVS_dimension):
                if do == 'zoomIn':
                    All_index = [row, col]
                    if All_index not in MainPINs:
                        self.Hex[row][col].Hide()
                        if self.HexTextType[row][col]: self.HexTextType[row][col].SetColor('WHITE')
                elif do == 'zoomOut':
                    if map_PIN_type[self.InTVS][row][col] != '-':
                        self.Hex[row][col].Show()
                        if self.HexTextType[row][col]: self.HexTextType[row][col].SetColor('BLACK')

        PIN = PINsize()
        Csym = int(TVS_dimension / 2)
        if do == 'zoomIn':
            self.Canvas.Zoom(1.8, (PIN.r*2*Csym+PIN.r*Csym+PIN.r*10, PIN.R*Csym*3/2+PIN.R*7))
        elif do == 'zoomOut':
            self.Canvas.Zoom(1/1.8, (PIN.r * 2 * Csym + PIN.r * Csym, PIN.R * Csym * 3 / 2))


    def DrawMap(self):
        PIN = PINsize()
        r = PIN.r
        R = PIN.R
        color_type = PIN.color_type
        dx = 0
        dy = 0
        self.Hex = [[0 for i in range(TVS_dimension)] for j in range(TVS_dimension)]
        self.HexTextYear = [['' for i in range(TVS_dimension)] for j in range(TVS_dimension)]
        self.HexTextType = [['' for i in range(TVS_dimension)] for j in range(TVS_dimension)]

        dRow = 0
        for row in map_PIN_type[self.InTVS]:
            dCol = 0
            for col in row:
                # Draw PINs
                Points = [(dx + r, dy + R / 2), (dx + r, dy - R / 2),
                          (dx + 0, dy - R), (dx - r, dy - R / 2),
                          (dx - r, dy + R / 2), (dx + 0, dy + R)]

                if col == '1':
                    self.Hex[dRow][dCol] = self.Canvas.AddPolygon(Points, LineColor='NAVI', FillColor=color_type[0])
                    self.Hex[dRow][dCol].Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.onClick_Lbtn)
                    self.Hex[dRow][dCol].Index = (dRow, dCol)
                    self.HexTextType[dRow][dCol] = self.Canvas.AddText('1', (dx-r*4/5, dy+R/8), Size = 10, Color = 'BLACK',
                                                                       Family = wx.FONTFAMILY_MODERN, Weight = wx.FONTWEIGHT_NORMAL, Position='bl')
                elif col == '2':
                    self.Hex[dRow][dCol] = self.Canvas.AddPolygon(Points, LineColor='NAVI', FillColor=color_type[1])
                    self.Hex[dRow][dCol].Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.onClick_Lbtn)
                    self.Hex[dRow][dCol].Index = (dRow, dCol)
                    self.HexTextType[dRow][dCol] = self.Canvas.AddText('2', (dx-r*4/5, dy+R/8), Size = 10, Color = 'BLACK',
                                                                       Family = wx.FONTFAMILY_MODERN, Weight = wx.FONTWEIGHT_NORMAL, Position='bl')
                elif col == '3':
                    self.Hex[dRow][dCol] = self.Canvas.AddPolygon(Points, LineColor='NAVI', FillColor=color_type[2])
                    self.Hex[dRow][dCol].Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.onClick_Lbtn)
                    self.Hex[dRow][dCol].Index = (dRow, dCol)
                    self.HexTextType[dRow][dCol] = self.Canvas.AddText('3', (dx-r*4/5, dy+R/8), Size = 10, Color = 'BLACK',
                                                                       Family = wx.FONTFAMILY_MODERN, Weight = wx.FONTWEIGHT_NORMAL, Position='bl')
                elif col == '4':
                    self.Hex[dRow][dCol] = self.Canvas.AddPolygon(Points, LineColor='NAVI', FillColor=color_type[3])
                    self.Hex[dRow][dCol].Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.onClick_Lbtn)
                    self.Hex[dRow][dCol].Index = (dRow, dCol)
                    self.HexTextType[dRow][dCol] = self.Canvas.AddText('3', (dx-r*4/5, dy+R/8), Size = 10, Color = 'BLACK',
                                                                       Family = wx.FONTFAMILY_MODERN, Weight = wx.FONTWEIGHT_NORMAL, Position='bl')
                elif col == '5':
                    self.Hex[dRow][dCol] = self.Canvas.AddPolygon(Points, LineColor='NAVI', FillColor=color_type[4])
                    self.Hex[dRow][dCol].Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.onClick_Lbtn)
                    self.Hex[dRow][dCol].Index = (dRow, dCol)
                    self.HexTextType[dRow][dCol] = self.Canvas.AddText('3', (dx-r*4/5, dy+R/8), Size = 10, Color = 'BLACK',
                                                                       Family = wx.FONTFAMILY_MODERN, Weight = wx.FONTWEIGHT_NORMAL, Position='bl')
                elif col == '6':
                    self.Hex[dRow][dCol] = self.Canvas.AddPolygon(Points, LineColor='NAVI', FillColor=color_type[5])
                    self.Hex[dRow][dCol].Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.onClick_Lbtn)
                    self.Hex[dRow][dCol].Index = (dRow, dCol)
                    self.HexTextType[dRow][dCol] = self.Canvas.AddText('3', (dx-r*4/5, dy+R/8), Size = 10, Color = 'BLACK',
                                                                       Family = wx.FONTFAMILY_MODERN, Weight = wx.FONTWEIGHT_NORMAL, Position='bl')
                elif col == '7':
                    self.Hex[dRow][dCol] = self.Canvas.AddPolygon(Points, LineColor='NAVI', FillColor=color_type[6])
                    self.Hex[dRow][dCol].Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.onClick_Lbtn)
                    self.Hex[dRow][dCol].Index = (dRow, dCol)
                    self.HexTextType[dRow][dCol] = self.Canvas.AddText('3', (dx-r*4/5, dy+R/8), Size = 10, Color = 'BLACK',
                                                                       Family = wx.FONTFAMILY_MODERN, Weight = wx.FONTWEIGHT_NORMAL, Position='bl')
                elif col == '8':
                    self.Hex[dRow][dCol] = self.Canvas.AddPolygon(Points, LineColor='NAVI', FillColor=color_type[7])
                    self.Hex[dRow][dCol].Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.onClick_Lbtn)
                    self.Hex[dRow][dCol].Index = (dRow, dCol)
                    self.HexTextType[dRow][dCol] = self.Canvas.AddText('3', (dx-r*4/5, dy+R/8), Size = 10, Color = 'BLACK',
                                                                       Family = wx.FONTFAMILY_MODERN, Weight = wx.FONTWEIGHT_NORMAL, Position='bl')
                elif col == '9':
                    self.Hex[dRow][dCol] = self.Canvas.AddPolygon(Points, LineColor='NAVI', FillColor= 'WHITE')

                else:
                    self.Hex[dRow][dCol] = self.Canvas.AddPolygon(Points, LineColor='WHITE', FillColor='WHITE')
                    self.Hex[dRow][dCol].Hide()
                dx += 2 * r
                dCol += 1
            dRow += 1
            dy += R * 2 - R / 2
            dx = r * dRow

        # Zoom
        Csym = int(TVS_dimension / 2)
        self.Canvas.Zoom(1, (r*2*Csym+r*Csym, R*Csym*3/2))

    def onClick_Lbtn(self, Hex):
        self.fPIN_change(Hex.Index, 'left')
        print(Hex.Index)

    def fPIN_symetry(self):
        Cn = int(TVS_dimension/2)
        Sym = [0 for i in range(56)]
        k=0
        Sym[0] = [[Cn, Cn]]
        for j in range(Cn-1):
            for i in range(1, Cn-j):
                k+=1
                Sym[k] = [[Cn+j, Cn-j-i], [Cn-j, Cn+j+i], [Cn-i, Cn-j], [Cn+i, Cn+j],  [Cn-j-i, Cn+i], [Cn+j+i, Cn-i]]
        return Sym

    def fPIN_change(self, Index, button):
        dRow = Index[0]
        dCol = Index[1]
        PIN_index = [dRow, dCol]

        PIN = PINsize()
        color_type = PIN.color_type

        NumPIN = self.InfoNumPIN()
        PIN_type = self.InfoPINtype()

        if self.IS_Symmetry:
            Sym = self.fPIN_symetry()    # call fTVS_symetry function
            for i in range(len(Sym)):  # walk by all Sym koeff list
                if PIN_index in Sym[i]:  # looking up Symetry
                    for SymIndex in Sym[i]:  # get indexes of all symetry TVS from list
                        dRow = SymIndex[0]
                        dCol = SymIndex[1]
                        self.ModifyMapType(button, dRow, dCol, color_type, NumPIN)
        else:
            self.ModifyMapType(button, dRow, dCol, color_type, NumPIN)

        self.Canvas.Draw(True)


    def ModifyMapType(self, button, dRow, dCol, color_type, NumPIN):
        # Modification MAP_TYPE
        if button == 'left':
            Type = self.Selected_PIN+1
            color = self.Selected_PIN
            self.HexTextType[dRow][dCol].SetText(str(Type))
            self.Hex[dRow][dCol].SetFillColor(color_type[color])

            map_PIN_type[self.InTVS][dRow] = map_PIN_type[self.InTVS][dRow][:dCol] + str(Type) + map_PIN_type[self.InTVS][dRow][(dCol + 1):]


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, 'Active Zone VVER maker', size=(1250, 1015))
        self.CenterOnScreen()

        self.NumTVS = init_NumTVS     # initial (default) value number of TVSs = 3
        self.TVS_type = ['XXXXXX' for i in range(max_NumTVS)]
        self.TVS_type[0] = 'E495A18'
        self.TVS_type[1] = 'E460A06'
        self.TVS_type[2] = 'E445A22'

        self.NumPIN = init_NumPIN     # initial (default) value number of PINs = 5
        self.Selected_PIN = 0
        self.PIN_type = ['xxxxxx' for i in range(max_NumPIN)]
        self.PIN_type[0] = 'U49P50'
        self.PIN_type[1] = 'U44P50'
        self.PIN_type[2] = 'U40P50'

        self.mainControlPanel = ControlPanel(self)
        self.ColorPanel = wx.Panel(self)

        self.mainMapsBook = wx.Notebook(self.ColorPanel, -1, size=(1030, 1010))

        self.sizerColorPanel = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerColorPanel.Add(self.mainMapsBook, 1, wx.ALL | wx.EXPAND, 5)
        self.ColorPanel.SetSizer(self.sizerColorPanel)

        self.mainAZonePanel = AZonePanel(self.mainMapsBook)

        self.mainTVSPanel = [0 for i in range(max_NumTVS)]
        for i in range(max_NumTVS):
            self.mainTVSPanel[i] = TVSPanel(self.mainMapsBook, i)
            self.mainTVSPanel[i].Hide()


        self.mainMapsBook.AddPage(self.mainAZonePanel, "Active ZONE map")
        self.mainMapsBook_NumPage = 0

        self.sizerFrame = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerFrame.Add(self.mainControlPanel, 0, wx.EXPAND)
        self.sizerFrame.Add(self.ColorPanel, 1, wx.EXPAND)
        self.SetSizer(self.sizerFrame)


        self.NumTVS = init_NumTVS
        self.mainAZonePanel.SaveInfoTVS(self.NumTVS, self.TVS_type)
        self.mainAZonePanel.DrawMap()

        for i in range(max_NumTVS):
            self.mainTVSPanel[i].SaveInfoPIN(self.NumPIN, self.Selected_PIN, self.PIN_type)
            self.mainTVSPanel[i].DrawMap()



        self.updateMapsBook()

        # Listen change in num TVS
        pub.subscribe(self.listenerCPanelSymmetry, 'CPanel Symmetry')
        pub.subscribe(self.listenerCPanelZoom, 'CPanel Zoom')
        pub.subscribe(self.listenerCPanelTVS, 'CPanel TVS')
        pub.subscribe(self.ListenerCPanelPIN, 'CPanel PIN')


    def updateMapsBook(self):
        # If Add TVS
        if self.NumTVS > self.mainMapsBook_NumPage:
            for i in range(self.mainMapsBook_NumPage, self.NumTVS, 1):
                self.mainMapsBook.AddPage(self.mainTVSPanel[i], self.TVS_type[i])
                self.mainMapsBook_NumPage += 1
        # If Remove TVS
        if self.NumTVS < self.mainMapsBook_NumPage:
            if self.mainMapsBook.GetSelection() == self.mainMapsBook_NumPage:
                self.mainMapsBook.ChangeSelection(self.mainMapsBook_NumPage-1)
            for i in range(self.mainMapsBook_NumPage, self.NumTVS, -1):
                self.mainMapsBook.RemovePage(i)
                self.mainMapsBook_NumPage -= 1

        for i in range(self.NumTVS):
            self.mainMapsBook.SetPageText(i+1, self.TVS_type[i])

        #self.mainMapsBook.ChangeSelection(0)
        #self.SetAutoLayout(True) # Auto Layout when window is resized
        self.Layout()


    def listenerCPanelSymmetry(self, arg1, arg2=None):
        IsSymmetry = arg1
        self.mainAZonePanel.SymmetrySave(IsSymmetry)
        for i in range(max_NumTVS):
            self.mainTVSPanel[i].SymmetrySave(IsSymmetry)

    def listenerCPanelZoom(self, arg1, arg2=None):
        IsZoom = arg1
        if IsZoom:
            self.mainAZonePanel.Zoom('zoomIn')
            for i in range(self.NumTVS): self.mainTVSPanel[i].Zoom('zoomIn')
        else:
            self.mainAZonePanel.Zoom('zoomOut')
            for i in range(self.NumTVS): self.mainTVSPanel[i].Zoom('zoomOut')

    def listenerCPanelTVS(self, arg1, arg2=None):
        self.NumTVS = arg1
        #print('NumTVS:', self.NumTVS)
        if arg2:
            self.TVS_type = arg2
            #for i in range(max_NumTVS):
                #print(self.TVS_type[i])
        self.updateMapsBook()

        self.mainAZonePanel.SaveInfoTVS(self.NumTVS, self.TVS_type)
        self.mainAZonePanel.modifyTVSname()

    def ListenerCPanelPIN(self, arg1, arg2=None):
        self.NumPIN = arg1
        if arg2:
            self.Selected_PIN = arg2[0]
            self.PIN_type = arg2[1]
            #for i in range(len(arg2[1])):
                #print(self.PIN_type[i])

        for i in range(max_NumTVS):
            self.mainTVSPanel[i].SaveInfoPIN(self.NumPIN, self.Selected_PIN, self.PIN_type)
            #self.mainTVSPanel[i].DrawMap()

        #self.mainAZonePanel.SaveInfoTVS(self.NumTVS, self.TVS_type)
        #self.mainAZonePanel.modifyTVSname()


if  __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    frame.Show()
app.MainLoop()