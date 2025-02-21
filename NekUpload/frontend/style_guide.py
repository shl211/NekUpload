from tkinter import ttk
from typing import Dict

def get_styles() -> ttk.Style:
    style = ttk.Style()
    style.configure("Error.TEntry",
                    fieldbackground="lightcoral",  # Always red
                    borderwidth=2,
                    relief="solid",
                    foreground="black")
    
    return style

def highlight_mandatory_entry_on_focus_out(entry: ttk.Entry):
    style = get_styles()
    if entry.get():
        entry.config(style="TEntry")
    else:
        entry.config(style="Error.TEntry")

def highlight_mandatory_entry_on_focus_in(entry: ttk.Entry):
    style = get_styles()
    entry.config(style="TEntry")

def show_error_in_entry(entry: ttk.Entry):
    style = get_styles()
    entry.config(style="Error.TEntry")

