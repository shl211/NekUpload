import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame

class InfoScene(ScrolledFrame):
    def __init__(self, parent):
        super().__init__(parent, autohide=True)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        LEFT_MARGIN = 5

        # Create the label for the title
        about_label = ttk.Label(
            master=self,
            text="What is NekUpload?",
            font=("TkDefaultFont", 20, "bold", "underline"),
            anchor="center",
            bootstyle=PRIMARY
        )
        about_label.grid(row=0, column=0, pady=5, padx=LEFT_MARGIN, sticky=W)

        # Create the description label
        self.about_description = ttk.Label(
            master=self,
            text=("NekUpload is designed to enforce a consistent upload format for Nektar++ datasets. "
                "This program removes the burden of data management from the user, ensuring files are uploaded in a defined format. "
                "This ensures that data management best practices are enforced, and that users can easily find their files, "
                "which are hosted on an online repository. This also ensures that the online post-processing programs can function correctly."),
            font=("TKDefaultFont", 12),
            anchor="w",
            justify="left",
        )
        self.about_description.grid(row=1, column=0, padx=LEFT_MARGIN, pady=10, sticky="nsew")

        # Bind the configure event to dynamically adjust wraplength
        self.bind("<Configure>", self.update_wraplength)

    def update_wraplength(self, event):
        # Dynamically set the wraplength based on the width of the parent frame
        # Subtract a little for padding and margin
        self.about_description.config(wraplength=event.width - 20)

