import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class Header(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)

        self.columnconfigure(0,weight=1)

        logo_text = ttk.Label(
            master = self,
            text = "NekUpload",
            font = ("TkDefaultFixed",30)
        )

        logo_text.grid(row=0,column=0)