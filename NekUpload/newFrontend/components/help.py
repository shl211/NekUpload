import tkinter as tk
from ttkbootstrap.icons import Icon
import ttkbootstrap as ttk

class HelpNotification(ttk.Label):
    def __init__(self,parent):
        self.img = tk.PhotoImage(data=Icon.question)
        super().__init__(master=parent,
                        image=self.img,
                        anchor="center")



