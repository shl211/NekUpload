import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import filedialog
from NekUpload.newFrontend.components.help import HelpNotification

class UploadOutputFrame(ttk.LabelFrame):
    def __init__(self,parent):
        super().__init__(
            master=parent,
            text="Output",
            bootstyle=DANGER,
            padding=10
            )

        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)

        label = ttk.Label(
            master=self,
            text="Upload all output related files here.",
            font=("TKDefaultFont", 12),
            anchor="w",
            justify="left",
        )
        label.grid(row=0,column=0,columnspan=2,pady=2,sticky=(NSEW))

        n = ttk.Notebook(self,bootstyle=SECONDARY)
        n.grid(row=1,column=0,columnspan=2,sticky=NSEW)
        
        f1: ttk.Frame = self._upload_output(n)

        n.add(f1,text="Upload from Source")
    
    def _upload_output(self,parent) -> ttk.Frame:
        frame = ttk.Frame(master=parent)

        frame.rowconfigure(0,weight=1)
        frame.rowconfigure(1,weight=1)
        frame.columnconfigure(0,weight=1)
        frame.columnconfigure(1,weight=1)
        frame.columnconfigure(2,weight=1)

        output_file_frame: ttk.Labelframe = self._output_mandatory_info(frame)
        output_file_frame.grid(row=0,column=0,sticky=NSEW)

        return frame
    
    def _output_mandatory_info(self,parent) -> ttk.Labelframe:
        output_file_frame= ttk.Labelframe(
            master=parent,
            text="Mandatory"
        )
        output_file_frame.columnconfigure(0,weight=1)
        output_file_frame.columnconfigure(1,weight=3)
        output_file_frame.columnconfigure(2,weight=1)
        output_file_frame.columnconfigure(3,weight=1)

        ################################
        # Ask for title
        title_label = ttk.Label(
            master=output_file_frame,
            text="Output Title: "
        )
        title_label.grid(row=0,column=0,sticky=NSEW)
        
        self._output_title = tk.StringVar()
        output_title_entry = ttk.Entry(
            master=output_file_frame,
            textvariable=self._output_title,
        )
        output_title_entry.grid(row=0,column=1,sticky=NSEW)

        ################################
        # Ask for output file
        output_file_label = ttk.Label(
            master=output_file_frame,
            text="Select Output File: "
        )
        output_file_label.grid(row=1,column=0,sticky=NSEW)

        self._output_file = tk.StringVar()
        output_file_entry = ttk.Entry(
            master=output_file_frame,
            textvariable=self._output_file,
        )
        output_file_entry.grid(row=1,column=1,sticky=NSEW)

        def browse_file():
            file_path = filedialog.askopenfilename(
                title="Select Output File",
                filetypes=(("Output Files",(".fld",".chk")),)
            )
            self._output_file.set(file_path)

        browse = ttk.Button(
            master=output_file_frame,
            text="Browse Files",
            command=browse_file
        )
        browse.grid(row=1,column=2,sticky=NSEW)

        help_logo:ttk.Label = HelpNotification(output_file_frame)
        help_logo.add_help_message("This will be the title of the output record")
        help_logo2:ttk.Label = HelpNotification(output_file_frame)
        help_logo2.add_help_message("Only HDF5 formatted output files are accepted")
        help_logo.grid(row=0, column=3, sticky=NSEW)
        help_logo2.grid(row=1, column=3, sticky=NSEW)

        return output_file_frame
    
    @property
    def output_file_name(self):
        return self._output_file.get()
    
    @property
    def output_dataset_title(self):
        return self._output_title.get()