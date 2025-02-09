from .db import db
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
        self.draft_url: str = None
        self.publish_url: str = None
        self.review_url: str = None

        #track where files are added in records
        self.record_file_name_url: Dict[str,str] = {} #file_name -> record_file_url
        self.record_file_name_content_url: Dict[str,str] = {} #file_name -> file_content_url
        self.record_file_name_commit_url: Dict[str,str] = {} #file_name -> file_commit_url

        #community uuid extracted from get_community
        self.community_uuid: str = None

    def upload_files(self,url: str, token: str, file_paths: List[str], metadata: Dict[str,Any],community_id: str,publish: bool=True) -> None:  
        """Upload files to an InvenioRDM repository

        Args:
            url (str): Base URL to the InvenioRDM repository.  For example: "https://my-invenio-rdm.example.com"            
            token (str): User access token
            file_paths (List[str]): List of paths of files to be uploaded
            metadata (Dict[str,Any]): Metadata to be uploaded
            community_id (str): Invenio community id for upload or slug
            publish (bool, optional): If True, will publish the record. Defaults to True.
        """        
        #prevent mixup of files from previous uploads
        self._clear()

        records_url = url + f"/api/records"
        self._create_draft_record(records_url,token,metadata)

        draft_files_url = self._get_draft_files_url()
        for file_path in file_paths:
            self._upload_file(draft_files_url,token,file_path)

        if publish:
            publish_records_url = self._get_publish_url()
            self._publish_draft(publish_records_url,token)

        self._get_community(url,token,community_id)
        community_uuid = self._get_community_uuid()

        review_url = self._get_review_url()
        self._submit_record_to_community(token,review_url,community_uuid)
        self._submit_record_for_review(url,token)


    def _create_draft_record(self,records_url: str, token: str, metadata: Dict[str,Any]) -> requests.Response:
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
            
            if response.status_code == 201:
                logging.info(f"Draft upload created successfully: {response.json()}")
                self._handle_create_draft_response(response) #add relevant variables to class 
                return response
            else:
                logging.error(f"Unexpected status code: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Error creating draft upload: {e}")
            return None

    def _upload_file(self, draft_files_url: str, token: str, file_path: str) -> requests.Response:
        """Upload a single file to the draft record

        Args:
            draft_files_url (str): url route to the draft record
            token (str): User personal access token
            file_path (str): Path to the file to be uploaded

        Returns:
            requests.Response: Commit repsonse object
        """
        file_name = self._get_file_name(file_path)
        self._prepare_upload(draft_files_url,token,file_name)

        file_upload_url = self._get_draft_files_upload_content_url(file_name)
        self._do_upload(file_upload_url,token,file_path)

        #this saves the uploaded file to the repository
        file_commit_url = self._get_draft_files_upload_commit_url(file_name)
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

            if draft_files_response.status_code == 201:
                logging.info(f"Draft file metadata for {file_name} created succesfully: {draft_files_response.json()}")
                self._handle_prepare_upload_response(draft_files_response) #extract relevant urls from response
                return draft_files_response
            else:
                logging.error(f"Unexpected status code: {draft_files_response.status_code} - {draft_files_response.text}")
                return None
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
                
                if upload_response.status_code == 200:
                    logging.info(f"File {file_path} uploaded successfully: {upload_response.json()}")
                    return upload_response
                else:
                    logging.error(f"Unexpected status code: {upload_response.status_code} - {upload_response.text}")
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
            
            if commit_response.status_code == 200:
                logging.info(f"File {file_path} committed successfully: {commit_response.json()}")
                return commit_response
            else:
                logging.error(f"Unexpected status code: {commit_response.status_code} - {commit_response.text}")
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
            response.raise_for_status() #raise exception for bad status codes
            
            if response.status_code == 202:
                logging.info(f"Draft published successfully: {response.json()}")
            else:
                logging.error(f"Unexpected status code: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error publishing draft: {e}")
            raise
    
    def _delete_draft(self,draft_url: str, token: str) -> requests.Response:
        header = {"Authorization": f"Bearer {token}"}

        try:
            response = requests.delete(draft_url, headers=header)
            response.raise_for_status() #raise exception for bad status codes

            if response.status_code == 204:
                logging.info(f"Draft record deleted successfully")
                return response
            else:
                logging.error(f"Unexpected status code: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Error deleting draft record: {e}")
            return None

    def _get_community(self,url:str, token: str,community_slug: str) -> requests.Response:
        
        community_url = url + f"/api/communities/{community_slug}"
        
        header = {
            "Authorization": f"Bearer {token}"
        }

        try:
            response = requests.get(community_url,headers=header)
            response.raise_for_status()

            if response.status_code == 200:
                logging.info(f"Successfully found community associated with {community_url}")
                self._handle_community_response(response) #extract relevant data and store in class variables
                return response
            else:
                logging.error(f"Unexpected status code: {response.status_code} - {response.text}")
        except:
            logging.error(f"Error finding community with {community_url}")
            raise
        
    def _submit_record_to_community(self,token: str,record_review_url: str,community_uuid:str) -> requests.Request:
        
        header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
            }

        body =  {
            "receiver" : {
                "community": f"{community_uuid}"
            },
            "type": "community-submission"
        }

        try:
            response = requests.put(record_review_url,headers=header,json=body)
            response.raise_for_status()

            if response.status_code == 200:
                logging.info(f"Successfully submitted record {record_review_url} to community {community_uuid}")
                return response
            else:
                logging.error(f"Unexpected status code: {response.status_code} - {response.text}")
        except:
            logging.error(f"Error submitting record {record_review_url} to community {community_uuid}")
            raise

    def _submit_record_for_review(self,base_url: str,token: str) -> requests.Response:
        submit_url = base_url + f"/api/records/{self.record_id}/draft/actions/submit-review"

        header = {"Authorization": f"Bearer {token}"}
        body = {
            "payload": {
                "content": "This draft record was submitted via the Nektar Upload and Validation Pipeline.",
                "format": "html"
            },
        }

        try: 
            response = requests.post(submit_url,headers=header,json=body)
            response.raise_for_status()

            if response.status_code == 202:
                logging.info(f"Record {self.record_id} submitted for review to community {self.community_uuid}")
                return response
            else:
                logging.error(f"Unexpected status code: {response.status_code} - {response.text}")
        except:
            logging.error(f"Error submitting record {self.record_id} for review to community {self.community_uuid}")
            raise 

    def _get_draft_files_url(self) -> str:
        """Get the url for preparing a file to be uploaded to a draft record

        Returns:
            str: url route for preparing a file to be uploaded to draft record
        """
        return self.draft_url
    
    def _get_draft_files_upload_content_url(self,file_name: str) -> str:
        """Get the url location in the records where the specified file should be uploaded

        Args:
            file_name (str): Name of file to be uploaded

        Returns:
            str: url location of where in records specified file should be uploaded
        """
        return self.record_file_name_content_url[file_name]
    
    def _get_community_uuid(self) -> str:
        return self.community_uuid

    def _get_draft_files_upload_commit_url(self, file_name: str) -> str:
        """Get the url location detailing which file in records is to be committed

        Args:
            file_name (str): Name of file to be uploaded

        Returns:
            str: url location detailing which file in records is to be committed
        """
        return self.record_file_name_commit_url[file_name]

    def _get_publish_url(self) -> str:
        """Get the url to publish the draft

        Returns:
            str: url for publishing the draft
        """
        return self.publish_url

    def _get_review_url(self) -> str:
        """Get the url to submit a record for review to community

        Returns:
            str: Review url
        """
        return self.review_url

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
        self.draft_url = data["links"]["files"]
        self.publish_url = data["links"]["publish"]
        self.review_url = data["links"]["review"]

    def _handle_prepare_upload_response(self,response: requests.Response) -> None:
        """Handles response from preparing file upload. Reads useful information into class variables

        Args:
            response (requests.Response): Preparing upload response
        """
        data = response.json()
        
        #contains dictionary of file locations
        #each dictionary has fields "key" (file_name) and "links"
        entry_list: List[Dict[str,Any]] = data["entries"]

        #search from back to front, as last entry usually the new one added
        for entry in reversed(entry_list):
            if entry["key"] not in self.record_file_name_url:
                file_name = entry["key"]
                self.record_file_name_url[file_name] = entry["links"]["self"]
                self.record_file_name_content_url[file_name] = entry["links"]["content"]
                self.record_file_name_commit_url[file_name] = entry["links"]["commit"]
                break

    def _handle_community_response(self,response: requests.Response) -> None:
        data = response.json()
        self.community_uuid = data["id"]

    def _clear(self) -> None:
        """Reset internal state of the invenioRDM uploader
        """
        self.record_id = None
        self.draft_url = None
        self.publish_url = None
        self.review_url = None

        self.record_file_name_url.clear()
        self.record_file_name_content_url.clear()
        self.record_file_name_commit_url.clear()

        self.community_uuid = None