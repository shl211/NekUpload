import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame

class InfoScene(ScrolledFrame):
    def __init__(self,parent):
        super().__init__(parent,autohide=True)

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)

        LEFT_MARGIN = 5

        about_label = ttk.Label(
            master = self,
            text = "What is NekUpload?",
            font=("TkDefaultFont", 20, "bold", "underline"),
            anchor="center"
        )
        about_label.grid(row=0,column=0,pady=LEFT_MARGIN,padx=5,sticky=W)

        about_description = ttk.Label(
            master = self,
            text="This is a long description text that will automatically wrap when the window is resized. "
                "It will adjust to the width of the window, providing a clean and responsive layout.",
                anchor="w",
                justify="left",
                #wraplength=300
                )
        about_description.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
