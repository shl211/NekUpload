import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class Menu(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)

        self.columnconfigure(0,weight=1)

        info_btn = ttk.Button(
            master = self,
            text = "Info",
            compound=TOP,
            bootstyle=INFO
        )
        info_btn.grid(row=0,column=0,padx=10,pady=10,sticky=NSEW)

        upload_btn = ttk.Button(
            master = self,
            text = "Upload",
            compound=TOP,
            bootstyle=INFO
        )
        upload_btn.grid(row=1,column=0,padx=10,pady=10,sticky=NSEW)

        review_btn = ttk.Button(
            master = self,
            text = "Review",
            compound=TOP,
            bootstyle=INFO
        )
        review_btn.grid(row=2,column=0,padx=10,pady=10,sticky=NSEW)

        explore_btn = ttk.Button(
            master = self,
            text = "Explore",
            compound=TOP,
            bootstyle=INFO
        )
        explore_btn.grid(row=3,column=0,padx=10,pady=10,sticky=NSEW)

        help_btn = ttk.Button(
            master = self,
            text = "Help",
            compound=TOP,
            bootstyle=INFO
        )
        help_btn.grid(row=4,column=0,padx=10,pady=10,sticky=NSEW)