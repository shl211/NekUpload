import ttkbootstrap as ttk
from ttkbootstrap.constants import *
#from NekUpload.newFrontend.scenes
from NekUpload.newFrontend.components.header import Header
from NekUpload.newFrontend.components.menu import Menu

class NekUploadNewGUI:
    def __init__(self):
        self.root = ttk.Window(themename="litera")
        self.root.title("NekUpload")
        self.root.attributes('-zoomed', True)

        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=10)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=20)

        #create a header
        self.header = Header(self.root)
        self.header.grid(row=0,column=0,padx=20,pady=20,columnspan=10,sticky=(N,E,S,W))

        #create a menu
        self.menu = Menu(self.root)
        self.menu.grid(row=1,column=0,padx=10,pady=10,rowspan=10,sticky=NSEW)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = NekUploadNewGUI()
    app.run()
