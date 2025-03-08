import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from typing import Callable
from types import MappingProxyType

class Menu(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)

        self.columnconfigure(0,weight=1)

        self.info_btn = ttk.Button(
            master = self,
            text = "Info",
            compound=TOP,
            bootstyle=INFO
        )
        self.info_btn.grid(row=0,column=0,padx=10,pady=10,sticky=NSEW)

        self.upload_btn = ttk.Button(
            master = self,
            text = "Upload",
            compound=TOP,
            bootstyle=INFO
        )
        self.upload_btn.grid(row=1,column=0,padx=10,pady=10,sticky=NSEW)

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

        self.button_map: MappingProxyType[str,ttk.Button] = MappingProxyType({
                                                            "INFO": self.info_btn,
                                                            "UPLOAD": self.upload_btn,
                                                            "REVIEW": review_btn,
                                                            "EXPLORE": explore_btn,
                                                            "HELP": help_btn})

    def add_link_to_button(self,button: str, on_click_command: Callable):
        """Add a on click command to a button. Available buttons are "INFO","UPLOAD","REVIEW","EXPLORE","HELP"

        Args:
            button (str): Available buttons "INFO","UPLOAD","EXPLORE","HELP","REVIEW"
            on_click_command (Callable): _description_
        """
        self.button_map[button].config(command=on_click_command)