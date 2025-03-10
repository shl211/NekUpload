import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from NekUpload.newFrontend.components.header import Header
from NekUpload.newFrontend.components.menu import Menu
from NekUpload.newFrontend.scenes.info import InfoScene
from NekUpload.newFrontend.scenes.upload import UploadScene
from NekUpload.newFrontend.scenes.review import ReviewScene
from NekUpload.newFrontend.scenes.explore import ExploreScene
from NekUpload.newFrontend.scenes.help import HelpScene
from NekUpload.newFrontend.scenes.settings import SettingScene
from NekUpload.newFrontend.components.terminal import TerminalHandler,TerminalWidget
from NekUpload.newFrontend.components.settings_manager import SettingsManager
import logging

class NekUploadNewGUI:
    def __init__(self):
        self.root = ttk.Window(themename="sandstone")
        self.root.title("NekUpload")
        self.root.attributes('-zoomed', True)

        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=20)

        setting_manager = SettingsManager("","")

        #create a header
        self.header: ttk.Frame = Header(self.root)
        self.header.grid(row=0, column=0, columnspan=2, sticky=(N, E, S, W), ipadx=10, ipady=10)

        #create a menu
        self.menu = Menu(self.root)
        self.menu.grid(row=1, column=0, sticky=NSEW, ipadx=10, ipady=10)

        #pages and which button they link to
        info_page = InfoScene(self.root)
        review_page = ReviewScene(self.root)
        explore_page = ExploreScene(self.root)
        help_page = HelpScene(self.root)
        setting_page = SettingScene(self.root,setting_manager)
        upload_page = UploadScene(self.root,self.root,setting_page)

        #create page frame and default to INFO
        #menu buttons will direct pages to here
        self.page = info_page
        self.page.grid(row=1, column=1,sticky=NSEW,ipadx=20,ipady=20)  # Show new page

        self.menu.add_link_to_button("UPLOAD",lambda: self.switch_page(upload_page))
        self.menu.add_link_to_button("INFO",lambda: self.switch_page(info_page))
        self.menu.add_link_to_button("REVIEW",lambda: self.switch_page(review_page))
        self.menu.add_link_to_button("EXPLORE",lambda: self.switch_page(explore_page))
        self.menu.add_link_to_button("HELP",lambda: self.switch_page(help_page))
        self.menu.add_link_to_button("SETTINGS",lambda: self.switch_page(setting_page))

        self.terminal = TerminalWidget(self.root)
        self.terminal.grid(row=2,column=0,columnspan=2,sticky=(E,W))

        #configure terminal for logging        
        logger = logging.getLogger()  # Get the root logger
        logger.setLevel(logging.INFO)
        terminal_handler = TerminalHandler(self.terminal)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') #format of message
        terminal_handler.setFormatter(formatter)
        logger.addHandler(terminal_handler)

    def switch_page(self, new_page: ttk.Frame):
        if self.page != new_page:
            self.page.grid_forget()
            self.page = new_page
            self.page.grid(row=1, column=1,sticky=NSEW,ipadx=20,ipady=20)  # Show new page



    def run(self):
        #add welcome message
        self.root.mainloop()

if __name__ == "__main__":
    app = NekUploadNewGUI()
    app.run()
