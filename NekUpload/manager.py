from NekUpload.metadataModule.invenioMetadata import InvenioMetadata 
from NekUpload.uploadModule.invenio_db import invenioRDM
from NekUpload.metadataModule.extractor import AutoExtractor
from .validationModule import ValidateSession,ValidateOutput,ValidateGeometry
from typing import List

class NekManager:
    def __init__(self,
                geometry_file: str,
                session_file: str,
                output_file: str,
                chk_files: List[str],
                supporting_files: List[str],
                metadata: InvenioMetadata,
                uploader: invenioRDM):
        
        self.metadata_manager = metadata
        self.upload_manager = uploader
        self.file_list = [geometry_file,session_file,output_file]
        self.auto_metadata_extractor = AutoExtractor(session_file,geometry_file,output_file)

        self.session_validator = ValidateSession(session_file)
        self.geometry_validator = ValidateGeometry(geometry_file)
        self.output_validator = ValidateOutput(output_file)

    def execute_upload(self,url:str,token:str,community_id:str):
        self._update_metadata_with_auto_extraction()
        metadata_json = self.metadata_manager.get_metadata_payload()
        metadata = {"metadata": metadata_json}

        self.upload_manager.upload_files(url,token,self.file_list,metadata,community_id)

    def _update_metadata_with_auto_extraction(self):
        results = self.auto_metadata_extractor.extract_data()
        
        if version := results.get("VERSION",None):
            self.metadata_manager.add_version(version)

        #TODO implement everything else

    def validate(self):
        self.session_validator.check_schema()
        self.geometry_validator.check_schema()
        self.output_validator.check_schema()