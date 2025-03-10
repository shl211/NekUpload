import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import filedialog
from NekUpload.newFrontend.components.help import HelpNotification

class UploadGeometryFrame(ttk.LabelFrame):
    def __init__(self,parent):
        super().__init__(
            master=parent,
            text="Geometry",
            bootstyle=DANGER,
            padding=10
            )

        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)

        label = ttk.Label(
            master=self,
            text="Upload all geometry related files here.",
            font=("TKDefaultFont", 12),
            anchor="w",
            justify="left",
        )
        label.grid(row=0,column=0,columnspan=2,pady=2,sticky=(NSEW))

        n = ttk.Notebook(self,bootstyle=SECONDARY)
        n.grid(row=1,column=0,columnspan=2,sticky=NSEW)
        
        f1: ttk.Frame = self._upload_geometry(n)
        f2: ttk.Frame = self._link_geometry_to_existing_record(n)

        n.add(f1,text="Upload from Source")
        n.add(f2,text="Link to Existing Record")
    
    def _link_geometry_to_existing_record(self,parent) -> ttk.Frame:
        frame = ttk.Frame(master=parent)

        todo = ttk.Label(master=frame,
                        text="TBC",
                        bootstyle=DANGER,
                        anchor="w")
        todo.grid(row=0,column=0,sticky=NSEW)

        return frame
    
    def _upload_geometry(self,parent) -> ttk.Frame:
        frame = ttk.Frame(master=parent)

        frame.rowconfigure(0,weight=1)
        frame.rowconfigure(1,weight=1)
        frame.columnconfigure(0,weight=1)
        frame.columnconfigure(1,weight=1)
        frame.columnconfigure(2,weight=1)

        geometry_file_frame: ttk.Labelframe = self._geometry_mandatory_info(frame)
        geometry_file_frame.grid(row=0,column=0,sticky=NSEW)

        return frame
    
    def _geometry_mandatory_info(self,parent) -> ttk.Labelframe:
        geometry_file_frame= ttk.Labelframe(
            master=parent,
            text="Mandatory"
        )
        geometry_file_frame.columnconfigure(0,weight=1)
        geometry_file_frame.columnconfigure(1,weight=3)
        geometry_file_frame.columnconfigure(2,weight=1)
        geometry_file_frame.columnconfigure(3,weight=1)

        ################################
        # Ask for title
        title_label = ttk.Label(
            master=geometry_file_frame,
            text="Geometry Title: "
        )
        title_label.grid(row=0,column=0,sticky=NSEW)
        
        self._geometry_title = tk.StringVar()
        geometry_title_entry = ttk.Entry(
            master=geometry_file_frame,
            textvariable=self._geometry_title,
        )
        geometry_title_entry.grid(row=0,column=1,sticky=NSEW)

        ################################
        # Ask for geometry file
        geometry_file_label = ttk.Label(
            master=geometry_file_frame,
            text="Select Geometry File: "
        )
        geometry_file_label.grid(row=1,column=0,sticky=NSEW)

        self._geometry_file = tk.StringVar()
        geometry_file_entry = ttk.Entry(
            master=geometry_file_frame,
            textvariable=self._geometry_file,
        )
        geometry_file_entry.grid(row=1,column=1,sticky=NSEW)

        def browse_file():
            file_path = filedialog.askopenfilename(
                title="Select Geometry File",
                filetypes=(("Geometry Files",".nekg"),)
            )
            self._geometry_file.set(file_path)

        browse = ttk.Button(
            master=geometry_file_frame,
            text="Browse Files",
            command=browse_file
        )
        browse.grid(row=1,column=2,sticky=NSEW)

        help_logo:ttk.Label = HelpNotification(geometry_file_frame)
        help_logo.add_help_message("This will be the title of the geometry record")
        help_logo2:ttk.Label = HelpNotification(geometry_file_frame)
        help_logo2.add_help_message("Only HDF5 formatted geometry files are accepted")
        help_logo.grid(row=0, column=3, sticky=NSEW)
        help_logo2.grid(row=1, column=3, sticky=NSEW)

        return geometry_file_frame
    
    @property
    def geometry_file_name(self):
        return self._geometry_file.get()
    
    @property
    def geometry_dataset_title(self):
        return self._geometry_title.get()