import ttkbootstrap as ttk
from ttkbootstrap.constants import *
class InfoScene(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)

        self.placeholder = ttk.Label(
            master=self,  # Ensure label is inside this frame
            text="PLACEHOLDER",
            font=("TkDefaultFont", 20),  # Make text larger for visibility
            anchor="center"  # Center text inside the label
        )

        self.placeholder.grid(row=1,column=1,sticky=(NSEW))
        