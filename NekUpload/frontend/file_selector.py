from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from typing import List 

class FileSelectorNotebookFrame(ttk.Notebook):
    def __init__(self,parent: ttk.Frame):
        super().__init__(parent)

        #member variables
        self.dirname_temp: StringVar = StringVar()
        self.filenames_temp: Variable = Variable()
        self.dir_label: ttk.Label = None #created in dynamic fields frame
        self.file_listbox_temp: Listbox = None

        #create the upload frame
        f1 = self._create_directory_upload_frame(self)
        f2 = self._create_files_upload_frame(self)

        self.add(f1,text="Upload by Directory")
        self.add(f2,text="Upload by Files")
      
        #clear states if switching between tabs to ensure consistency
        def on_tab_change(event: Event):
            selected_tab = event.widget.select()
            tab_index = event.widget.index(selected_tab)

            if tab_index == 0: #upload by directory tab
                self._clear_directory_upload_frame(f1)
            elif tab_index == 1: #upload by files tab
                self._clear_files_upload_frame(f2)

        self.bind("<<NotebookTabChanged>>",on_tab_change)

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
        self.dirname_temp.set("")

    def _clear_files_upload_frame(self,frame: ttk.Frame) -> None:
        for widget in frame.winfo_children():
            if isinstance(widget, Listbox):
                widget.delete(0,END)

        #reset states
        self.filenames_temp = ()

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
        self.file_listbox_temp: Listbox = Listbox(file_selector_frame,selectmode=EXTENDED)
        scrollbar: Scrollbar = Scrollbar(file_selector_frame,command=self.file_listbox_temp.yview)
        scrollbar_horizontal: Scrollbar = Scrollbar(file_selector_frame,command=self.file_listbox_temp.xview,orient=HORIZONTAL) #help view full path 
        self.file_listbox_temp.config(yscrollcommand=scrollbar.set,xscrollcommand=scrollbar_horizontal.set)
        scrollbar.config(command=self.file_listbox_temp.yview)
        scrollbar_horizontal.config(command=self.file_listbox_temp.xview)
        self.file_listbox_temp.grid(row=0,column=2,sticky=(N,S,E,W))
        scrollbar.grid(row=0,column=3,sticky=(N,S))
        scrollbar_horizontal.grid(row=1,column=2,sticky=(W,E))

        return file_selector_frame

    def _select_directory(self) -> None:
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.dirname_temp.set(selected_dir)
            self.dir_label.config(text=f"Selected Directory: {selected_dir}")  # Update text
            print(f"dirname.get(): {self.dirname_temp.get()}")
        else:
            self.dirname_temp.set("")
            self.dir_label.config(text="Selected Directory: None")  # Update text
            print("No directory selected")
    
    def _select_files_listbox(self) -> None:
            selected_files = filedialog.askopenfilenames(title="Select Files",
                                                filetypes=(("Nektar Files",("*.xml","*.nekg","*.fld","*.fce","*.chk"),),
                                                ("Supporting Files",("*.pdf","*.png","*.jpg",".jpegs")),
                                                ("All Files","*.*"),),    
                                            )

            #insert files in listbox
            self.filenames_temp = selected_files
            if selected_files:
                self.file_listbox_temp.delete(0,END)
                for file in selected_files:
                    self.file_listbox_temp.insert(END,file)
                print(f"filenames.get(): {self.filenames_temp}")
            else:
                self.filenames_temp=()
                print("No Files Selected")

    @property
    def dirname(self) -> str:
        return self.dirname_temp.get()
    
    @property
    def file_list(self) -> List[str]:
        return [self.file_listbox_temp.get(i) for i in range(self.file_listbox_temp.size())]

    