from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from typing import List 

class FileSelectorNotebookFrame(ttk.Notebook):
    def __init__(self,parent: ttk.Frame):
        super().__init__(parent)

        #member variables
        self._dirname: StringVar = StringVar()
        self.filenames: Variable = Variable()
        self.dir_label: ttk.Label = None #created in dynamic fields frame
        self.file_listbox: Listbox = None

        f2 = self._create_files_upload_frame(self)
        self.add(f2,text="Upload by Files")

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
    
    @property
    def file_list(self) -> List[str]:
        return [self.file_listbox.get(i) for i in range(self.file_listbox.size())]

    