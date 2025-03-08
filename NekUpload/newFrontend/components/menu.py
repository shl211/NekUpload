import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from typing import Callable, Dict

class Menu(ttk.Frame):
    """A menu frame with buttons for various actions."""

    def __init__(self, parent):
        """Initializes the Menu frame."""
        super().__init__(parent)
        self.columnconfigure(0, weight=1)

        self.button_data: Dict[str, Dict] = {
            "INFO": {"row": 0, "command": None},
            "UPLOAD": {"row": 1, "command": None},
            "REVIEW": {"row": 2, "command": None},
            "EXPLORE": {"row": 3, "command": None},
            "HELP": {"row": 4, "command": None},
            "SETTINGS": {"row": 5,"command": None}
        }

        self.button_map: Dict[str, ttk.Button] = {}
        self._create_buttons()

    def _create_buttons(self) -> None:
        """Creates the menu buttons."""
        for text, data in self.button_data.items():
            button = ttk.Button(
                master=self,
                text=text,
                compound=TOP,
                bootstyle=OUTLINE,
                command=data["command"]
            )
            button.grid(row=data["row"], column=0, padx=10, pady=0, sticky=NSEW)
            self.button_map[text] = button

    def add_link_to_button(self, button_text: str, on_click_command: Callable) -> None:
        """Adds a click command to a button.

        Args:
            button_text (str): The text of the button to link.
            on_click_command (Callable): The function to execute on click.
        """
        if button_text in self.button_map:
            self.button_map[button_text].config(command=on_click_command)
        else:
            print(f"Warning: Button '{button_text}' not found.")