from tkinter import *
from tkinter import filedialog
from tkinter import ttk #holds the more modern widgets
from datetime import date

from typing import List
from NekUpload.metadataModule import *
from NekUpload.uploadModule import invenioRDM
import os
from dotenv import load_dotenv

from NekUpload.frontend.terminal_widget import TerminalWidget,TerminalHandler
from NekUpload.frontend.header_frame import HeaderFrame
from NekUpload.frontend.static_fields_frame import StaticFieldsFrame
from NekUpload.frontend.dynamic_fields_frame import DynamicFieldsFrame
from NekUpload.frontend.file_selector import FileSelectorNotebookFrame
import logging

class NekUploadGUI:
    def __init__(self,root: Tk) -> None:
        self.root: Tk = root
        self.mainframe: ttk.Frame = self._create_mainframe()
        
        #dynamic fields

        self.header_frame = HeaderFrame(self.mainframe)
        self.header_frame.grid(column=0,row=0,columnspan=2,sticky=(N,W,E,S))
        self.static_fields_frame = StaticFieldsFrame(self.mainframe)
        self.static_fields_frame.grid(column=0,row=1,sticky=(N,E,W,S))

        self.dynamic_fields_frame = DynamicFieldsFrame(self.root,self.mainframe)
        self.dynamic_fields_frame.grid(column=1, row=1, rowspan=2, sticky=(N,S))

        self.file_selector_notebook_frame = FileSelectorNotebookFrame(self.mainframe)
        self.file_selector_notebook_frame.grid(row=2,column=0,sticky=(E,W))

        self.terminal = TerminalWidget(root)
        self.terminal.grid(row=6,column=0,columnspan=5,sticky=(E,W))

        #configure terminal for logging        
        logger = logging.getLogger()  # Get the root logger
        logger.setLevel(logging.INFO)
        terminal_handler = TerminalHandler(self.terminal)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') #format of message
        terminal_handler.setFormatter(formatter)
        logger.addHandler(terminal_handler)

        self.submit_button: ttk.Button = ttk.Button(self.mainframe, text="Submit", command=self.submit_form)
        self.submit_button.grid(row=7, column=1, sticky=E)

    def _create_mainframe(self) -> ttk.Frame:
        mainframe = ttk.Frame(self.root)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        return mainframe
    
    def submit_form(self) -> None: 
        
        is_read_user_guide = self.static_fields_frame.is_read_user_guide
        if not is_read_user_guide or is_read_user_guide == "False":
            logging.error("ERROR")
            return

        title: str = self.static_fields_frame.title
        publication_date: str = self.static_fields_frame.publication_date
        
        #ASSIGN USERS
        author_list: List[InvenioOrgInfo | InvenioPersonInfo] = []
        authors_from_app: List[InvenioOrgInfo | InvenioPersonInfo] = self.dynamic_fields_frame.author_list
        for author in authors_from_app:
            author_info: InvenioOrgInfo | InvenioPersonInfo = None
            
            if author["type"] == "personal":
                given_name = author["given_name"]
                last_name = author["last_name"]
                author_info = InvenioPersonInfo(given_name,last_name)
            elif author["type"] == "organizational":
                name = author["name"]
                author_info = InvenioOrgInfo(name)

            if author["id"] != "":
                mapping = {"ORCID" : IdentifierType.ORCID}
                id = Identifier(author["id"],mapping[author["id_type"]])
                author_info.add_identifier(id)
                
            #also affiliations, but not supported in backend for now
            author_list.append(author_info)

        #create metadata
        metadata = InvenioMetadata(title,publication_date,author_list,"dataset")
        metadata.add_publisher("NekUpload App")
        metadata.add_description("This was uploaded via NekUpload app")
        metadata_payload = metadata.get_metadata_payload()
        metadata_json = {"metadata": metadata_payload}
        print(metadata_json)

        #only one of the following is not empty
        dirname = self.file_selector_notebook_frame.dirname
        file_list = self.file_selector_notebook_frame.file_list

        #first see if dirname is empty, if not, use directory to upload
        upload_manager = invenioRDM()
        
        URL = self.static_fields_frame.host_name
        COMMUNITY_SLUG = self.static_fields_frame.community_slug
        API_KEY_ENV_VAR = self.static_fields_frame.api_key_env_var

        load_dotenv()
        if dirname:
            files_to_upload = [os.path.join(dirname, f) for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f))]
            upload_manager.upload_files(URL,os.getenv(API_KEY_ENV_VAR,None),files_to_upload,metadata_json,COMMUNITY_SLUG)
        elif file_list:
            upload_manager.upload_files(URL,os.getenv(API_KEY_ENV_VAR,None),file_list,metadata_json,COMMUNITY_SLUG)
        else:
            print("Failed to upload as no files detected")

def main() -> None:
    root: Tk = Tk() 
    app: NekUploadGUI = NekUploadGUI(root)
    root.title("NekUpload")
    root.mainloop()

if __name__ == "__main__":
    main()