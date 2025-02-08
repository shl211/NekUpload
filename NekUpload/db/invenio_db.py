from .db import db
from typing import List, Dict, Any
import requests
import logging
import os

class invenioRDM(db):
    def __init__(self):
        pass

    def upload_files(self,file_paths: List[str], metadata: Dict[str,Any], url: str, token: str):        
        #url expected to be db_url/api/records        
        draft_response = self._create_draft_upload(url,token,metadata)
        draft_files_url = self._get_draft_files_url(draft_response)
        for file_path in file_paths:
            upload_file_response = self._upload_file(draft_files_url,token,file_path)

    def _create_draft_upload(self,records_url: str, token: str, metadata: Dict[str,Any]) -> requests.Response:  # Return the response object
        header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        logger = logging.getLogger(__name__)

        try:
            response = requests.post(records_url, headers=header, json=metadata)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            logger.info(f"Draft upload created successfully: {response.json()}")  # Log the response
            return response # Return the response object
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating draft upload: {e}")
            return None  # Or handle the error as needed

    def _upload_file(self, draft_files_url: str, token: str, file_path: str) -> requests.Response:
        logger = logging.getLogger(__name__)
        file_name = self._get_file_names(file_path)

        header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        #use file name here rather than path as dictated by InvenioRDM API documentation
        #convert to JSON array with []
        body = [{"key": f"{file_name}"}]
        
        #initialise file metadata
        draft_files_response = None
        try:
            draft_files_response = requests.post(draft_files_url,headers=header, json=body)
            draft_files_response.raise_for_status()
            logger.info(f"Draft file metadata for {file_name} created succesfully: {draft_files_response.json()}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating draft file metadata for {file_name}: {e}")
            raise

        #add file now
        header = {
            "Content-Type": "application/octet-stream",
            "Authorization": f"Bearer {token}"
        }
        file_upload_url = self._get_draft_files_upload_content_url(draft_files_response,file_name)

        #open in binary mode, requests behaviour is file is streamed for upload, avoiding memory issues
        with open(file_path, "rb") as f:
            try:
                upload_response = requests.put(file_upload_url, headers=header, data=f)
                upload_response.raise_for_status()
                logger.info(f"File {file_path} uploaded successfully: {upload_response.json()}")
            except requests.exceptions.RequestException as e:
                logger.error(f"Error uploading file {file_path}: {e}")
                raise
   
        #finally commit the uploaded file
        file_commit_url = self._get_draft_files_upload_commit_url(draft_files_response,file_name)
        header = {"Authorization": f"Bearer {token}"}

        try:
            commit_response = requests.post(file_commit_url, headers=header)
            commit_response.raise_for_status()
            logger.info(f"File {file_path} committed successfully: {commit_response.json()}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error committing file {file_path}: {e}")
            raise

    def _publish_draft(self):
        pass
    
    def _get_draft_files_url(self,draft_response: requests.Response) -> str:
        #this returns the url for initialising a file to be uploaded
        draft_data = draft_response.json()
        return draft_data["links"]["files"]
    
    def _get_draft_files_upload_content_url(self,draft_files_response: requests.Response,file_name: str) -> str:
        #this returns the url for uploading file to online repository
        draft_files_data = draft_files_response.json()
        # draft_files_data["entries"] is a list, so access the first element:
        entry = next(entry for entry in draft_files_data["entries"] if entry["key"] == file_name)  # Get the dictionary associated with the file from the list
        file_upload_url = entry["links"]["content"] # Now you can access links
        return file_upload_url
    
    def _get_draft_files_upload_commit_url(self,draft_files_response: requests.Response, file_name: str) -> str:
        #this returns the url for commiting an uploaded file to online repository
        draft_files_data = draft_files_response.json()
        # draft_files_data["entries"] is a list, so access the first element:
        entry = next(entry for entry in draft_files_data["entries"] if entry["key"] == file_name)  # Get the dictionary associated with the file from the list
        file_commit_url = entry["links"]["commit"] # Now you can access links
        return file_commit_url

    def _get_file_names(self,file_path: str) -> str:
        file_name = os.path.basename(file_path)
        return file_name