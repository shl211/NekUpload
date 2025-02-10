from .db import db
from . import invenio_rdm_api as invenioAPI 
from typing import List, Dict, Any
import requests
import logging
import os

# Note that all private functions will return requests.Response for flexibility and testing purposes
# Each member function is responsible for handling that requests.Response and parsing relevant data, stored in class files

class invenioRDM(db):
    def __init__(self):
        #instantiated after draft record is created
        self.record_id: str = None

        #community uuid extracted from get_community
        self.community_uuid: str = None

        #acquired after submitting request to community
        self.request_id: str = None

    def upload_files(self,url: str, token: str, file_paths: List[str], metadata: Dict[str,Any],community_id: str) -> None:  
        """Upload files to an InvenioRDM repository and submit to community for review

        Args:
            url (str): Base URL to the InvenioRDM repository.  For example: "https://my-invenio-rdm.example.com"            
            token (str): User access token
            file_paths (List[str]): List of paths of files to be uploaded
            metadata (Dict[str,Any]): Metadata to be uploaded
            community_id (str): Invenio community id for upload or slug
        """        
        #prevent mixup of files from previous uploads
        self._clear()

        #create the draft
        create_record_response = invenioAPI.create_record(url,token,metadata)
        self._handle_create_draft_response(create_record_response)
        logging.info(f"Record draft {self.record_id} has been created.")

        #after creation of draft, if any api calls fail, clean up the draft to prevent clutter
        try: 
            #set up the file locations in the record
            file_name_list = [self._get_file_name(file) for file in file_paths]
            invenioAPI.prepare_file_upload(url,token,self.record_id,file_name_list) #does batch
            logging.info(f"Draft {self.record_id} now ready for file uploads.")

            #upload each file and commit
            for file,filename in zip(file_paths,file_name_list):
                invenioAPI.upload_file(url,token,self.record_id,file)
                invenioAPI.commit_file_upload(url,token,self.record_id,filename)
                logging.info(f"File {file} has been uploaded and committed to record {self.record_id}")

            #get community uuid, then submit record to communtiy for review
            community_request = invenioAPI.get_community(url,token,community_id)
            self._handle_community_response(community_request)
            create_review_request_response = invenioAPI.submit_record_to_community(url,token,self.community_uuid,self.record_id)
            self._handle_create_review_request_response(create_review_request_response)

            payload = {
                "content": "This record was submitted via the Nektar++ validation and upload pipeline",
                "format": "html"
            } #this is a comment for the reviewer as to what this record is
            
            invenioAPI.submit_record_for_review(url,token,self.record_id,payload)
            logging.info(f"Record {self.record_id} has been submitted to community {self.community_uuid} for review")
        except Exception as e:
            invenioAPI.delete_draft(url,token,self.record_id)
            logging.info(f"Record draft {self.record_id} has been deleted due to error: {e}")
            raise
    
    def _get_community_uuid(self) -> str:
        """Get community UUID

        Returns:
            str: Community UUID
        """
        return self.community_uuid

    def _get_file_name(self,file_path: str) -> str:
        """Given a file path, extract the file name

        Args:
            file_path (str): Path to file

        Returns:
            str: File name
        """
        file_name = os.path.basename(file_path)
        return file_name

    def _handle_create_draft_response(self,response: requests.Response) -> None:
        """Handles response from creation of draft. Reads useful information into class variables

        Args:
            response (requests.Response): Create draft response
        """
        data = response.json()
        self.record_id = data["id"]

    def _handle_community_response(self,response: requests.Response) -> None:
        """Handles get community request response

        Args:
            response (requests.Response): Get Community response
        """
        data = response.json()
        self.community_uuid = data["id"]

    def _handle_create_review_request_response(self,response: requests.Response) -> None:
        """Handles create review request response

        Args:
            response (requests.Response): Create review request response
        """
        data = response.json()
        self.request_id = data["id"]

    def _clear(self) -> None:
        """Reset internal state of the invenioRDM uploader
        """
        self.record_id = None
        self.community_uuid = None
        self.request_id = None
