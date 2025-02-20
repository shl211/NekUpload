from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from typing import List, Tuple

class FileSelectorNotebookFrame(ttk.Notebook):
    def __init__(self,parent: ttk.Frame):
        super().__init__(parent)

        self.file_types = {
            "Session": FileType("Session Files",["*.xml"]),
            "Geometry": FileType("Geometry Files",["*.nekg"]),
            "Output": FileType("Output Files",["*.fld"]),
            "Checkpoint": FileType("Checkpoint Files",["*.chk"]),
            "Filter": FileType("Filter Files", ["*.fce"]),
            "Supporting": FileType("Supporting Files", ["*.pdf",".jpg","*.jpeg","*.png"])
        }

        self.session_frame = FileSelectorFrame(self,self.file_types["Session"])
        self.add(self.session_frame,text="Session")

        self.geometry_frame = FileSelectorFrame(self,self.file_types["Geometry"])
        self.add(self.geometry_frame,text="Geometry")

        self.output_frame = FileSelectorFrame(self,self.file_types["Output"])
        self.add(self.output_frame,text="Output")

        self.checkpoint_frame = FileSelectorFrame(self,self.file_types["Checkpoint"])
        self.add(self.checkpoint_frame,text="Checkpoint")
        
        self.filter_frame = FileSelectorFrame(self,self.file_types["Filter"])
        self.add(self.filter_frame,text="Filter")

        self.supporting_frame = FileSelectorFrame(self,self.file_types["Supporting"])
        self.add(self.supporting_frame, text="Supporting")
        

    @property
    def session_file_list(self) -> List[str]:
        return self.session_frame.file_list

    @property
    def geometry_file_list(self) -> List[str]:
        return self.geometry_frame.file_list
    
    @property
    def output_file_list(self) -> List[str]:
        return self.output_frame.file_list

    @property
    def output_file_list(self) -> List[str]:
        return self.output_frame.file_list

    @property
    def checkpoint_file_list(self) -> List[str]:
        return self.checkpoint_frame.file_list

    @property
    def filter_file_list(self) -> List[str]:
        return self.filter_frame.file_list
    
    @property
    def supporting_file_list(self) -> List[str]:
        return self.supporting_frame.file_list

    def get_file_list(self) -> List[str]:
        return self.session_file_list + self.geometry_file_list + self.output_file_list + \
                self.checkpoint_file_list + self.filter_file_list + self.supporting_file_list

class FileSelectorFrame(ttk.Frame):
    def __init__(self,parent: ttk.Frame,file_type: 'FileType'):
        super().__init__(parent)
        self.file_type = file_type

        self.grid_rowconfigure(0, weight=1)  # Row with Listbox expands
        self.grid_columnconfigure(2, weight=1)  # Column with Listbox expands

        find_files_button = ttk.Button(self,text="Select Files",command=self._select_files_listbox)
        find_files_button.grid(column=0,row=0,sticky=W)

        #set up list box with scroller for displaying files
        self.file_listbox: Listbox = Listbox(self,selectmode=EXTENDED)
        scrollbar: Scrollbar = Scrollbar(self,command=self.file_listbox.yview)
        scrollbar_horizontal: Scrollbar = Scrollbar(self,command=self.file_listbox.xview,orient=HORIZONTAL) #help view full path 
        self.file_listbox.config(yscrollcommand=scrollbar.set,xscrollcommand=scrollbar_horizontal.set)
        scrollbar.config(command=self.file_listbox.yview)
        scrollbar_horizontal.config(command=self.file_listbox.xview)
        self.file_listbox.grid(row=0,column=2,sticky=(N,S,E,W))
        scrollbar.grid(row=0,column=3,sticky=(N,S))
        scrollbar_horizontal.grid(row=1,column=2,sticky=(W,E))

    def _select_files_listbox(self) -> None:
            filetype = self.file_type.get_filetype()
            """
            selected_files = filedialog.askopenfilenames(title="Select Files",
                                                filetypes=(("Nektar Files",("*.xml","*.nekg","*.fld","*.fce","*.chk"),),
                                                ("Supporting Files",("*.pdf","*.png","*.jpg",".jpegs")),
                                                ("All Files","*.*"),),    
                                         )
            """
            selected_files = filedialog.askopenfilenames(title="Select Files",
                                                filetypes=(filetype,),    
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

class FileType:
    def __init__(self,name: str,extensions: List[str]):
        self.name = name
        self.extensions = extensions

    def get_filetype(self) -> Tuple[str, Tuple[str, ...]]:
        return (self.name,tuple(self.extensions))