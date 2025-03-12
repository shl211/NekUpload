import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from .create_author_window import CreateAuthorOrgWindow,CreateAuthorPersonWindow
from typing import Dict,List,Any
from NekUpload.newFrontend.components.settings_manager import SettingsManager
from NekUpload.newFrontend.components.scrollbox import ScrolledListbox
class UploadInfoFrame(ttk.Labelframe):
    def __init__(self,root,parent,setting_manager: SettingsManager):
        super().__init__(
            master=parent,
            text="Basic Upload Information",
            bootstyle=PRIMARY,
            padding=10
        )
        self.root = root
        self.setting_manager = setting_manager

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

        self.presets = ttk.Combobox(
            master=self,
            state="readonly"
        )
        self.presets.grid(row=0, column=1, padx=5, pady=5, sticky=EW)
        self.presets.bind("<<ComboboxSelected>>",self._update_community_slug_value)
        self.setting_manager.add_callbacks_on_update_host_name(self._update_community_slug_value)

        community_slug_label = ttk.Label(
            master=self,
            text="Community (URL Slug or UUID): ",
            bootstyle=PRIMARY
        )
        community_slug_label.grid(row=1,column=0,sticky=W)

        self._community_slug = tk.StringVar()
        self._community_slug.set("nektar")
        self.community_slug_entry = ttk.Entry(
            master=self,
            textvariable=self._community_slug
        )
        self.community_slug_entry.grid(row=1,column=1,padx=5,pady=5,sticky=EW)

        publication_date_label = ttk.Label(
            master=self,
            text="Publication Date: ",
            bootstyle=PRIMARY
        )
        publication_date_label.grid(row=2,column=0,sticky=EW)

        self.publication_date = tk.StringVar()
        self.date_entry = ttk.DateEntry(
            master=self,
            dateformat=r"%Y-%m-%d"
        )
        self.date_entry.grid(row=2,column=1,columnspan=1,padx=5,pady=5,sticky=EW)

        add_author_frame: ttk.Frame = self._add_authors_frame(self)
        add_author_frame.grid(row=3,column=0,sticky=NSEW,rowspan=2,columnspan=3)

        #update final value of combobox
        self._update_community_slug_value()

    def _add_authors_frame(self,parent) -> ttk.Frame:
        frame = ttk.Frame(
            master=parent
        )
        frame.columnconfigure(0,weight=1)
        frame.columnconfigure(1,weight=1)
        frame.columnconfigure(2,weight=1)

        #note that this mirrors self.author_listbox data in terms of order
        #should probably consolidate at some point
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

        #have a listbox to specify the creation
        self.author_listbox_frame = ScrolledListbox(frame)
        self.author_listbox = self.author_listbox_frame.listbox
        self.author_listbox_frame.grid(row=2,column=0,columnspan=2,rowspan=2,sticky=(NSEW))

        #add a delete button
        delete_button = ttk.Button(frame,text="Delete",command=self._delete_selected_author)
        delete_button.grid(row=4,column=1,padx=5,pady=5,sticky=NSEW)
        return frame

    def _delete_selected_author(self) -> None:
        """Delete the selected author from the list of authors. Deletion is accomplished via a Button connected to a Listbox.
        """
        selection_indices = self.author_listbox.curselection()
        if selection_indices:
            # 1. Get the items to delete *before* modifying the listbox
            items_to_delete = [self.author_listbox.get(index) for index in selection_indices]

            # 2. Delete from the listbox (reverse order to prevent issues with shifting indices)
            for index,item in zip(sorted(selection_indices, reverse=True),sorted(items_to_delete,reverse=True)):
                self.author_listbox.delete(index)

                #delete from self.authors using the index
                # self.authors should mirror same order as listbox
                try:
                    self.authors.pop(index)
                except ValueError:
                    print(f"Warning: Item '{item}' not found in self.authors")  # Handle potential mismatch

        print(self.authors)

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
        self.author_listbox.insert(END,f"{author_data['name']}")

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
        self.author_listbox.insert(END,f"{author_data['name']}")

        window.destroy()
    
    def _update_community_slug_value(self,event: tk.Event=None):
        """Callback for combobox selection, sets default values in some fields

        Args:
            event (Event): _description_
        """
        #update options based on database url
        database_name: str = self.setting_manager.database_name        
        if database_name == "AE Datastore":
            self.presets.configure(values=["Nektar++","Custom"])
        elif database_name == "InvenioRDM Demo":
            self.presets.configure(values=["NekUpload Demo","Custom"])
        else:
            self.presets.configure(values=["Custom"])
        
        if event:
            selected_value = event.widget.get()
        else:
            selected_value = self.presets.get()

        if database_name == "AE Datastore":
            if selected_value == "Nektar++":
                self._community_slug.set("nektar")#tbc
            else:
                self._community_slug.set("")
        elif database_name == "InvenioRDM Demo":
            if selected_value == "NekUpload Demo":
                self._community_slug.set("test_nekupload")
            else:
                self._community_slug.set("")
        else:
            self._community_slug.set("")

        #if not an event, then that means switched due to settings
        #hence, set a default config
        #brute force for now
        if not event:
            if database_name == "AE Datastore":
                self.presets.set("Nektar++")
                self._community_slug.set("nektar")
            elif database_name == "InvenioRDM Demo":
                self.presets.set("InvenioRDM Demo")
                self._community_slug.set("test_nekupload")
            else:
                self.presets.set("Custom")
                self._community_slug.set("")

    #Sets settings for default config
    def set_AE_db_default(self):
        """Set default settings for sending to AE database
        """
        self.host_url = "https://data.ae.ic.ac.uk"

    def set_default(self):
        """No default settings
        """
        self.host_url = ""

    @property
    def author_list(self) -> List[Dict[str,Any]]:
        """Read only access to list of authors

        Returns:
            List[Dict[str,Any]]: Dictionary containing information on authors
        """
        return self.authors
    
    @property
    def community_slug(self) -> str:
        return self._community_slug.get()
    
    @property
    def publication_date_iso(self) -> str:
        """Return in  format YYYY-MM-DD

        Returns:
            str: _description_
        """
        return self.date_entry.entry.get()