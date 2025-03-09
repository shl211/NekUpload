import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
import os

class SettingScene(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)

        self.columnconfigure(0,weight=1)

        self.repository_info: ttk.LabelFrame = self._get_repository_info(self)
        self.repository_info.grid(row=0,column=0,padx=10,pady=10,sticky=NSEW)

        self.api_key_info: ttk.LabelFrame = self._get_api_key(self)
        self.api_key_info.grid(row=1,column=0,padx=10,pady=10,sticky=NSEW)

        #add a debug button for now
        self.debug_button = ttk.Button(
            master=self,
            text="DEBUG",
            command=self.debug_notify
        )
        self.debug_button.grid(row=2,column=0,sticky=E)

    def debug_notify(self,event:tk.Event=None):
        """Utility debugger

        Args:
            event (tk.Event, optional): _description_. Defaults to None.
        """
        toast = ToastNotification(
            title="Check api message",
            message=f"API KEY: {self.api_key}",
            duration=3000,
            position=(100,100,'se')
        )
        toast.show_toast()

    def _get_repository_info(self,parent) -> ttk.LabelFrame:
        frame = ttk.LabelFrame(
            master=parent,
            text="Online Repository Info"
        )
        
        preset_label = ttk.Label(
            master=frame,
            text="I am accessing: "
        )
        preset_label.grid(row=0,column=0,padx=5,pady=5,sticky=W)

        presets = ttk.Combobox(
            master=frame,
            values=["AE Datastore", "InvenioRDM Demo", "Custom"],
            state="readonly"
        )
        presets.set("AE Datastore")
        presets.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        host_label = ttk.Label(
            master=frame,
            text="Host URL: "
        )
        host_label.grid(row=1,column=0,padx=5,pady=5,sticky=W)

        self._host_url = tk.StringVar()
        host_entry = ttk.Entry(
            master=frame,
            textvariable=self._host_url
        )
        host_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        #set the defaults
        presets.bind("<<ComboboxSelected>>",self.on_combobox_select)
        self.set_AE_db_default()

        return frame

    def _get_api_key(self,parent) -> ttk.LabelFrame:
        frame = ttk.LabelFrame(
            master=parent,
            text="API Key"
        )

        #for formatting purposes, temporary for now
        frame.grid_columnconfigure(0,minsize=250,weight=1)
        frame.grid_columnconfigure(1,minsize=25,weight=1)
        frame.grid_columnconfigure(2,minsize=25,weight=1)
        frame.grid_columnconfigure(3,minsize=25,weight=1)
        frame.grid_columnconfigure(4,minsize=25,weight=1)

        radio_label = ttk.Label(
            master=frame,
            text="I have: "
        )
        radio_label.grid(row=1, column=0, padx=5, pady=5, sticky=EW)

        self._api_radio_value = tk.StringVar(value="Option1")
        radio_option1 = ttk.Radiobutton(
            master=frame,
            text="API key",
            value="Option1",
            variable=self._api_radio_value,
            command=self.update_api_form
        )
        radio_option1.grid(row=1, column=1, padx=5, pady=5, sticky=EW)

        radio_option2 = ttk.Radiobutton(
            master=frame,
            text="API key stored in environment variable",
            value="Option2",
            variable=self._api_radio_value,
            command=self.update_api_form
        )
        radio_option2.grid(row=1, column=2, padx=5, pady=5, sticky=W)

        self.api_key_label = ttk.Label(
            master=frame,
            text="API Key: "
        )
        self.api_key_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)

        self._api_key = tk.StringVar()
        api_key_entry = ttk.Entry(
            master=frame,
            textvariable=self._api_key
        )
        api_key_entry.grid(row=2, column=1,columnspan=2, pady=5, sticky=EW)

        return frame

    def update_api_form(self,event: tk.Event=None):
        if self._api_radio_value.get() == "Option1":
            self.api_key_label.configure(text="API Key: ")
        elif self._api_radio_value.get() == "Option2":
            self.api_key_label.configure(text="API Environment Variable: ")

    def on_combobox_select(self,event: tk.Event):
        """Callback for combobox selection, sets default values in some fields

        Args:
            event (Event): _description_
        """
        selected_value = event.widget.get()

        if selected_value == "AE Datastore":
            self.set_AE_db_default()
        elif selected_value == "InvenioRDM Demo":
            self.set_demo_default()
        else:
            self.set_default()

    #Sets settings for default config
    def set_AE_db_default(self):
        """Set default settings for sending to AE database
        """
        self.host_url = "https://data.ae.ic.ac.uk"

    def set_default(self):
        """No default settings
        """
        self.host_url = ""

    def set_demo_default(self):
        """Set default settings for sending to a demo instance
        """
        self.host_url = "https://inveniordm.web.cern.ch"

    @property
    def host_url(self):
        return self._host_url.get()

    @host_url.setter
    def host_url(self,value: str):
        self._host_url.set(value)

    @property
    def api_key(self):
        if self._api_radio_value.get() == "Option1":
            #if given as plain key
            return self._api_key.get()
        elif self._api_radio_value.get() == "Option2":
            #if given as environment variable
            return os.getenv(self._api_key.get(),None)