import nimodinst
import niswitch
import wx


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((400, 400))
        self.device_value = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)  # noqa: E501
        self.topology_value = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)
        self.tab_control = wx.Notebook(self, wx.ID_ANY)
        self.channel_tab = wx.Panel(self.tab_control, wx.ID_ANY)
        self.channel_1_value = wx.ComboBox(self.channel_tab, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)  # noqa: E501
        self.channel_2_value = wx.ComboBox(self.channel_tab, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)  # noqa: E501
        self.connection_status = wx.TextCtrl(self.channel_tab, wx.ID_ANY, "")
        self.activate_channel = wx.Button(self.channel_tab, wx.ID_ANY, "Connect!")  # noqa: E501
        self.relay_tab = wx.Panel(self.tab_control, wx.ID_ANY)
        self.relay_name_value = wx.ComboBox(self.relay_tab, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)  # noqa: E501
        self.relay_status_value = wx.TextCtrl(self.relay_tab, wx.ID_ANY, "")
        self.relay_count_value = wx.TextCtrl(self.relay_tab, wx.ID_ANY, "")
        self.activate_relay = wx.Button(self.relay_tab, wx.ID_ANY, "Close Relay!")  # noqa: E501
        self.status = wx.StaticText(self, wx.ID_ANY, "Good!")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

        self.Bind(wx.EVT_CLOSE, self.__window_close_event)

        # Changing channel, function or device closes and creates new session
        self.Bind(wx.EVT_COMBOBOX, self.__change_device_event, self.device_value)  # noqa: E501

        # Changing properties updates reading
        self.Bind(wx.EVT_BUTTON, self.__activate_relay, self.activate_relay)  # noqa: E501
        self.Bind(wx.EVT_BUTTON, self.__activate_channel, self.activate_channel)  # noqa: E501
        self.Bind(wx.EVT_COMBOBOX, self.__update_selection_event, self.relay_name_value)  # noqa: E501
        self.Bind(wx.EVT_COMBOBOX, self.__update_selection_event, self.channel_1_value)  # noqa: E501
        self.Bind(wx.EVT_COMBOBOX, self.__update_selection_event, self.channel_2_value)  # noqa: E501

        self._error = False
        self._session = None
        self._modinst_session = None
        self._dev_name = None

        # Using NI-ModInst session to list available NI-DCPower devices
        self._modinst_session = nimodinst.Session('niswitch')
        for dev in self._modinst_session.devices:
            dev_name = dev.device_name
            self.device_value.Append('{0}'.format(dev_name))
        self.device_value.SetSelection(0)

        # Opening a new session to the selected device
        self.__initialize_new_session()

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("NI-SWITCH Simple SFP")
        self.device_value.SetMinSize((111, 23))
        self.topology_value.SetMinSize((111, 23))
        self.activate_channel.SetMinSize((115, 26))
        self.relay_status_value.SetMinSize((111, 23))
        self.relay_count_value.SetMinSize((111, 23))
        self.activate_relay.SetMinSize((115, 26))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        status_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Status"), wx.HORIZONTAL)  # noqa: E501
        relay_tab_sizer = wx.BoxSizer(wx.VERTICAL)
        relay_count_sizer = wx.BoxSizer(wx.HORIZONTAL)
        relay_status_sizer = wx.BoxSizer(wx.HORIZONTAL)
        relay_name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        channel_tab_sizer = wx.BoxSizer(wx.VERTICAL)
        channel_status_sizer = wx.BoxSizer(wx.HORIZONTAL)
        channel_2_sizer = wx.BoxSizer(wx.HORIZONTAL)
        channel_1_sizer = wx.BoxSizer(wx.HORIZONTAL)
        device_sizer = wx.BoxSizer(wx.VERTICAL)
        topology_sizer = wx.BoxSizer(wx.HORIZONTAL)
        device_selection_sizer = wx.BoxSizer(wx.HORIZONTAL)
        device_selection_sizer.Add(self.device_value, 0, wx.ALIGN_CENTER, 0)
        device_label = wx.StaticText(self, wx.ID_ANY, "Device Name")
        device_selection_sizer.Add(device_label, 0, wx.ALIGN_CENTER, 0)
        device_sizer.Add(device_selection_sizer, 1, wx.EXPAND, 0)
        topology_sizer.Add(self.topology_value, 0, 0, 0)
        topology_label = wx.StaticText(self, wx.ID_ANY, "Device Topology")
        topology_sizer.Add(topology_label, 0, 0, 0)
        device_sizer.Add(topology_sizer, 1, wx.EXPAND, 0)
        main_sizer.Add(device_sizer, 1, wx.EXPAND, 0)
        channel_1_sizer.Add(self.channel_1_value, 0, 0, 0)
        channel_1_label = wx.StaticText(self.channel_tab, wx.ID_ANY, "Channel 1")  # noqa: E501
        channel_1_sizer.Add(channel_1_label, 0, 0, 0)
        channel_tab_sizer.Add(channel_1_sizer, 1, wx.EXPAND, 0)
        channel_2_sizer.Add(self.channel_2_value, 0, 0, 0)
        channel_2_label = wx.StaticText(self.channel_tab, wx.ID_ANY, "Channel 2")  # noqa: E501
        channel_2_sizer.Add(channel_2_label, 0, 0, 0)
        channel_tab_sizer.Add(channel_2_sizer, 1, wx.EXPAND, 0)
        channel_status_sizer.Add(self.connection_status, 0, 0, 0)
        connection_status_label = wx.StaticText(self.channel_tab, wx.ID_ANY, "Connection Status")  # noqa: E501
        channel_status_sizer.Add(connection_status_label, 0, 0, 0)
        channel_tab_sizer.Add(channel_status_sizer, 1, wx.EXPAND, 0)
        channel_tab_sizer.Add(self.activate_channel, 0, 0, 0)
        self.channel_tab.SetSizer(channel_tab_sizer)
        relay_name_sizer.Add(self.relay_name_value, 0, 0, 0)
        relay_name_label = wx.StaticText(self.relay_tab, wx.ID_ANY, "Name")
        relay_name_sizer.Add(relay_name_label, 0, 0, 0)
        relay_tab_sizer.Add(relay_name_sizer, 1, wx.EXPAND | wx.SHAPED, 0)
        relay_status_sizer.Add(self.relay_status_value, 0, 0, 0)
        relay_status_label = wx.StaticText(self.relay_tab, wx.ID_ANY, "Status")
        relay_status_sizer.Add(relay_status_label, 0, 0, 0)
        relay_tab_sizer.Add(relay_status_sizer, 1, wx.EXPAND, 0)
        relay_count_sizer.Add(self.relay_count_value, 0, 0, 0)
        relay_count_label = wx.StaticText(self.relay_tab, wx.ID_ANY, "Count")
        relay_count_sizer.Add(relay_count_label, 0, 0, 0)
        relay_tab_sizer.Add(relay_count_sizer, 1, wx.EXPAND, 0)
        relay_tab_sizer.Add(self.activate_relay, 0, 0, 0)
        self.relay_tab.SetSizer(relay_tab_sizer)
        self.tab_control.AddPage(self.channel_tab, "Channels")
        self.tab_control.AddPage(self.relay_tab, "Relays")
        main_sizer.Add(self.tab_control, 5, wx.EXPAND, 0)
        status_sizer.Add(self.status, 0, 0, 0)
        main_sizer.Add(status_sizer, 6, wx.EXPAND, 0)
        self.SetSizer(main_sizer)
        self.Layout()
        # end wxGlade

    def __initialize_new_session(self):
        # Open session to device
        try:
            if self._session is not None:
                self._session.close()
            self._session = niswitch.Session(self.device_value.GetStringSelection())  # noqa: E501

            # Add total channels on device to combo-box
            channels = self._session.channel_count
            self.channel_1_value.Clear()
            self.channel_2_value.Clear()
            for channel in range(channels):
                self.channel_1_value.Append(self._session.get_channel_name(channel + 1))  # noqa: E501
                self.channel_2_value.Append(self._session.get_channel_name(channel + 1))  # noqa: E501

            # Add total relays on device to combo-box
            relays = self._session.channel_count
            self.relay_name_value.Clear()
            for relay in range(relays):
                self.relay_name_value.Append(self._session.get_relay_name(relay + 1))  # noqa: E501

            # Set selection to first item in the lists
            self.relay_name_value.SetSelection(0)
            self.channel_1_value.SetSelection(0)
            self.channel_2_value.SetSelection(0)
            self.__update_status()

        # Catch error
        except niswitch.Error as e:
            self._session = None
            self._error = True
            self.status.SetLabel(str(e))
            self.status.Wrap(350)

    def __change_device_event(self, event):
        self.__initialize_new_session()

    def __activate_relay(self, event):
        try:
            # Get current relay position to use the correct for relay action enum value  # noqa: E501
            name = self.relay_name_value.GetValue()
            position = self._session.get_relay_position(name)
            if position == niswitch.RelayPosition.OPEN:
                relay_action = niswitch.RelayAction.CLOSE
            else:
                relay_action = niswitch.RelayAction.OPEN

            # Activate selected relay with selected relay action & update status  # noqa: E501
            self._session.relay_control(name, relay_action)
            self.__update_status()
            self.status.SetLabel("Good!")
            self._error = False

        except niswitch.Error as e:
            self._error = True
            self.status.SetLabel(str(e))
            self.status.Wrap(350)

    def __activate_channel(self, event):
        try:
            # Read channel names and connection status
            channel_1 = self.channel_1_value.GetValue()
            channel_2 = self.channel_2_value.GetValue()

            # Make or break connection between selected channels
            can_connect_result = self._session.can_connect(channel_1, channel_2)  # noqa: E501

            # Based on connection status, update strings
            if can_connect_result == niswitch.PathCapability.PATH_AVAILABLE:
                self._session.connect(channel_1, channel_2)
            elif can_connect_result == niswitch.PathCapability.PATH_EXISTS:
                self._session.disconnect(channel_1, channel_2)
            self.__update_status()
            self.status.SetLabel("Good!")
            self._error = False

        except niswitch.Error as e:
            self._error = True
            self.status.SetLabel(str(e))
            self.status.Wrap(350)

    def __window_close_event(self, event):
        if self._session is not None:
            self._session.close()
        self.Destroy()

    def __update_selection_event(self, event):
        self.__update_status()

    def __update_status(self):
        if self._error is False:
            if self._session is not None:
                try:
                    # Retrieve relay count and relay position
                    name = self.relay_name_value.GetValue()
                    position = self._session.get_relay_position(name)
                    count = self._session.get_relay_count(name)

                    # Based on position of relay, update strings
                    if position == niswitch.RelayPosition.OPEN:
                        position_str = "Open"
                        activate_relay_label_str = "Close Relay!"
                    else:
                        position_str = "Closed"
                        activate_relay_label_str = "Open Relay!"
                    self.relay_status_value.SetValue(position_str)
                    self.relay_count_value.SetValue(str(count))
                    self.activate_relay.SetLabel(activate_relay_label_str)

                    # Read channel names and connection status
                    channel_1 = self.channel_1_value.GetValue()
                    channel_2 = self.channel_2_value.GetValue()
                    can_connect_result = self._session.can_connect(channel_1, channel_2)  # noqa: E501

                    # Based on connection status, update strings
                    if can_connect_result == niswitch.PathCapability.PATH_AVAILABLE:  # noqa: E501
                        connection_str = "Ready to connect"
                        activate_channel_label_str = "Connect!"
                        self.activate_channel.Enable()
                    elif can_connect_result == niswitch.PathCapability.PATH_EXISTS:  # noqa: E501
                        connection_str = "Connected"
                        activate_channel_label_str = "Disconnect"
                        self.activate_channel.Enable()
                    else:
                        connection_str = "Not Supported"
                        activate_channel_label_str = "Not Supported"
                        self.activate_channel.Disable()
                    self.connection_status.SetValue(connection_str)
                    self.activate_channel.SetLabel(activate_channel_label_str)

                    self._error = False
                    self.status.SetLabel("Good!")

                except niswitch.Error as e:
                    self._error = True
                    self.status.SetLabel(str(e))
                    self.status.Wrap(350)
# end of class MyFrame


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp


if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
