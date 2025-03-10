import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from ttkbootstrap.tableview import Tableview
from .create_author_window import CreateAuthorOrgWindow,CreateAuthorPersonWindow
from typing import Dict

class UploadInfoFrame(ttk.Labelframe):
    def __init__(self,root,parent):
        super().__init__(
            master=parent,
            text="Basic Upload Information",
            bootstyle=PRIMARY,
            padding=10
        )
        self.root = root
        
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=5)
        self.columnconfigure(3,weight=5)
        self.rowconfigure(0,weight=1)

        community_upload_label = ttk.Label(
            master=self,
            text="Upload to community: ",
            bootstyle=PRIMARY
        )
        community_upload_label.grid(row=0,column=0,sticky=W)

        presets = ttk.Combobox(
            master=self,
            values=["Nektar", "Custom"],
            state="readonly"
        )
        presets.set("Nektar")
        presets.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        self.authors = []

        add_author_person_button = ttk.Button(
            master=self,
            text="Add Person",
            command=self._create_author_person
        )
        add_author_person_button.grid(row=1,column=0,padx=5,pady=5,sticky=NSEW)

        add_author_org_button = ttk.Button(
            master=self,
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
            master=self,
            coldata=coldata,
            rowdata=rowdata,
            searchable=False,
            bootstyle=DEFAULT,
        )
        self.authors_table_display.grid(row=3,column=0,columnspan=10,sticky=NSEW)
    
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