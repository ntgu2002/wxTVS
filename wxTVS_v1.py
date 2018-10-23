import wx
import os
import math

BASE  = 80.0    # sizes used in shapes drawn below
BASE2 = BASE/2
BASE4 = BASE/4

USE_BUFFER = ('wxMSW' in wx.PlatformInfo) # use buffered drawing on Windows

class clControlPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        btn = wx.Button(self, label="Control")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btn, 0, wx.ALL, 10)
        self.SetSizer(sizer)


class clAZonePanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.SetBackgroundColour("WHITE")

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        if USE_BUFFER:
            self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, evt):
        # When there is a size event then recreate the buffer to match
        # the new size of the window.
        self.InitBuffer()
        evt.Skip()


    def OnPaint(self, evt):
        if USE_BUFFER:
            # The buffer already contains our drawing, so no need to
            # do anything else but create the buffered DC.  When this
            # method exits and dc is collected then the buffer will be
            # blitted to the paint DC automagically
            dc = wx.BufferedPaintDC(self, self._buffer)
        else:
            # Otherwise we need to draw our content to the paint DC at
            # this time.
            dc = wx.PaintDC(self)
            gc = self.MakeGC(dc)
            self.Draw(gc)


    def InitBuffer(self):
        sz = self.GetClientSize()
        sz.width = max(1, sz.width)
        sz.height = max(1, sz.height)
        self._buffer = wx.Bitmap(sz.width, sz.height, 32)

        dc = wx.MemoryDC(self._buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        gc = self.MakeGC(dc)
        self.Draw(gc)


    def MakeGC(self, dc):
        try:
            if False:
                wxdir = os.path.dirname(wx.__file__) + os.pathsep
                if not wxdir in os.environ.get('PATH', ""):
                    os.environ['PATH'] = wxdir + os.environ.get('PATH', "")

                gcr = wx.GraphicsRenderer.GetCairoRenderer
                gc = gcr() and gcr().CreateContext(dc)

                if gc is None:
                    wx.MessageBox("Unable to create Cairo Context this way.", "Oops")
                    gc = wx.GraphicsContext.Create(dc)
            else:
                gc = wx.GraphicsContext.Create(dc)

        except NotImplementedError:
            dc.DrawText("This build of wxPython does not support the wx.GraphicsContext "
                        "family of classes.",
                        25, 25)
            return None
        return gc


    def Draw(self, gc):
        TVS_r = 32
        TVS_R = 2 * TVS_r / math.sqrt(3)
        dx = TVS_R
        dy = TVS_R

        points = [(dx + TVS_r, dy + TVS_R / 2), (dx + TVS_r, dy - TVS_R / 2), (dx + 0, dy - TVS_R),
                  (dx - TVS_r, dy - TVS_R / 2), (dx - TVS_r, dy + TVS_R / 2), (dx + 0, dy + TVS_R)]

        gc.SetPen(wx.Pen("navy", 1))
        gc.SetBrush(wx.Brush("pink"))
        path = gc.CreatePath()
        for i in range(6):
            path.AddLineToPoint(points[i])
        path.CloseSubpath()
        gc.DrawPath(path)


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