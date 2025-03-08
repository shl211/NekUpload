import ttkbootstrap as ttk
from ttkbootstrap.constants import *
#from NekUpload.newFrontend.scenes
from NekUpload.newFrontend.components.header import Header
from NekUpload.newFrontend.components.menu import Menu
from NekUpload.newFrontend.scenes.info import InfoScene
from NekUpload.newFrontend.scenes.upload import UploadScene
from NekUpload.newFrontend.scenes.review import ReviewScene
from NekUpload.newFrontend.scenes.explore import ExploreScene
from NekUpload.newFrontend.scenes.help import HelpScene
from NekUpload.newFrontend.scenes.settings import SettingScene

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
        self.header.grid(row=0, column=0, columnspan=2, sticky=(N, E, S, W), ipadx=10, ipady=10)

        #create a menu
        self.menu = Menu(self.root)
        self.menu.grid(row=1, column=0, sticky=NSEW, ipadx=10, ipady=10)

        #pages and which button they link to
        info_page = InfoScene(self.root)
        upload_page = UploadScene(self.root)
        review_page = ReviewScene(self.root)
        explore_page = ExploreScene(self.root)
        help_page = HelpScene(self.root)
        setting_page = SettingScene(self.root)

        #create page frame and default to INFO
        #menu buttons will direct pages to here
        self.page = info_page
        self.page.grid(row=1,column=1,sticky=NSEW)
        self.page.grid_propagate(False)

        self.menu.add_link_to_button("UPLOAD",lambda: self.switch_page(upload_page))
        self.menu.add_link_to_button("INFO",lambda: self.switch_page(info_page))
        self.menu.add_link_to_button("REVIEW",lambda: self.switch_page(review_page))
        self.menu.add_link_to_button("EXPLORE",lambda: self.switch_page(explore_page))
        self.menu.add_link_to_button("HELP",lambda: self.switch_page(help_page))
        self.menu.add_link_to_button("SETTINGS",lambda: self.switch_page(setting_page))

        #help with visualising for now
        self.header.config(style="primary.TFrame")  # Bootstrap theme color
        self.menu.config(style="danger.TFrame")  # Another color for menu
        self.page.config(style="success.TFrame")  #

    def switch_page(self, new_page: ttk.Frame):
        if self.page != new_page:
            self.page.grid_forget()
            self.page = new_page
            self.page.grid(row=1, column=1,sticky=NSEW)  # Show new page
            self.page.grid_propagate(False)
            self.page.config(style="success.TFrame")  #help with visualisation for now

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = NekUploadNewGUI()
    app.run()
