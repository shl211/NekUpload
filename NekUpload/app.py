from tkinter import *
from tkinter import filedialog
from tkinter import ttk #holds the more modern widgets
from datetime import date

from typing import List
from NekUpload.metadataModule import *
from NekUpload.uploadModule import invenioRDM
import os
from dotenv import load_dotenv

class NekUploadGUI:
    def __init__(self,root: Tk) -> None:
        self.root: Tk = root
        self.mainframe: ttk.Frame = self._create_mainframe()
        
        #static fields
        self.title: StringVar = StringVar()
        self.publication_date: StringVar = StringVar()

        self.is_read_user_guide: StringVar = StringVar()
        self.api_key_env_var: StringVar = StringVar()
        self.host_name: StringVar = StringVar()
        self.community_slug: StringVar = StringVar()

        #dynamic fields
        self.dirname: StringVar = StringVar()
        self.filenames: Variable = Variable()
        self.dir_label: ttk.Label = None #created in dynamic fields frame
        self.file_listbox: Listbox = None

        self.author_listbox: Listbox = None
        self.authors = []

        self.create_header_frame()
        self.create_static_fields_frame()
        self.create_dynamic_fields_frame()
        self.create_file_selector_frame()

        self.submit_button: ttk.Button = ttk.Button(self.mainframe, text="Submit", command=self.submit_form)
        self.submit_button.grid(row=6, column=1, sticky=E)

    def _create_mainframe(self) -> ttk.Frame:
        mainframe = ttk.Frame(self.root)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        return mainframe

    def create_header_frame(self) -> None: 
        header_frame: ttk.Frame = ttk.Frame(self.mainframe) 
        header_frame.grid(column=0, row=0, columnspan=2,sticky=(N, W, E, S))
        header_frame.columnconfigure(0, weight=1)
        header_frame.columnconfigure(1, weight=1)

        # add title and header
        style: ttk.Style = ttk.Style()
        style.configure("Header.TLabel", font=("Helvetica", 24, "bold"), underline=True)
        header: ttk.Label = ttk.Label(header_frame, text="Welcome to NekUpload", style="Header.TLabel")
        header.grid(column=0, row=0,columnspan=2,sticky=(N))

        # add some description/info for user
        description_text: str = "This is an interactive GUI upload and validation pipeline for Nektar++ datasets. " + \
            "Please complete the setup instructions found in the User Guide before proceeding [link]."
        description: ttk.Label = ttk.Label(header_frame, text=description_text,wraplength=600)
        description.grid(column=0, row=1,columnspan=2,sticky=N)

    def create_static_fields_frame(self) -> None:
        static_fields_frame: ttk.Labelframe = ttk.Labelframe(self.mainframe,text="Basic Info")
        static_fields_frame.grid(column=0, row=1, sticky=(N, W, E, S))

        #tick box to serve as reminder for user to set host name environment variable
        read_user_info_check: ttk.Checkbutton = ttk.Checkbutton(static_fields_frame,text="Have you read User Guide for setting up environment variables?",
                                       command=None,variable=self.is_read_user_guide,
                                       onvalue="True",offvalue="False")
        read_user_info_check.grid(row=0,column=0,sticky=W,padx=5,pady=.5)

        #ask user for what the environment variables are for the api key
        api_key_env_label = ttk.Label(static_fields_frame,text="Environment Variable for API Key: ")
        api_key_env_label.grid(row=1,column=0,sticky=W,padx=5,pady=.5)
        api_key_entry = ttk.Entry(static_fields_frame,textvariable=self.api_key_env_var)
        api_key_entry.grid(row=1,column=1,sticky=E,padx=5,pady=.5)

        #ask user for host name
        host_label = ttk.Label(static_fields_frame,text="Host Name URL: ")
        host_label.grid(row=2,column=0,sticky=W,padx=5,pady=.5)
        host_name_entry = ttk.Entry(static_fields_frame,textvariable=self.host_name)
        host_name_entry.grid(row=2,column=1,sticky=E,padx=5,pady=.5)

        #ask user for community url slug
        community_label = ttk.Label(static_fields_frame,text="Community (URL slug or UUID): ")
        community_label.grid(row=3,column=0,sticky=W,padx=5,pady=.5)
        community_entry = ttk.Entry(static_fields_frame,textvariable=self.community_slug)
        community_entry.grid(row=3,column=1,sticky=E,padx=5,pady=.5)

        #ask for title of the dataset
        title_label: ttk.Label = ttk.Label(static_fields_frame, text="Title: ")
        title_label.grid(row=4, column=0, sticky=W, padx=5, pady=.5)
        title_widget: ttk.Entry = ttk.Entry(static_fields_frame, textvariable=self.title) 
        title_widget.grid(row=4, column=1, sticky=E, padx=5, pady=.5)

        #ask for publication date, pre-populate with current date
        publication_date_label: ttk.Label = ttk.Label(static_fields_frame, text="Publication Date: ") 
        publication_date_label.grid(row=5, column=0, sticky=W, padx=5, pady=.5)
        self.publication_date.set(self._get_current_iso8601_date())  
        publication_date_widget: ttk.Entry = ttk.Entry(static_fields_frame, textvariable=self.publication_date) 
        publication_date_widget.grid(row=5, column=1, sticky=E, padx=5, pady=.5)

    def _get_current_iso8601_date(self) -> str:
        today: date = date.today() 
        return today.isoformat()

    def create_dynamic_fields_frame(self) -> None:
        dynamic_fields_frame: ttk.LabelFrame = ttk.LabelFrame(self.mainframe,text="Author(s)")  
        dynamic_fields_frame.grid(column=1, row=1, rowspan=2, sticky=(N,S))

        # Configure row weights in the MAIN frame
        self.mainframe.grid_rowconfigure(1, weight=1)
        self.mainframe.grid_rowconfigure(2, weight=1)
        self.mainframe.grid_columnconfigure(1, weight=1)

        #allow addition of author as a person
        create_author_person_button: ttk.Button = ttk.Button(dynamic_fields_frame,text="Add Person",command=self._create_author_person)
        create_author_person_button.grid(row=0,column=0,sticky=W)

        #allow additiong of author as an organisation
        create_author_org_button: ttk.Button = ttk.Button(dynamic_fields_frame,text="Add Org",command=self._create_author_org)
        create_author_org_button.grid(row=0,column=1,sticky=W)

        #have a listbox to specify the creation
        self.author_listbox: Listbox = Listbox(dynamic_fields_frame,selectmode=EXTENDED)
        scrollbar_y: Scrollbar = Scrollbar(dynamic_fields_frame,command=self.author_listbox.yview)
        scrollbar_x: Scrollbar = Scrollbar(dynamic_fields_frame,command=self.author_listbox.xview,orient=HORIZONTAL)
        self.author_listbox.config(yscrollcommand=scrollbar_y.set,xscrollcommand=scrollbar_x)
        scrollbar_y.config(command=self.author_listbox.yview)
        scrollbar_x.config(command=self.author_listbox.xview)

        self.author_listbox.grid(row=1,column=0,columnspan=2,sticky=(N,S))
        scrollbar_x.grid(row=2,column=0,columnspan=2,sticky=(W,E))
        scrollbar_y.grid(row=1,column=2,sticky=(N,S))

        #add a delete button
        delete_button = ttk.Button(dynamic_fields_frame,text="Delete",command=self._delete_selected_author)
        delete_button.grid(row=3,column=1)

    def _delete_selected_author(self) -> None:
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
        new_window = Toplevel(self.root)
        new_window.title("Specify Author Information") 
        new_window.grid_rowconfigure(0,weight=1)
        new_window.grid_columnconfigure(0,weight=1)

        content_frame = ttk.Frame(new_window,padding=20)
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
        given_name = StringVar()
        given_name_entry = ttk.Entry(mandatory_frame,textvariable=given_name)
        given_name_entry.grid(row=1,column=1)

        #ask for last name
        last_name_label = ttk.Label(mandatory_frame,text="Last Name: ")
        last_name_label.grid(row=2,column=0)
        last_name = StringVar()
        last_name_entry = ttk.Entry(mandatory_frame,textvariable=last_name)
        last_name_entry.grid(row=2,column=1)

        #########Optional
        #optional arguments: ORCID and affiliations
        optional_frame = ttk.Labelframe(content_frame,text="Optional")
        optional_frame.grid(column=0,row=2,sticky=(N,W,E,S))
        
        affiliation_label = ttk.Label(optional_frame,text="Affiliation(s): ")
        affiliation_label.grid(row=3,column=0)
        affiliation = StringVar()
        affiliation_entry = ttk.Entry(optional_frame,textvariable=affiliation)
        affiliation_entry.grid(row=3,column=1)

        id_type = StringVar()
        id_type_combobox = ttk.Combobox(optional_frame,
                                        textvariable=id_type,
                                        values=('ORCID',),
                                        state="readonly")
        id_type_combobox.grid(row=4,column=0)
        new_window.after(1, lambda: id_type_combobox.current(0))
        id = StringVar()
        id_entry = ttk.Entry(optional_frame,textvariable=id)
        id_entry.grid(row=4,column=1)

        author_data = {}
        def submit_author_info():
            author_data['type'] = 'personal'
            author_data['given_name'] = given_name_entry.get()
            author_data['last_name'] = last_name.get()
            author_data['name'] = f"{author_data['given_name']} {author_data['last_name']}"
            author_data['affiliation'] = affiliation_entry.get()
            author_data['id_type'] = id_type.get()
            author_data['id'] = id_entry.get()

            print("Author Data: ", author_data)

            self.authors.append(author_data)
            self.author_listbox.insert(END,f"{author_data['name']}")
            
            new_window.destroy()

        submit_button = ttk.Button(content_frame,text="Submit",command=submit_author_info)
        submit_button.grid(row=10,column=0,pady=10)

    def _create_author_org(self) -> None:
        new_window = Toplevel(self.root)
        new_window.title("Specify Author Information") 
        new_window.grid_rowconfigure(0,weight=1)
        new_window.grid_columnconfigure(0,weight=1)

        content_frame = ttk.Frame(new_window,padding=20)
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
        name = StringVar()
        name_entry = ttk.Entry(mandatory_frame,textvariable=name)
        name_entry.grid(row=1,column=1)

        #########Optional
        #optional arguments: ORCID and affiliations
        optional_frame = ttk.Labelframe(content_frame,text="Optional")
        optional_frame.grid(column=0,row=2,sticky=(N,W,E,S))
        
        affiliation_label = ttk.Label(optional_frame,text="Affiliation(s): ")
        affiliation_label.grid(row=3,column=0)
        affiliation = StringVar()
        affiliation_entry = ttk.Entry(optional_frame,textvariable=affiliation)
        affiliation_entry.grid(row=3,column=1)

        id_type = StringVar()
        id_type_combobox = ttk.Combobox(optional_frame,
                                        textvariable=id_type,
                                        values=('ORCID',),
                                        state="readonly")
        id_type_combobox.grid(row=4,column=0)
        new_window.after(1, lambda: id_type_combobox.current(0))
        id = StringVar()
        id_entry = ttk.Entry(optional_frame,textvariable=id)
        id_entry.grid(row=4,column=1)

        author_data = {}
        def submit_author_info():
            author_data['type'] = 'organizational'
            author_data['name'] = name.get()
            author_data['affiliation'] = affiliation_entry.get()
            author_data['id_type'] = id_type.get()
            author_data['id'] = id_entry.get()

            print("Author Data: ", author_data)

            self.authors.append(author_data)
            self.author_listbox.insert(END,f"{author_data['name']}")
            
            new_window.destroy()

        submit_button = ttk.Button(content_frame,text="Submit",command=submit_author_info)
        submit_button.grid(row=10,column=0,pady=10)

    def _create_directory_upload_frame(self,parent:ttk.Frame) -> ttk.Frame:
        file_selector_frame: ttk.Frame = ttk.Frame(parent) 
        file_selector_frame.grid(column=0, row=2, columnspan=2, sticky=(N,E,S,W))

        find_dir_button: ttk.Button = ttk.Button(
            file_selector_frame,
            text="Select Directory",
            command=self._select_directory
        )
        find_dir_button.grid(column=0, row=0, sticky=W)

        self.dir_label: ttk.Label = ttk.Label(file_selector_frame,text=f"Selected Directory: None")
        self.dir_label.grid(column=1,row=0,sticky=W)

        return file_selector_frame

    def _clear_directory_upload_frame(self,frame: ttk.Frame) -> None:
        #reset widgets
        for widget in frame.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.config(text="Selected Directory: None")

        #reset states
        self.dirname.set("")

    def _clear_files_upload_frame(self,frame: ttk.Frame) -> None:
        for widget in frame.winfo_children():
            if isinstance(widget, Listbox):
                widget.delete(0,END)

        #reset states
        self.filenames = ()

    def _create_files_upload_frame(self,parent:ttk.Frame) -> ttk.Frame:
        file_selector_frame: ttk.Frame = ttk.Frame(parent) 
        file_selector_frame.grid(column=0, row=2, columnspan=2, sticky=(N,E,S,W))

        # Configure grid weights for the frame's columns and rows
        file_selector_frame.grid_rowconfigure(0, weight=1)  # Row with Listbox expands
        file_selector_frame.grid_columnconfigure(2, weight=1)  # Column with Listbox expands

        find_files_button: ttk.Button = ttk.Button(
            file_selector_frame,
            text="Select Files",
            command=self._select_files_listbox
        )
        find_files_button.grid(column=0, row=0, sticky=W)

        #set up list box with scroller for displaying files
        self.file_listbox: Listbox = Listbox(file_selector_frame,selectmode=EXTENDED)
        scrollbar: Scrollbar = Scrollbar(file_selector_frame,command=self.file_listbox.yview)
        scrollbar_horizontal: Scrollbar = Scrollbar(file_selector_frame,command=self.file_listbox.xview,orient=HORIZONTAL) #help view full path 
        self.file_listbox.config(yscrollcommand=scrollbar.set,xscrollcommand=scrollbar_horizontal.set)
        scrollbar.config(command=self.file_listbox.yview)
        scrollbar_horizontal.config(command=self.file_listbox.xview)
        self.file_listbox.grid(row=0,column=2,sticky=(N,S,E,W))
        scrollbar.grid(row=0,column=3,sticky=(N,S))
        scrollbar_horizontal.grid(row=1,column=2,sticky=(W,E))

        return file_selector_frame

    def create_file_selector_frame(self) -> None:
        n: ttk.Notebook = ttk.Notebook(self.mainframe)
        f1 = self._create_directory_upload_frame(n)
        f2 = self._create_files_upload_frame(n)
        n.add(f1,text="Upload by Directory")
        n.add(f2,text="Upload by Files")
        n.grid(row=2,column=0,sticky=(E,W))

        #clear states if switching between tabs to ensure consistency
        def on_tab_change(event: Event):
            selected_tab = event.widget.select()
            tab_index = event.widget.index(selected_tab)

            if tab_index == 0: #upload by directory tab
                self._clear_directory_upload_frame(f1)
            elif tab_index == 1: #upload by files tab
                self._clear_files_upload_frame(f2)

        n.bind("<<NotebookTabChanged>>",on_tab_change)

    def _select_directory(self) -> None:
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.dirname.set(selected_dir)
            self.dir_label.config(text=f"Selected Directory: {selected_dir}")  # Update text
            print(f"dirname.get(): {self.dirname.get()}")
        else:
            self.dirname.set("")
            self.dir_label.config(text="Selected Directory: None")  # Update text
            print("No directory selected")
    
    def _select_files_listbox(self) -> None:
            selected_files = filedialog.askopenfilenames(title="Select Files",
                                                filetypes=(("Nektar Files",("*.xml","*.nekg","*.fld","*.fce","*.chk"),),
                                                ("Supporting Files",("*.pdf","*.png","*.jpg",".jpegs")),
                                                ("All Files","*.*"),),    
                                            )

            #insert files in listbox
            self.filenames = selected_files
            if selected_files:
                self.file_listbox.delete(0,END)
                for file in selected_files:
                    self.file_listbox.insert(END,file)
                print(f"filenames.get(): {self.filenames}")
            else:
                self.filenames=()
                print("No Files Selected")

    def submit_form(self) -> None: 
        
        is_read_user_guide = self.is_read_user_guide.get()
        if not is_read_user_guide or is_read_user_guide == "False":
            print("ERROR")
            return
        print(is_read_user_guide)

        title: str = self.title.get()
        publication_date: str = self.publication_date.get()
        
        #ASSIGN USERS
        author_list: List[InvenioOrgInfo | InvenioPersonInfo] = []
        for author in self.authors:
            author_info: InvenioOrgInfo | InvenioPersonInfo = None
            
            if author["type"] == "personal":
                given_name = author["given_name"]
                last_name = author["last_name"]
                author_info = InvenioPersonInfo(given_name,last_name)
            elif author["type"] == "organizational":
                name = author["name"]
                author_info = InvenioOrgInfo(name)

            if author["id"] != "":
                mapping = {"ORCID" : IdentifierType.ORCID}
                id = Identifier(author["id"],mapping[author["id_type"]])
                author_info.add_identifier(id)
                
            #also affiliations, but not supported in backend for now
            author_list.append(author_info)

        #create metadata
        metadata = InvenioMetadata(title,publication_date,author_list,"dataset")
        metadata.add_publisher("NekUpload App")
        metadata.add_description("This was uploaded via NekUpload app")
        metadata_payload = metadata.get_metadata_payload()
        metadata_json = {"metadata": metadata_payload}
        print(metadata_json)

        #only one of the following is not empty
        dirname = self.dirname.get()
        file_list = [self.file_listbox.get(i) for i in range(self.file_listbox.size())]

        #first see if dirname is empty, if not, use directory to upload
        upload_manager = invenioRDM()
        
        URL = self.host_name.get()
        COMMUNITY_SLUG = self.community_slug.get()
        API_KEY_ENV_VAR = self.api_key_env_var.get()

        load_dotenv()
        if dirname:
            files_to_upload = [os.path.join(dirname, f) for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f))]
            upload_manager.upload_files(URL,os.getenv(API_KEY_ENV_VAR,None),files_to_upload,metadata_json,COMMUNITY_SLUG)
        elif file_list:
            upload_manager.upload_files(URL,os.getenv(API_KEY_ENV_VAR,None),file_list,metadata_json,COMMUNITY_SLUG)
        else:
            print("Failed to upload as no files detected")

def main() -> None:
    root: Tk = Tk() 
    app: NekUploadGUI = NekUploadGUI(root)
    root.title("NekUpload")
    root.mainloop()

if __name__ == "__main__":
    main()