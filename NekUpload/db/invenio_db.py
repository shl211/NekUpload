from .db import db
from typing import List, Dict, Any
import requests
import logging
import os

class invenioRDM(db):
    def __init__(self):
        pass

    def upload_files(self,url: str, token: str, file_paths: List[str], metadata: Dict[str,Any]):        
        #url expected to be db_url/api/records        
        draft_response = self._create_draft_upload(url,token,metadata)
        draft_files_url = self._get_draft_files_url(draft_response)
        for file_path in file_paths:
            self._upload_file(draft_files_url,token,file_path)

        publish_records_url = self._get_publish_url(draft_response)
        self._publish_draft(publish_records_url,token)

    def _create_draft_upload(self,records_url: str, token: str, metadata: Dict[str,Any]) -> requests.Response:  # Return the response object
        """Create a draft template in Invenio.

        Args:
            records_url (str): url route to the invenio database, of form https://url/api/records
            token (str): User personal access token
            metadata (Dict[str,Any]): Metadata to be uploaded

        Returns:
            requests.Response: API response object
        """
        
        header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        try:
            response = requests.post(records_url, headers=header, json=metadata)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            logging.info(f"Draft upload created successfully: {response.json()}")  # Log the response
            return response # Return the response object
        except requests.exceptions.RequestException as e:
            logging.error(f"Error creating draft upload: {e}")
            return None  # Or handle the error as needed

    def _upload_file(self, draft_files_url: str, token: str, file_path: str) -> requests.Response:
        """Upload a single file to the draft record

        Args:
            draft_files_url (str): url route to the draft record
            token (str): User personal access token
            file_path (str): Path to the file to be uploaded

        Returns:
            requests.Response: Commit repsonse object
        """
        file_name = self._get_file_names(file_path)
        
        draft_files_response = self._prepare_upload(draft_files_url,token,file_name)

        file_upload_url = self._get_draft_files_upload_content_url(draft_files_response,file_name)
        self._do_upload(file_upload_url,token,file_path)

        #this saves the uploaded file to the repository
        file_commit_url = self._get_draft_files_upload_commit_url(draft_files_response,file_name)
        commit_response = self._commit_upload(file_commit_url,token,file_path)

        return commit_response #not sure if this is most sensible response to return

    def _prepare_upload(self,draft_files_url: str, token: str, file_name: str) -> requests.Response:
        """Creates a location in the Invenio database record to store the file

        Args:
            draft_files_url (str): url route to the invenio record draft
            token (str): User personal access token
            file_name (str): Name of file to be uploaded

        Returns:
            requests.Response: Response for preparing upload
        """
        
        header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        #use file name here rather than path as dictated by InvenioRDM API documentation
        #convert to JSON array with []
        body = [{"key": f"{file_name}"}]
        
        #initialise file metadata
        try:
            draft_files_response = requests.post(draft_files_url,headers=header, json=body)
            draft_files_response.raise_for_status()
            logging.info(f"Draft file metadata for {file_name} created succesfully: {draft_files_response.json()}")
            return draft_files_response
        except requests.exceptions.RequestException as e:
            logging.error(f"Error creating draft file metadata for {file_name}: {e}")
            raise

    def _do_upload(self,file_upload_url: str, token: str, file_path: str) -> requests.Response:
        """Upload the specified file to the records location specified in the url

        Args:
            file_upload_url (str): url route to location in records where file will be stored
            token (str): User personal access token
            file_path (str): Path of file to be uploaded

        Returns:
            requests.Response: Upload response object
        """
        
        header = {
            "Content-Type": "application/octet-stream",
            "Authorization": f"Bearer {token}"
        }

        #open in binary mode, requests behaviour is file is streamed for upload, avoiding memory issues
        with open(file_path, "rb") as f:
            try:
                upload_response = requests.put(file_upload_url, headers=header, data=f)
                upload_response.raise_for_status()
                logging.info(f"File {file_path} uploaded successfully: {upload_response.json()}")
                return upload_response
            except requests.exceptions.RequestException as e:
                logging.error(f"Error uploading file {file_path}: {e}")
                raise 
   
    def _commit_upload(self,file_commit_url: str, token: str, file_path: str) -> requests.Response:
        """Save uploaded file in the specified url location to the repository

        Args:
            file_upload_url (str): url route to location in records where file will be stored
            token (str): User personal access token
            file_path (str): Path of file to be uploaded

        Returns:
            requests.Response: Commit response object
        """
        
        header = {"Authorization": f"Bearer {token}"}

        try:
            commit_response = requests.post(file_commit_url, headers=header)
            commit_response.raise_for_status()
            logging.info(f"File {file_path} committed successfully: {commit_response.json()}")
            return commit_response
        except requests.exceptions.RequestException as e:
            logging.error(f"Error committing file {file_path}: {e}")
            raise

    def _publish_draft(self,publish_url: str, token: str) -> requests.Response:
        """Publish the specified draft on InvenioRDM

        Args:
            publish_url (str): url route to draft to be published
            token (str): User personal access token

        Returns:
            requests.Response: Publish response object
        """
        
        header = {"Authorization": f"Bearer {token}"}

        try:
            response = requests.post(publish_url, headers=header)
            response.raise_for_status()
            logging.info(f"Draft published successfully: {response.json()}")
            return response
        except requests.exceptions.RequestException as e:
            logging.error(f"Error publishing draft: {e}")
            raise
    
    def _delete_draft(self,draft_url: str, token: str) -> bool:
        header = {"Authorization": f"Bearer {token}"}

        try:
            response = requests.delete(draft_url, headers=header)
            response.raise_for_status() #raise exception for bad status codes

            if response.status_code == 204: #denotes successful deletion
                logging.info(f"Draft record deleted successfully")
                return True
            else:
                logging.error(f"Unexpected status code: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error deleting draft record: {e}")
            return False
        
    def _get_draft_files_url(self,draft_response: requests.Response) -> str:
        """Get the url for preparing a file to be uploaded to a draft record

        Args:
            draft_response (requests.Response): Record draft response object

        Returns:
            str: url route for preparing a file to be uploaded to draft record
        """
        draft_data = draft_response.json()
        return draft_data["links"]["files"]
    
    def _get_draft_files_upload_content_url(self,draft_files_response: requests.Response,file_name: str) -> str:
        """Get the url location in the records where the specified file should be uploaded

        Args:
            draft_files_response (requests.Response): Draft file response object
            file_name (str): Name of file to be uploaded

        Returns:
            str: url location of where in records specified file should be uploaded
        """
        draft_files_data = draft_files_response.json()

        # draft_files_data["entries"] is a list, and desired entry is generally at the end
        # iterate from end of list to get associated dictionary associated with the file from the list
        entry = next(entry for entry in reversed(draft_files_data["entries"]) if entry["key"] == file_name)
        file_upload_url = entry["links"]["content"]
        return file_upload_url
    
    def _get_draft_files_upload_commit_url(self,draft_files_response: requests.Response, file_name: str) -> str:
        """Get the url location detailing which file in records is to be committed

        Args:
            draft_files_response (requests.Response): Draft file response object
            file_name (str): Name of file to be uploaded

        Returns:
            str: url location detailing which file in records is to be committed
        """
        draft_files_data = draft_files_response.json()
        # draft_files_data["entries"] is a list, and desired entry is generally at the end
        # iterate from end of list to get associated dictionary associated with the file from the list
        entry = next(entry for entry in reversed(draft_files_data["entries"]) if entry["key"] == file_name)
        file_commit_url = entry["links"]["commit"]
        return file_commit_url

    def _get_publish_url(self,draft_response: requests.Response) -> str:
        """Get the url to publish the draft

        Args:
            draft_response (requests.Response): Draft response object

        Returns:
            str: url for publishing the draft
        """
        draft_data = draft_response.json()
        return draft_data["links"]["publish"]

    def _get_file_names(self,file_path: str) -> str:
        """Given a file path, extract the file name

        Args:
            file_path (str): Path to file

        Returns:
            str: File name
        """
        file_name = os.path.basename(file_path)
        return file_name