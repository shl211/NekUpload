import ttkbootstrap as ttk
import tkinter as tk
from tkinter import filedialog
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from NekUpload.newFrontend.components.help import HelpNotification
from ttkbootstrap.tableview import Tableview
from NekUpload.newFrontend.scenes.create_author_window import CreateAuthorOrgWindow,CreateAuthorPersonWindow
from typing import List,Dict,Tuple
from .upload_widgets.geometry import UploadGeometryFrame

class UploadScene(ScrolledFrame):
    def __init__(self,root,parent):
        super().__init__(parent,autohide=True)

        self.root = root

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.columnconfigure(0,weight=1)

        about_section: ttk.Frame = self._add_upload_info_section(self)
        about_section.grid(row=0,column=0,sticky=(NSEW))

        basic_info_section: ttk.Labelframe = self._basic_info_frame(self)
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
    
    def _basic_info_frame(self,parent) -> ttk.Labelframe:
        frame = ttk.Labelframe(
            master=parent,
            text="Basic Information",
            bootstyle=PRIMARY,
            padding=10
        )

        frame.columnconfigure(0,weight=1)
        frame.columnconfigure(1,weight=1)
        frame.columnconfigure(2,weight=5)
        frame.columnconfigure(3,weight=5)
        frame.rowconfigure(0,weight=1)

        community_upload_label = ttk.Label(
            master=frame,
            text="Upload to community: ",
            bootstyle=PRIMARY
        )
        community_upload_label.grid(row=0,column=0,sticky=W)

        presets = ttk.Combobox(
            master=frame,
            values=["Nektar", "Custom"],
            state="readonly"
        )
        presets.set("Nektar")
        presets.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        self.authors = []

        add_author_person_button = ttk.Button(
            master=frame,
            text="Add Person",
            command=self._create_author_person
        )
        add_author_person_button.grid(row=1,column=0,padx=5,pady=5,sticky=NSEW)

        add_author_org_button = ttk.Button(
            master=frame,
            text="Add Organisation",
            command=self._create_author_org
        )
        add_author_org_button.grid(row=1,column=1,padx=5,pady=5,sticky=NSEW)

        coldata = [
            {"text" : "Name", "stretch": False},
            "Type",
            {"text": "Persistent ID Type", "stretch": False},
            {"text": "Persistent ID", "stretch": False},
        ]

        rowdata = []
        self.authors_table_display = Tableview(
            master=frame,
            coldata=coldata,
            rowdata=rowdata,
            searchable=False,
            bootstyle=DEFAULT,
        )
        self.authors_table_display.grid(row=3,column=0,columnspan=10,sticky=NSEW)

        return frame
    
    def _create_author_person(self) -> None:
        """Opens a new window with a form to specify the author as a person
        """
        
        # The lambda function will be executed later when triggered by an event.
        # By that time, new_window will have already been created by __init__.
        # This works because lambdas capture variables by reference, not by value.
        new_window = CreateAuthorPersonWindow(self.root,lambda: self.submit_author_person_info(new_window))

    def _create_author_org(self) -> None:
        """Opens a new window with a form to specify the author as an organisation
        """
        # The lambda function will be executed later when triggered by an event.
        # By that time, new_window will have already been created by __init__.
        # This works because lambdas capture variables by reference, not by value.
        new_window = CreateAuthorOrgWindow(self.root,lambda: self.submit_author_org_info(new_window))

    def submit_author_person_info(self,window: CreateAuthorPersonWindow):
        """Takes person data from CreateAuthorPersonWindow and stores it. Closes window on success.

        Args:
            window (CreateAuthorPersonWindow): Window containing form to specify user info
        """
        author_data = {}
        author_data['type'] = 'personal'
        author_data['given_name'] = window.given_name
        author_data['last_name'] = window.last_name
        author_data['name'] = f"{author_data['given_name']} {author_data['last_name']}"
        author_data['affiliation'] = window.affiliation
        author_data['id_type'] = window.id_type
        author_data['id'] = window.id

        print("Author Data: ", author_data)

        self.authors.append(author_data)        
        self._add_to_table_display(author_data)

        window.destroy()

    def submit_author_org_info(self,window: CreateAuthorOrgWindow):
        """Takes person data from CreateAuthorOrgWindow and stores it. Closes window on success.

        Args:
            window (CreateAuthorOrgWindow): Window containing form to specify organisation info
        """
        author_data = {}
        author_data['type'] = 'organizational'
        author_data['name'] = window.name
        author_data['affiliation'] = window.affiliation
        author_data['id_type'] = window.id_type
        author_data['id'] = window.id

        print("Author Data: ", author_data)

        self.authors.append(author_data)
        self._add_to_table_display(author_data)
        window.destroy()

    def _add_to_table_display(self,author_data: Dict[str,str]):
        self.authors_table_display.insert_row(values=[
            author_data['name'],
            author_data["type"],
            author_data["id_type"],
            author_data["id"]
        ])
        self.authors_table_display.load_table_data(clear_filters=True)