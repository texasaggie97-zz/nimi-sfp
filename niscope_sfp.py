import nimodinst
import niscope
import warnings
import wx

# begin wxGlade: extracode
import matplotlib
matplotlib.use("WxAgg")
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
# end wxGlade

USE_WIT = True

AppBaseClass = wx.App
if USE_WIT:
    from wx.lib.mixins.inspection import InspectableApp
    AppBaseClass = InspectableApp

vertical_couplings = {
    'AC': niscope.VerticalCoupling.AC,
    'DC': niscope.VerticalCoupling.DC,
    'Ground': niscope.VerticalCoupling.GND,
}


def get_vertical_coupling_enum(coupling_string):
    if coupling_string in vertical_couplings:
        return vertical_couplings[coupling_string]
    else:
        raise TypeError('Incorrect vertical coupling string: {0}'.format(coupling_string))  # noqa: E501


trigger_couplings = {
    'AC': niscope.TriggerCoupling.AC,
    'DC': niscope.TriggerCoupling.DC,
    'HF_REJECT': niscope.TriggerCoupling.HF_REJECT,
    'LF_REJECT': niscope.TriggerCoupling.LF_REJECT,
    'AC_PLUS_HF_REJECT': niscope.TriggerCoupling.AC_PLUS_HF_REJECT,
}


def get_trigger_coupling_enum(coupling_string):
    if coupling_string in trigger_couplings:
        return trigger_couplings[coupling_string]
    else:
        raise TypeError('Incorrect trigger coupling string: {0}'.format(coupling_string))  # noqa: E501


slopes = {
    'Positive': niscope.TriggerSlope.POSITIVE,
    'Negative': niscope.TriggerSlope.NEGATIVE,
}


def get_slope_enum(slope_string):
    if slope_string in slopes:
        return slopes[slope_string]
    else:
        raise TypeError('Incorrect slope string: {0}'.format(slope_string))


modes = {
    'Entering': niscope.TriggerWindowMode.ENTERING,
    'Leaving': niscope.TriggerWindowMode.LEAVING,
}


def get_mode_enum(mode_string):
    if mode_string in modes:
        return modes[mode_string]
    else:
        raise TypeError('Incorrect mode string: {0}'.format(mode_string))


class SFP(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: SFP.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((550, 800))
        self._devices = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)  # noqa: E501
        self._modinst_session = nimodinst.Session('niscope')
        for dev in self._modinst_session.devices:
            dev_name = dev.device_name
            self._devices.Append('{0}'.format(dev_name))
        self._min_sample_rate = wx.SpinCtrlDouble(self, wx.ID_ANY, "1000000.0", min=0.0, max=100000000.0)  # noqa: E501
        self._min_record_length = wx.SpinCtrl(self, wx.ID_ANY, "1000", min=0, max=100000000)  # noqa: E501
        self._channel_list = wx.TextCtrl(self, wx.ID_ANY, "0")
        self._vertical_range = wx.SpinCtrlDouble(self, wx.ID_ANY, "1.0", min=0.0, max=100.0)  # noqa: E501
        self._probe_attenuation = wx.SpinCtrlDouble(self, wx.ID_ANY, "1.0", min=0.0, max=100.0)  # noqa: E501
        self._vertical_offset = wx.SpinCtrlDouble(self, wx.ID_ANY, "0.0", min=0.0, max=100.0)  # noqa: E501
        self._vertical_coupling = wx.ComboBox(self, wx.ID_ANY, choices=["AC", "DC", "Ground"], style=wx.CB_DROPDOWN | wx.CB_READONLY)  # noqa: E501
        self._trigger_type = wx.Notebook(self, wx.ID_ANY)
        self._trigger_type_immediate = wx.Panel(self._trigger_type, wx.ID_ANY)
        self._trigger_type_edge = wx.Panel(self._trigger_type, wx.ID_ANY)
        self._trigger_source_edge = wx.TextCtrl(self._trigger_type_edge, wx.ID_ANY, "0")  # noqa: E501
        self._trigger_level_edge = wx.SpinCtrlDouble(self._trigger_type_edge, wx.ID_ANY, "0.0", min=0.0, max=30.0)  # noqa: E501
        self._trigger_slope_edge = wx.ComboBox(self._trigger_type_edge, wx.ID_ANY, choices=["Positive", "Negative"], style=wx.CB_DROPDOWN | wx.CB_READONLY)  # noqa: E501
        self._trigger_coupling_edge = wx.ComboBox(self._trigger_type_edge, wx.ID_ANY, choices=["AC", "DC", "HF_REJECT", "LF_REJECT", "AC_PLUS_HF_REJECT"], style=wx.CB_DROPDOWN | wx.CB_READONLY)  # noqa: E501
        self._trigger_type_digital = wx.Panel(self._trigger_type, wx.ID_ANY)
        self._trigger_source_digital = wx.TextCtrl(self._trigger_type_digital, wx.ID_ANY, "VAL_RTSI_0")  # noqa: E501
        self._trigger_slope_digital = wx.ComboBox(self._trigger_type_digital, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)  # noqa: E501
        self._trigger_type_window = wx.Panel(self._trigger_type, wx.ID_ANY)
        self._trigger_source_window = wx.TextCtrl(self._trigger_type_window, wx.ID_ANY, "0")  # noqa: E501
        self._mode_window = wx.ComboBox(self._trigger_type_window, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)  # noqa: E501
        self._low_level_window = wx.SpinCtrlDouble(self._trigger_type_window, wx.ID_ANY, "0.0", min=-30.0, max=30.0)  # noqa: E501
        self._high_level_window = wx.SpinCtrlDouble(self._trigger_type_window, wx.ID_ANY, "0.0", min=-30.0, max=30.0)  # noqa: E501
        self._trigger_coupling_window = wx.ComboBox(self._trigger_type_window, wx.ID_ANY, choices=["AC", "DC", "HF_REJECT", "LF_REJECT", "AC_PLUS_HF_REJECT"], style=wx.CB_DROPDOWN)  # noqa: E501
        self._trigger_type_hysteresis = wx.Panel(self._trigger_type, wx.ID_ANY)
        self._trigger_source_hysteresis = wx.TextCtrl(self._trigger_type_hysteresis, wx.ID_ANY, "0")  # noqa: E501
        self._trigger_level_hysteresis = wx.SpinCtrlDouble(self._trigger_type_hysteresis, wx.ID_ANY, "0.0", min=-30.0, max=30.0)  # noqa: E501
        self._hysteresis = wx.SpinCtrlDouble(self._trigger_type_hysteresis, wx.ID_ANY, "0.0", min=-30.0, max=30.0)  # noqa: E501
        self._trigger_slope_hysteresis = wx.ComboBox(self._trigger_type_hysteresis, wx.ID_ANY, choices=["Positive", "Negative"], style=wx.CB_DROPDOWN | wx.CB_READONLY)  # noqa: E501
        self._trigger_coupling_hysteresis = wx.ComboBox(self._trigger_type_hysteresis, wx.ID_ANY, choices=["AC", "DC", "HF_REJECT", "LF_REJECT", "AC_PLUS_HF_REJECT"], style=wx.CB_DROPDOWN | wx.CB_READONLY)  # noqa: E501
        figure = Figure()
        self._waveform_axes = figure.add_subplot(111)
        self._waveform_canvas = FigureCanvas(self, wx.ID_ANY, figure)
        self._status = wx.StaticText(self, wx.ID_ANY, "Good!")
        # Extra code that we need somewhere in the generated code
        self._timer = wx.Timer(self, wx.ID_ANY)
        self._running = False
        self.Bind(wx.EVT_TIMER, self.OnUpdate, self._timer)
        self._timer.Start(250)
        self._dev_name = ''
        self._session = None

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_COMBOBOX, self.OnConfigUpdate, self._devices)
        self.Bind(wx.EVT_TEXT, self.OnConfigUpdate, self._devices)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnConfigUpdate, self._devices)
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnConfigUpdate, self._min_sample_rate)  # noqa: E501
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnConfigUpdate, self._min_record_length)  # noqa: E501
        self.Bind(wx.EVT_TEXT_ENTER, self.OnConfigUpdate, self._channel_list)  # noqa: E501
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnConfigUpdate, self._vertical_range)  # noqa: E501
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnConfigUpdate, self._probe_attenuation)  # noqa: E501
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnConfigUpdate, self._vertical_offset)  # noqa: E501
        self.Bind(wx.EVT_COMBOBOX, self.OnConfigUpdate, self._vertical_coupling)  # noqa: E501
        self.Bind(wx.EVT_TEXT, self.OnConfigUpdate, self._vertical_coupling)  # noqa: E501
        self.Bind(wx.EVT_TEXT_ENTER, self.OnConfigUpdate, self._vertical_coupling)  # noqa: E501
        self.Bind(wx.EVT_TEXT, self.OnConfigUpdate, self._trigger_source_edge)  # noqa: E501
        self.Bind(wx.EVT_TEXT_ENTER, self.OnConfigUpdate, self._trigger_source_edge)  # noqa: E501
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnConfigUpdate, self._trigger_level_edge)  # noqa: E501
        self.Bind(wx.EVT_COMBOBOX, self.OnConfigUpdate, self._trigger_slope_edge)  # noqa: E501
        self.Bind(wx.EVT_TEXT, self.OnConfigUpdate, self._trigger_slope_edge)  # noqa: E501
        self.Bind(wx.EVT_TEXT_ENTER, self.OnConfigUpdate, self._trigger_slope_edge)  # noqa: E501
        self.Bind(wx.EVT_COMBOBOX, self.OnConfigUpdate, self._trigger_coupling_edge)  # noqa: E501
        self.Bind(wx.EVT_TEXT, self.OnConfigUpdate, self._trigger_coupling_edge)  # noqa: E501
        self.Bind(wx.EVT_TEXT_ENTER, self.OnConfigUpdate, self._trigger_coupling_edge)  # noqa: E501
        self.Bind(wx.EVT_TEXT, self.OnConfigUpdate, self._trigger_source_digital)  # noqa: E501
        self.Bind(wx.EVT_TEXT_ENTER, self.OnConfigUpdate, self._trigger_source_digital)  # noqa: E501
        self.Bind(wx.EVT_COMBOBOX, self.OnConfigUpdate, self._trigger_slope_digital)  # noqa: E501
        self.Bind(wx.EVT_TEXT, self.OnConfigUpdate, self._trigger_slope_digital)  # noqa: E501
        self.Bind(wx.EVT_TEXT_ENTER, self.OnConfigUpdate, self._trigger_slope_digital)  # noqa: E501
        self.Bind(wx.EVT_TEXT, self.OnConfigUpdate, self._trigger_source_window)  # noqa: E501
        self.Bind(wx.EVT_TEXT_ENTER, self.OnConfigUpdate, self._trigger_source_window)  # noqa: E501
        self.Bind(wx.EVT_COMBOBOX, self.OnConfigUpdate, self._mode_window)
        self.Bind(wx.EVT_TEXT, self.OnConfigUpdate, self._mode_window)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnConfigUpdate, self._mode_window)
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnConfigUpdate, self._low_level_window)  # noqa: E501
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnConfigUpdate, self._high_level_window)  # noqa: E501
        self.Bind(wx.EVT_COMBOBOX, self.OnConfigUpdate, self._trigger_coupling_window)  # noqa: E501
        self.Bind(wx.EVT_TEXT, self.OnConfigUpdate, self._trigger_coupling_window)  # noqa: E501
        self.Bind(wx.EVT_TEXT_ENTER, self.OnConfigUpdate, self._trigger_coupling_window)  # noqa: E501
        self.Bind(wx.EVT_TEXT, self.OnConfigUpdate, self._trigger_source_hysteresis)  # noqa: E501
        self.Bind(wx.EVT_TEXT_ENTER, self.OnConfigUpdate, self._trigger_source_hysteresis)  # noqa: E501
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnConfigUpdate, self._trigger_level_hysteresis)  # noqa: E501
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnConfigUpdate, self._hysteresis)  # noqa: E501
        self.Bind(wx.EVT_COMBOBOX, self.OnConfigUpdate, self._trigger_slope_hysteresis)  # noqa: E501
        self.Bind(wx.EVT_TEXT, self.OnConfigUpdate, self._trigger_slope_hysteresis)  # noqa: E501
        self.Bind(wx.EVT_TEXT_ENTER, self.OnConfigUpdate, self._trigger_slope_hysteresis)  # noqa: E501
        self.Bind(wx.EVT_COMBOBOX, self.OnConfigUpdate, self._trigger_coupling_hysteresis)  # noqa: E501
        self.Bind(wx.EVT_TEXT, self.OnConfigUpdate, self._trigger_coupling_hysteresis)  # noqa: E501
        self.Bind(wx.EVT_TEXT_ENTER, self.OnConfigUpdate, self._trigger_coupling_hysteresis)  # noqa: E501
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: SFP.__set_properties
        self.SetTitle("NI-SCOPE Simple Soft Front Panel")
        self._vertical_coupling.SetSelection(0)
        self._trigger_slope_edge.SetSelection(0)
        self._trigger_coupling_edge.SetSelection(0)
        self._trigger_coupling_window.SetSelection(0)
        self._trigger_slope_hysteresis.SetSelection(0)
        self._trigger_coupling_hysteresis.SetSelection(0)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: SFP.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_10 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Status"), wx.HORIZONTAL)  # noqa: E501
        sizer_5 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Results:"), wx.VERTICAL)  # noqa: E501
        sizer_2 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Configuration"), wx.VERTICAL)  # noqa: E501
        grid_sizer_5 = wx.GridSizer(0, 2, 0, 0)
        grid_sizer_4 = wx.GridSizer(0, 2, 0, 0)
        grid_sizer_3 = wx.GridSizer(4, 2, 0, 0)
        grid_sizer_2 = wx.GridSizer(0, 2, 0, 0)
        sizer_4 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Vertical"), wx.VERTICAL)  # noqa: E501
        grid_sizer_1 = wx.GridSizer(0, 4, 0, 0)
        sizer_11 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Horizontal"), wx.VERTICAL)  # noqa: E501
        grid_sizer_6 = wx.GridSizer(0, 4, 0, 0)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        label_1 = wx.StaticText(self, wx.ID_ANY, "Device:  ")
        label_1.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        sizer_3.Add(label_1, 25, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_3.Add(self._devices, 25, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 5)  # noqa: E501
        sizer_3.Add((20, 20), 50, 0, 0)
        sizer_1.Add(sizer_3, 3, wx.EXPAND, 0)
        static_line_1 = wx.StaticLine(self, wx.ID_ANY)
        sizer_1.Add(static_line_1, 1, wx.EXPAND, 0)
        label_11 = wx.StaticText(self, wx.ID_ANY, "Min Sample Rate")
        grid_sizer_6.Add(label_11, 25, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_6.Add(self._min_sample_rate, 25, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 5)  # noqa: E501
        label_8 = wx.StaticText(self, wx.ID_ANY, "Min Record Length")
        grid_sizer_6.Add(label_8, 25, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_6.Add(self._min_record_length, 25, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)  # noqa: E501
        label_6 = wx.StaticText(self, wx.ID_ANY, "Channels (blank for all)")
        grid_sizer_6.Add(label_6, 25, 0, 0)
        grid_sizer_6.Add(self._channel_list, 25, 0, 0)
        grid_sizer_6.Add((20, 20), 25, 0, 0)
        grid_sizer_6.Add((20, 20), 25, 0, 0)
        sizer_11.Add(grid_sizer_6, 1, wx.EXPAND, 0)
        sizer_2.Add(sizer_11, 0, wx.EXPAND, 0)
        label_2 = wx.StaticText(self, wx.ID_ANY, "Vertical Range (V)")
        grid_sizer_1.Add(label_2, 25, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self._vertical_range, 25, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 5)  # noqa: E501
        label_3 = wx.StaticText(self, wx.ID_ANY, "Probe Attenuation")
        grid_sizer_1.Add(label_3, 25, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self._probe_attenuation, 25, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.LEFT, 0)  # noqa: E501
        label_4 = wx.StaticText(self, wx.ID_ANY, "Vertical Offset (V)")
        grid_sizer_1.Add(label_4, 25, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self._vertical_offset, 25, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 5)  # noqa: E501
        label_5 = wx.StaticText(self, wx.ID_ANY, "Vertical Coupling")
        grid_sizer_1.Add(label_5, 25, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self._vertical_coupling, 25, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.LEFT, 0)  # noqa: E501
        sizer_4.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        sizer_2.Add(sizer_4, 0, wx.EXPAND, 0)
        label_9 = wx.StaticText(self._trigger_type_edge, wx.ID_ANY, "Trigger Source")  # noqa: E501
        grid_sizer_2.Add(label_9, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 5)  # noqa: E501
        grid_sizer_2.Add(self._trigger_source_edge, 0, wx.ALIGN_CENTER_VERTICAL, 0)  # noqa: E501
        label_10 = wx.StaticText(self._trigger_type_edge, wx.ID_ANY, "Trigger Level")  # noqa: E501
        grid_sizer_2.Add(label_10, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 5)  # noqa: E501
        grid_sizer_2.Add(self._trigger_level_edge, 0, wx.ALIGN_CENTER_VERTICAL, 0)  # noqa: E501
        label_12 = wx.StaticText(self._trigger_type_edge, wx.ID_ANY, "Trigger Slope")  # noqa: E501
        grid_sizer_2.Add(label_12, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 5)  # noqa: E501
        grid_sizer_2.Add(self._trigger_slope_edge, 0, wx.ALIGN_CENTER_VERTICAL, 0)  # noqa: E501
        label_13 = wx.StaticText(self._trigger_type_edge, wx.ID_ANY, "Trigger Coupling")  # noqa: E501
        grid_sizer_2.Add(label_13, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 5)  # noqa: E501
        grid_sizer_2.Add(self._trigger_coupling_edge, 0, wx.ALIGN_CENTER_VERTICAL, 0)  # noqa: E501
        self._trigger_type_edge.SetSizer(grid_sizer_2)
        label_14 = wx.StaticText(self._trigger_type_digital, wx.ID_ANY, "Trigger Source")  # noqa: E501
        grid_sizer_3.Add(label_14, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 5)  # noqa: E501
        grid_sizer_3.Add(self._trigger_source_digital, 0, wx.ALIGN_CENTER_VERTICAL, 0)  # noqa: E501
        label_15 = wx.StaticText(self._trigger_type_digital, wx.ID_ANY, "Trigger Slope")  # noqa: E501
        grid_sizer_3.Add(label_15, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 5)  # noqa: E501
        grid_sizer_3.Add(self._trigger_slope_digital, 0, wx.ALIGN_CENTER_VERTICAL, 0)  # noqa: E501
        grid_sizer_3.Add((20, 20), 0, 0, 0)
        grid_sizer_3.Add((20, 20), 0, 0, 0)
        grid_sizer_3.Add((20, 20), 0, 0, 0)
        grid_sizer_3.Add((20, 20), 0, 0, 0)
        self._trigger_type_digital.SetSizer(grid_sizer_3)
        label_16 = wx.StaticText(self._trigger_type_window, wx.ID_ANY, "Trigger Source")  # noqa: E501
        grid_sizer_4.Add(label_16, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 5)  # noqa: E501
        grid_sizer_4.Add(self._trigger_source_window, 0, wx.ALIGN_CENTER_VERTICAL, 0)  # noqa: E501
        label_17 = wx.StaticText(self._trigger_type_window, wx.ID_ANY, "Window Mode")  # noqa: E501
        grid_sizer_4.Add(label_17, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 5)  # noqa: E501
        grid_sizer_4.Add(self._mode_window, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        label_18 = wx.StaticText(self._trigger_type_window, wx.ID_ANY, "Window Low Level")  # noqa: E501
        grid_sizer_4.Add(label_18, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 5)  # noqa: E501
        grid_sizer_4.Add(self._low_level_window, 0, wx.ALIGN_CENTER_VERTICAL, 0)  # noqa: E501
        label_19 = wx.StaticText(self._trigger_type_window, wx.ID_ANY, "Window High Level")  # noqa: E501
        grid_sizer_4.Add(label_19, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 5)  # noqa: E501
        grid_sizer_4.Add(self._high_level_window, 0, wx.ALIGN_CENTER_VERTICAL, 0)  # noqa: E501
        label_20 = wx.StaticText(self._trigger_type_window, wx.ID_ANY, "Trigger Coupling")  # noqa: E501
        grid_sizer_4.Add(label_20, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 5)  # noqa: E501
        grid_sizer_4.Add(self._trigger_coupling_window, 0, wx.ALIGN_CENTER_VERTICAL, 0)  # noqa: E501
        self._trigger_type_window.SetSizer(grid_sizer_4)
        label_21 = wx.StaticText(self._trigger_type_hysteresis, wx.ID_ANY, "Trigger Source")  # noqa: E501
        grid_sizer_5.Add(label_21, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 5)  # noqa: E501
        grid_sizer_5.Add(self._trigger_source_hysteresis, 0, 0, 0)
        label_22 = wx.StaticText(self._trigger_type_hysteresis, wx.ID_ANY, "Trigger Level")  # noqa: E501
        grid_sizer_5.Add(label_22, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 5)  # noqa: E501
        grid_sizer_5.Add(self._trigger_level_hysteresis, 0, 0, 0)
        label_23 = wx.StaticText(self._trigger_type_hysteresis, wx.ID_ANY, "Hysteresis")  # noqa: E501
        grid_sizer_5.Add(label_23, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 5)  # noqa: E501
        grid_sizer_5.Add(self._hysteresis, 0, 0, 0)
        label_24 = wx.StaticText(self._trigger_type_hysteresis, wx.ID_ANY, "Trigger Slope")  # noqa: E501
        grid_sizer_5.Add(label_24, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 5)  # noqa: E501
        grid_sizer_5.Add(self._trigger_slope_hysteresis, 0, 0, 0)
        label_25 = wx.StaticText(self._trigger_type_hysteresis, wx.ID_ANY, "Trigger Coupling")  # noqa: E501
        grid_sizer_5.Add(label_25, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT, 5)  # noqa: E501
        grid_sizer_5.Add(self._trigger_coupling_hysteresis, 0, 0, 0)
        self._trigger_type_hysteresis.SetSizer(grid_sizer_5)
        self._trigger_type.AddPage(self._trigger_type_immediate, "Immediate")
        self._trigger_type.AddPage(self._trigger_type_edge, "Edge")
        self._trigger_type.AddPage(self._trigger_type_digital, "Digital")
        self._trigger_type.AddPage(self._trigger_type_window, "Window")
        self._trigger_type.AddPage(self._trigger_type_hysteresis, "Hysteresis")
        sizer_2.Add(self._trigger_type, 0, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 15, wx.EXPAND, 0)
        sizer_5.Add(self._waveform_canvas, 0, wx.EXPAND, 0)
        sizer_1.Add(sizer_5, 25, wx.EXPAND, 0)
        sizer_10.Add(self._status, 0, 0, 0)
        sizer_1.Add(sizer_10, 10, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def OnUpdate(self, event):  # noqa: N802
        if not self._running:
            return

        status = self._session.acquisition_status()
        if status != niscope.AcquisitionStatus.COMPLETE:
            return

        with warnings.catch_warnings(record=True) as w:
            try:
                num_samples = int(self._min_record_length.GetValue())
            except TypeError as e:
                self._status.SetLabel('Error getting horizontal configuration: {0}'.format(str(e)))  # noqa: E501
                self._status.Wrap(500)

            channel_list = ','.join(['{0}'.format(i) for i in range(self._session.channel_count)]) if self._channel_list.GetValue() == '' else self._channel_list.GetValue()  # noqa: E501
            wfm_infos = self._session.channels[channel_list].fetch(num_samples=num_samples)  # noqa: E501
            if len(w) > 0:  # that means we got a warning so we will put it in the status area  # noqa: E501
                self._status.SetLabel(str(w[0].message))
                self._status.Wrap(500)

        if self._cached_x_increment != wfm_infos[0].x_increment or self._cached_absolute_initial_x != wfm_infos[0].absolute_initial_x or len(self._cached_x_axis_values) != num_samples:  # noqa: E501
            self._cached_x_axis_values = []
            for i in range(num_samples):
                self._cached_x_axis_values.append(wfm_infos[0].absolute_initial_x + (i * wfm_infos[0].x_increment))  # noqa: E501
            self._cached_x_increment = wfm_infos[0].x_increment
            self._cached_absolute_initial_x = wfm_infos[0].absolute_initial_x

        self._waveform_axes.clear()
        for wfm_info in wfm_infos:
            self._waveform_axes.plot(self._cached_x_axis_values, wfm_info.samples)  # noqa: E501
        self._waveform_canvas.draw()

    def OnConfigUpdate(self, event):  # noqa: N802
        current_dev_name = self._devices.GetStringSelection()

        try:
            if current_dev_name != self._dev_name:
                if self._session is not None:
                    self._running = False
                    self._session.close()
                self._session = niscope.Session(current_dev_name)

            # Get and validate parameters for configure vertical
            try:
                vert_range = float(self._vertical_range.GetValue())
                coupling = get_vertical_coupling_enum(self._vertical_coupling.GetStringSelection())  # noqa: E501
                vert_offset = float(self._vertical_offset.GetValue())
                probe_atten = float(self._probe_attenuation.GetValue())
            except TypeError as e:
                self._status.SetLabel('Error getting vertical configuration: {0}'.format(str(e)))  # noqa: E501
                self._status.Wrap(500)
            self._session.configure_vertical(vert_range, coupling, vert_offset, probe_atten)  # noqa: E501

            # Get and validate parameters for configure horizontal timing
            try:
                min_sample_rate = float(self._min_sample_rate.GetValue())
                min_record_length = int(self._min_record_length.GetValue())
            except TypeError as e:
                self._status.SetLabel('Error getting horizontal configuration: {0}'.format(str(e)))  # noqa: E501
                self._status.Wrap(500)
            self._session.configure_horizontal_timing(min_sample_rate, min_record_length, 0.50, 1, True)  # noqa: E501

            # Set Auto trigger to true
            self._session.trigger_modifier = niscope.TriggerModifier.AUTO

            # Determine trigger type and call configuration function
            trigger_type = self._trigger_type.GetPageText(self._trigger_type.GetSelection())  # noqa: E501
            if trigger_type == 'Immediate':
                self.configure_trigger_immediate()
            elif trigger_type == 'Edge':
                self.configure_trigger_edge()
            elif trigger_type == 'Digital':
                self.configure_trigger_digital()
            elif trigger_type == 'Window':
                self.configure_trigger_window()
            elif trigger_type == 'Hysteresis':
                self.configure_trigger_hysteresis()
            else:
                raise TypeError('Invalid trigger type: {0}'.format(trigger_type))  # noqa: E501

            self._session._initiate_acquisition()
            self._running = True
            self._cached_absolute_initial_x = 0.0
            self._cached_x_increment = 0.0
        except niscope.Error as e:
            self._status.SetLabel(str(e))
            self._status.Wrap(500)

        self._dev_name = current_dev_name

    def configure_trigger_immediate(self):
        self._session.configure_trigger_immediate()

    def configure_trigger_edge(self):
        try:
            trigger_source = self._trigger_source_edge.GetLineText(0)
            trigger_coupling = get_trigger_coupling_enum(self._trigger_coupling_edge.GetStringSelection())  # noqa: E501
            trigger_slope = get_slope_enum(self._trigger_slope_edge.GetStringSelection())  # noqa: E501
            trigger_level = float(self._trigger_level_edge.GetValue())
        except TypeError as e:
            self._status.SetLabel('Error getting edge trigger configuration: {0}'.format(str(e)))  # noqa: E501
            self._status.Wrap(500)
        self._session.configure_trigger_edge(trigger_source, trigger_coupling, trigger_level, trigger_slope)  # noqa: E501

    def configure_trigger_digital(self):
        try:
            trigger_source = self._trigger_source_digital.GetLineText(0)
            trigger_slope = get_slope_enum(self._trigger_slope_digital.GetStringSelection())  # noqa: E501
        except TypeError as e:
            self._status.SetLabel('Error getting digital trigger configuration: {0}'.format(str(e)))  # noqa: E501
            self._status.Wrap(500)
        self._session.configure_trigger_digital(trigger_source, trigger_slope)

    def configure_trigger_window(self):
        try:
            trigger_source = self._trigger_source_window.GetLineText(0)
            trigger_coupling = get_trigger_coupling_enum(self._trigger_coupling_window.GetStringSelection())  # noqa: E501
            trigger_low = float(self._low_level_window.GetValue())
            trigger_high = float(self._high_level_window.GetValue())
            window_mode = get_mode_enum(self._mode_window.GetStringSelection())
        except TypeError as e:
            self._status.SetLabel('Error getting edge trigger configuration: {0}'.format(str(e)))  # noqa: E501
            self._status.Wrap(500)
        self._session.configure_trigger_window(trigger_source, trigger_low, trigger_high, window_mode, trigger_coupling)  # noqa: E501

    def configure_trigger_hysteresis(self):
        try:
            trigger_source = self._trigger_source_hysteresis.GetLineText(0)
            trigger_coupling = get_trigger_coupling_enum(self._trigger_coupling_hysteresis.GetStringSelection())  # noqa: E501
            trigger_slope = get_slope_enum(self._trigger_slope_hysteresis.GetStringSelection())  # noqa: E501
            trigger_level = float(self._trigger_level_hysteresis.GetValue())
            hysteresis = float(self._hysteresis.GetValue())
        except TypeError as e:
            self._status.SetLabel('Error getting hysteresis trigger configuration: {0}'.format(str(e)))  # noqa: E501
            self._status.Wrap(500)
        self._session.configure_trigger_hysteresis(trigger_source, trigger_coupling, trigger_level, hysteresis, trigger_slope)  # noqa: E501

    def OnCloseWindow(self, event):  # noqa: N802
        if self._session is not None:
            self._session.close()
        self.Destroy()

    def OnIdle(self, event):  # noqa: N802
        self.idleCtrl.SetValue(str(self.count))
        self.count = self.count + 1

    def OnSize(self, event):  # noqa: N802
        size = event.GetSize()
        self.sizeCtrl.SetValue("%s, %s" % (size.width, size.height))
        event.Skip()

    def OnMove(self, event):  # noqa: N802
        pos = event.GetPosition()
        self.posCtrl.SetValue("%s, %s" % (pos.x, pos.y))


class SFPApp(AppBaseClass):

    def OnInit(self):  # noqa: N802
        self.frame = SFP(None, wx.ID_ANY, "NI-DMM Python SFP")
        self.SetTopWindow(self.frame)

        if USE_WIT:
            self.InitInspection()

        self.frame.Show(True)
        return True


app = SFPApp(False)
app.MainLoop()
