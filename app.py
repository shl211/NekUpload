from tkinter import *
from tkinter import filedialog
from tkinter import ttk #holds the more modern widgets
from datetime import date

class NekUploadGUI:
    def __init__(self,root: Tk) -> None:
        self.root: Tk = root
        self.mainframe: ttk.Frame = self._create_mainframe()
        
        #static fields
        self.title: StringVar = StringVar()
        self.publication_date: StringVar = StringVar()
        self.is_api_key_exist: StringVar = StringVar()
        self.is_host_name_exist: StringVar = StringVar()

        #dynamic fields
        self.dirname: StringVar = StringVar()
        self.filenames: Variable = Variable()
        self.dir_label: ttk.Label = None #created in dynamic fields frame
        self.file_listbox: Listbox = None

        self.create_header_frame()
        self.create_static_fields_frame()
        self.create_dynamic_fields_frame()
        self.create_file_selector_frame()

        self.submit_button: ttk.Button = ttk.Button(self.mainframe, text="Submit", command=self.submit_form)
        self.submit_button.grid(row=5, column=1, sticky=E)

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

        #tick box to serve as reminder for user to set API key environment variable
        api_key_check: ttk.Checkbutton = ttk.Checkbutton(static_fields_frame,text="Have you set environment variable NEKTAR_DB_API_KEY?",
                                       command=None,variable=self.is_api_key_exist,
                                       onvalue="True",offvalue="False",
                                       )
        api_key_check.grid(row=1,column=0,sticky=W,padx=5,pady=.5)

        #tick box to serve as reminder for user to set host name environment variable
        host_name_check: ttk.Checkbutton = ttk.Checkbutton(static_fields_frame,text="Have you set environment variable NEKTAR_DB_HOST?",
                                       command=None,variable=self.is_host_name_exist,
                                       onvalue="True",offvalue="False")
        host_name_check.grid(row=2,column=0,sticky=W,padx=5,pady=.5)

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
        dynamic_fields_frame.grid(column=1, row=1, sticky=(N,S))

        #allow addition of author as a person
        create_author_person_button: ttk.Button = ttk.Button(dynamic_fields_frame,text="Create Person",command=self._create_author_person)
        create_author_person_button.grid(row=0,column=0,sticky=W)

        #allow additiong of author as an organisation
        create_author_org_button: ttk.Button = ttk.Button(dynamic_fields_frame,text="Create Org",command=self._create_author_org)
        create_author_org_button.grid(row=0,column=1,sticky=W)

    def _create_author_person(self) -> None:
        print("Create Person")
    
    def _create_author_org(self) -> None:
        print("Create Organisation")

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
        self.file_listbox: Listbox = Listbox(file_selector_frame,selectmode=MULTIPLE)
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
        n.grid(row=5,column=0,sticky=(E,W))

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

    def _select_files(self) -> None:
        selected_files = filedialog.askopenfilenames(title="Select Files",
                                                filetypes=(("Nektar Files",("*.xml","*.nekg","*.fld","*.fce","*.chk"),),
                                                ("Supporting Files",("*.pdf","*.png","*.jpg",".jpegs")),
                                                ("All Files","*.*"),),    
                                            )
        
        if selected_files:
            self.filenames = selected_files
            formatted_filenames = "\n".join(selected_files) # Format to multiple lines
            self.files_label.config(text=f"Selected Files:\n{formatted_filenames}")
        else:
            self.filenames = ()
            self.files_label.config(text="Selected Files: None")  # Update text
            print("No Files selected")

    def submit_form(self) -> None: 
        print(self.title.get()) 
        print(self.publication_date.get())
        print(self.dirname.get())

def main() -> None:
    root: Tk = Tk() 
    app: NekUploadGUI = NekUploadGUI(root)
    root.title("NekUpload")
    root.mainloop()

if __name__ == "__main__":
    main()