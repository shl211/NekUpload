from tkinter import *
from tkinter import filedialog
from tkinter import ttk #holds the more modern widgets
from datetime import date

class NekUploadGUI:
    def __init__(self,root: Tk) -> None:
        self.root: Tk = root
        self.mainframe: ttk.Frame = self._create_mainframe()
        self.title: StringVar = StringVar()
        self.publication_date: StringVar = StringVar()
        self.dirname: StringVar = StringVar()

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

        style: ttk.Style = ttk.Style()
        style.configure("Header.TLabel", font=("Helvetica", 24, "bold"), underline=True)

        header: ttk.Label = ttk.Label(header_frame, text="Welcome to NekUpload", style="Header.TLabel")
        header.grid(column=0, row=0, sticky=N)

        description_text: str = "This is an interactive GUI upload and validation pipeline for Nektar++ datasets. " + \
            "Please complete the setup instructions found in the User Guide before proceeding [link]."

        description: ttk.Label = ttk.Label(header_frame, text=description_text,wraplength=500)
        description.grid(column=0, row=1,sticky=W)

    def create_static_fields_frame(self) -> None:
        static_fields_frame: ttk.Frame = ttk.Frame(self.mainframe)
        static_fields_frame.grid(column=0, row=1, sticky=(N, W, E, S))

        static_fields_header: ttk.Label = ttk.Label(static_fields_frame, text="Dataset Metadata")
        static_fields_header.grid(column=0, row=0, columnspan=2, sticky=N)

        title_label: ttk.Label = ttk.Label(static_fields_frame, text="Title: ")
        title_label.grid(row=1, column=0, sticky=W, padx=5, pady=.5)

        title_widget: ttk.Entry = ttk.Entry(static_fields_frame, textvariable=self.title) 
        title_widget.grid(row=1, column=1, sticky=E, padx=5, pady=.5)

        publication_date_label: ttk.Label = ttk.Label(static_fields_frame, text="Publication Date: ") 
        publication_date_label.grid(row=2, column=0, sticky=W, padx=5, pady=.5)

        self.publication_date.set(self._get_current_iso8601_date())  
        publication_date_widget: ttk.Entry = ttk.Entry(static_fields_frame, textvariable=self.publication_date) 
        publication_date_widget.grid(row=2, column=1, sticky=E, padx=5, pady=.5)

    def _get_current_iso8601_date(self) -> str:
        today: date = date.today() 
        return today.isoformat()

    def create_dynamic_fields_frame(self) -> None:
        dynamic_fields_frame: ttk.Frame = ttk.Frame(self.mainframe)  
        dynamic_fields_frame.grid(column=1, row=1, sticky=(E))

        placeholder_label: ttk.Label = ttk.Label(dynamic_fields_frame, text="PLACEHOLDER") 
        placeholder_label.grid(row=0, column=0, sticky=W)

    def create_file_selector_frame(self) -> None:
        file_selector_frame: ttk.Frame = ttk.Frame(self.mainframe) 
        file_selector_frame.grid(column=0, row=2, columnspan=2, sticky=S)

        file_header_label: ttk.Label = ttk.Label(file_selector_frame, text="Select Dataset")
        file_header_label.grid(column=0, row=0, sticky=N)

        dir_label: ttk.Label = ttk.Label(file_selector_frame,text="Selected Directory",textvariable=self.dirname)
        dir_label.grid(column=0,row=1,sticky=W)

        find_dir_button: ttk.Button = ttk.Button(
            file_selector_frame,
            text="Select Directory",
            command=lambda: (self.dirname.set(filedialog.askdirectory()), print(f"dirname.get(): {self.dirname.get()}")) #
        )
        find_dir_button.grid(column=0, row=0, sticky=W)

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