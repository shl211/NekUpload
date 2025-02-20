from tkinter import * 
import tkinter.ttk as ttk
from typing import Callable

class CreateAuthorPersonWindow(Toplevel):
    def __init__(self,root: Tk, submit_function: Callable):
        super().__init__(root)

        self.title("Specify Author Information") 
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)

        content_frame = ttk.Frame(self,padding=20)
        content_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        content_frame.grid_rowconfigure(0,weight=1)
        content_frame.grid_columnconfigure(0,weight=1)

        title_label = ttk.Label(content_frame,text="Add Person Info")
        title_label.grid(row=0,column=0)

        ####### Mandatory Info
        mandatory_frame = ttk.Labelframe(content_frame,text="Mandatory Info")
        mandatory_frame.grid(column=0,row=1,sticky=(N,W,E,S))

        #ask for given name
        given_name_label = ttk.Label(mandatory_frame,text="Given Name: ")
        given_name_label.grid(row=1,column=0)
        self._given_name = StringVar()
        given_name_entry = ttk.Entry(mandatory_frame,textvariable=self._given_name)
        given_name_entry.grid(row=1,column=1)

        #ask for last name
        last_name_label = ttk.Label(mandatory_frame,text="Last Name: ")
        last_name_label.grid(row=2,column=0)
        self._last_name = StringVar()
        last_name_entry = ttk.Entry(mandatory_frame,textvariable=self._last_name)
        last_name_entry.grid(row=2,column=1)

        #########Optional
        #optional arguments: ORCID and affiliations
        optional_frame = ttk.Labelframe(content_frame,text="Optional")
        optional_frame.grid(column=0,row=2,sticky=(N,W,E,S))
        
        affiliation_label = ttk.Label(optional_frame,text="Affiliation(s): ")
        affiliation_label.grid(row=3,column=0)
        self._affiliation = StringVar()
        affiliation_entry = ttk.Entry(optional_frame,textvariable=self._affiliation)
        affiliation_entry.grid(row=3,column=1)

        self._id_type = StringVar()
        id_type_combobox = ttk.Combobox(optional_frame,
                                        textvariable=self._id_type,
                                        values=('ORCID',),
                                        state="readonly")
        id_type_combobox.grid(row=4,column=0)
        self.after(1, lambda: id_type_combobox.current(0))
        self._id = StringVar()
        id_entry = ttk.Entry(optional_frame,textvariable=self._id)
        id_entry.grid(row=4,column=1)

        submit_button = ttk.Button(content_frame,text="Submit",command=submit_function)
        submit_button.grid(row=10,column=0,pady=10)

    @property
    def given_name(self):
        return self._given_name.get()

    @property
    def last_name(self):
        return self._last_name.get()

    @property
    def affiliation(self):
        return self._affiliation.get()

    @property
    def id_type(self):
        return self._id_type.get()
    
    @property
    def id(self):
        return self._id.get()

class CreateAuthorOrgWindow(Toplevel):
    def __init__(self,root: Tk, submit_function: Callable):
        super().__init__(root)

        self.title("Specify Author Information") 
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)

        content_frame = ttk.Frame(self,padding=20)
        content_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        content_frame.grid_rowconfigure(0,weight=1)
        content_frame.grid_columnconfigure(0,weight=1)

        title_label = ttk.Label(content_frame,text="Add Organisation Info")
        title_label.grid(row=0,column=0)

        ####### Mandatory Info
        mandatory_frame = ttk.Labelframe(content_frame,text="Mandatory Info")
        mandatory_frame.grid(column=0,row=1,sticky=(N,W,E,S))

        #ask for org name
        name_label = ttk.Label(mandatory_frame,text="Name: ")
        name_label.grid(row=1,column=0)
        self._org_name = StringVar()
        name_entry = ttk.Entry(mandatory_frame,textvariable=self._org_name)
        name_entry.grid(row=1,column=1)

        #########Optional
        #optional arguments: ORCID and affiliations
        optional_frame = ttk.Labelframe(content_frame,text="Optional")
        optional_frame.grid(column=0,row=2,sticky=(N,W,E,S))
        
        affiliation_label = ttk.Label(optional_frame,text="Affiliation(s): ")
        affiliation_label.grid(row=3,column=0)
        self._affiliation = StringVar()
        affiliation_entry = ttk.Entry(optional_frame,textvariable=self._affiliation)
        affiliation_entry.grid(row=3,column=1)

        self._id_type = StringVar()
        id_type_combobox = ttk.Combobox(optional_frame,
                                        textvariable=self._id_type,
                                        values=('ORCID',),
                                        state="readonly")
        id_type_combobox.grid(row=4,column=0)
        self.after(1, lambda: id_type_combobox.current(0))
        self._id = StringVar()
        id_entry = ttk.Entry(optional_frame,textvariable=id)
        id_entry.grid(row=4,column=1)

        submit_button = ttk.Button(content_frame,text="Submit",command=submit_function)
        submit_button.grid(row=10,column=0,pady=10)

    @property
    def name(self):
        return self._org_name.get()

    @property
    def affiliation(self):
        return self._affiliation.get()

    @property
    def id_type(self):
        return self._id_type.get()
    
    @property
    def id(self):
        return self._id.get()