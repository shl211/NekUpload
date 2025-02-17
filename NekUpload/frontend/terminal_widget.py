import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext

import logging

class TerminalHandler(logging.Handler):  # Custom logging handler
    def __init__(self, terminal: 'TerminalWidget'):
        super().__init__()
        self.terminal = terminal

    def emit(self, record):
        msg = self.format(record)  # Format the log message
        self.terminal.write(msg + "\n")  # Write to the terminal
        self.terminal.terminal.update_idletasks()

class TerminalWidget(ttk.Frame):
    def __init__(self, parent: ttk.Frame, height=10, **kwargs):  # Add height parameter
        super().__init__(parent, **kwargs)

        self.terminal = scrolledtext.ScrolledText(
            self, wrap=tk.WORD, state=tk.DISABLED, height=height  # Set initial height
        )
        self.terminal.pack(fill=tk.BOTH, expand=True)  # Make it expandable

    def write(self, text: str, tag=None):
        """Appends text to the terminal.

        Args:
            text: The text to add.
            tag: An optional tag to apply to the text (for styling).
        """
        self.terminal.config(state=tk.NORMAL)  # Enable editing temporarily
        self.terminal.insert(tk.END, text, tag)

        # Autoscroll to the bottom (optional):
        self.terminal.see(tk.END)  # or self.terminal.yview(tk.END)

        self.terminal.config(state=tk.DISABLED)  # Disable editing again

    def clear(self):
        """Clears the terminal content."""
        self.terminal.config(state=tk.NORMAL)
        self.terminal.delete(1.0, tk.END)  # Delete from beginning to end
        self.terminal.config(state=tk.DISABLED)

    def tag_configure(self, tag, **kwargs):
        """Configures a tag for styling text."""
        self.terminal.tag_configure(tag, **kwargs)


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        terminal = TerminalWidget(self, height=15)  # Set initial height
        terminal.pack(fill=tk.BOTH, expand=True)

        terminal.write("Welcome to the application!\n")
        terminal.write("This is a log message.\n", tag="log")
        terminal.write("An error occurred.\n", tag="error")

        terminal.tag_configure("log", foreground="blue")
        terminal.tag_configure("error", foreground="red", font=("Arial", 10, "bold"))

        button = ttk.Button(self, text="Clear Terminal", command=terminal.clear)
        button.pack()

        # Example of writing from a separate function (e.g., in a background thread)
        def log_something():
            terminal.write("Message from another function.\n")

        self.after(2000, log_something)  # Call after 2 seconds
        self.mainloop()

if __name__ == "__main__":
    app = MyApp()
