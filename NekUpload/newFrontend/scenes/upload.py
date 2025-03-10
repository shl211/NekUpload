import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from typing import List,Dict,Tuple
from .upload_widgets.geometry import UploadGeometryFrame
from .upload_widgets.basic import UploadInfoFrame
from NekUpload.newFrontend.components.settings_manager import SettingsManager

class UploadScene(ScrolledFrame):
    def __init__(self,root,parent,setting_manager: SettingsManager):
        super().__init__(parent,autohide=True)

        self.root = root
        self.setting_manager = setting_manager#contains settings data

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.columnconfigure(0,weight=1)

        about_section: ttk.Frame = self._add_upload_info_section(self)
        about_section.grid(row=0,column=0,sticky=(NSEW))

        basic_info_section: ttk.Labelframe = UploadInfoFrame(self,self,self.setting_manager)
        basic_info_section.grid(row=1,column=0,sticky=NSEW,padx=10)
        geometry_section: ttk.Labelframe = UploadGeometryFrame(self)
        geometry_section.grid(row=2,column=0,sticky=(NSEW),padx=10)


        self.bind("<Configure>", self.update_wraplength)

    def update_wraplength(self, event):
        # Dynamically set the wraplength based on the width of the parent frame
        # Subtract a little for padding and margin
        self.upload_description.config(wraplength=event.width - 20)
        pass

    def _add_upload_info_section(self,parent) -> ttk.Frame:

        frame = ttk.Frame(master=parent)

        # Create the label for the title
        self.upload_info_label = ttk.Label(
            master=frame,
            text="Uploading Nektar++ Datasets",
            font=("TkDefaultFont", 20, "bold", "underline"),
            anchor="w",
            bootstyle=PRIMARY
        )
        self.upload_info_label.grid(row=0, column=0, pady=5, sticky=W)

        # Create the description label
        self.upload_description = ttk.Label(
            master=frame,
            text=("A Nektar++ dataset consists of: \n\n"
                " - Geometry Files\n"
                " - Input Files\n"
                " - Output Files\n"
                "\n"
                "There are currently two ways of uploading. The traditional way is that you have all the geometry files, "
                "input files and output files to be uploaded. Another way is that the geometry file already exists in the "
                "database, and you wish to link your input and ouptut files against it. This prevents repeated instances of "
                "same geometry file."),
            font=("TKDefaultFont", 12),
            anchor="w",
            justify="left",
        )
        self.upload_description.grid(row=1, column=0, pady=10, sticky="nsew")

        return frame
