import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from typing import List,Dict,Tuple
from .upload_widgets.geometry import UploadGeometryFrame
from .upload_widgets.session import UploadSessionFrame
from .upload_widgets.output import UploadOutputFrame
from .upload_widgets.basic import UploadInfoFrame
from NekUpload.newFrontend.components.settings_manager import SettingsManager
from NekUpload.metadataModule.invenioMetadata import InvenioMetadata
from NekUpload.metadataModule.identifier import Identifier,IdentifierType
from NekUpload.metadataModule.user import InvenioOrgInfo,InvenioPersonInfo
import logging
from NekUpload.manager import NekManager
from NekUpload.uploadModule.invenio_db import invenioRDM

class UploadScene(ScrolledFrame):
    def __init__(self,root,parent,setting_manager: SettingsManager):
        super().__init__(parent,autohide=True)

        self.root = root
        self.setting_manager = setting_manager#contains settings data

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.columnconfigure(0,weight=1)

        about_section: ttk.Frame = self._add_upload_info_section(self)
        about_section.grid(row=0,column=0,sticky=(NSEW))

        self.basic_info_section= UploadInfoFrame(self,self,self.setting_manager)
        self.basic_info_section.grid(row=1,column=0,sticky=NSEW,padx=10,pady=5)
        self.geometry_section = UploadGeometryFrame(self)
        self.geometry_section.grid(row=2,column=0,sticky=(NSEW),padx=10,pady=5)
        self.input_section = UploadSessionFrame(self)
        self.input_section.grid(row=3,column=0,sticky=(NSEW),padx=10,pady=5)
        self.output_section = UploadOutputFrame(self)
        self.output_section.grid(row=4,column=0,sticky=(NSEW),padx=10,pady=5)

        self.bind("<Configure>", self.update_wraplength)

        #upload button
        submit_button = ttk.Button(
            master=self,
            bootstyle=PRIMARY,
            text="Upload Datasets",
            command=self._upload_datasets
        )
        submit_button.grid(row=10,column=0,columnspan=10,sticky=NSEW,padx=10,pady=5)

    def update_wraplength(self, event):
        # Dynamically set the wraplength based on the width of the parent frame
        # Subtract a little for padding and margin
        self.upload_description.config(wraplength=event.width - 20)
        pass

    def _add_upload_info_section(self,parent) -> ttk.Frame:

        frame = ttk.Frame(master=parent)

        # Create the label for the title
        self.upload_info_label = ttk.Label(
            master=frame,
            text="Uploading Nektar++ Datasets",
            font=("TkDefaultFont", 20, "bold", "underline"),
            anchor="w",
            bootstyle=PRIMARY
        )
        self.upload_info_label.grid(row=0, column=0, pady=5, sticky=W)

        # Create the description label
        self.upload_description = ttk.Label(
            master=frame,
            text=("A Nektar++ dataset consists of: \n\n"
                " - Geometry Files\n"
                " - Input Files\n"
                " - Output Files\n"
                "\n"
                "There are currently two ways of uploading. The traditional way is that you have all the geometry files, "
                "input files and output files to be uploaded. Another way is that the geometry file already exists in the "
                "database, and you wish to link your input and ouptut files against it. This prevents repeated instances of "
                "same geometry file."),
            font=("TKDefaultFont", 12),
            anchor="w",
            justify="left",
        )
        self.upload_description.grid(row=1, column=0, pady=10, sticky="nsew")

        return frame

    def _upload_datasets(self):
        logging.info("UPLOADING...")

        #get general info
        publication_date: str = self.basic_info_section.publication_date_iso
        COMMUNITY_SLUG: str = self.basic_info_section.community_slug
        URL: str = self.setting_manager.database_url

        #ASSIGN USERS
        author_list: List[InvenioOrgInfo | InvenioPersonInfo] = []
        for author in self.basic_info_section.author_list:
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

        #titles for each dataset
        geometry_title = self.geometry_section.geometry_dataset_title
        input_title = self.input_section.session_dataset_title
        output_title = self.output_section.output_dataset_title

        #create metadata for each one
        metadata_geometry = InvenioMetadata(geometry_title,publication_date,author_list,"dataset")
        metadata_input = InvenioMetadata(input_title,publication_date,author_list,"dataset")
        metadata_output = InvenioMetadata(output_title,publication_date,author_list,"dataset")

        #get files
        geometry_file = self.geometry_section.geometry_file_name
        session_file = self.input_section.session_file_name
        output_file = self.output_section.output_file_name

        #use geometry title for now
        #TODO in future, look to splinter records based on geometry, input, output
        geometry_uploader = invenioRDM()
        #geometry_uploader = invenioRDM()
        #geometry_uploader = invenioRDM()

        manager = NekManager(geometry_file,
                            session_file,
                            output_file,
                            [],
                            [],
                            metadata_geometry,
                            geometry_uploader)
        
        manager.execute_upload(URL,
                            self.setting_manager.token,
                            COMMUNITY_SLUG)