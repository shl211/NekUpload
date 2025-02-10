import logging
from typing import Dict,Any,Optional,Union,List
import requests
from .custom_exceptions import APIError,ClientError
import re
import os

"""
This file contains python wrapping of API calls for ease of use. Should be same as the InvenioRDM API docs.
Not using class here as each method should be atomic and stateless, much like REST API.
All inputs stated in the documentation should be provided.
Always return a response, so clients have flexibility to choose how they want to process things.
For now, lets not worry about other error codes
"""

def create_record(url: str, 
                  token: str,
                  access: Dict[str,Any]=None,
                  files: Dict[str,Any]=None,
                  metadata: Dict[str,Any]=None,
                  custom_fields:Dict[str,Any] = None) -> requests.Response:
    """Create a record draft in InvenioRDM. Not fully implemented with access, files and custom_fields yet.

    Args:
        url (str): url route to the invenio database, of form base_url/api/records
        token (str): Personal access token
        access (Dict[str,Any]): Record access options
        files (Dict[str,Any]): Files options for the record
        metadata (Dict[str,Any]): Metadata to be uploaded
        custom_fields (Dict[str,Any]): Custom fields metadata for record (v10 and newer)

    Returns:
        requests.Response: Returns a requests.Response object on success (201 status code) 
    
    Raises:
        APIError: If an error occurs during the API call. 
        ClientError: If an error occurs due to invalid message parameters
    """
    
    if not _is_valid_url(url,"/api/records"):
        msg = f"url: {url} is invalid, should be of form base_url/api/records. API call terminated."
        logging.error(msg)
        raise ClientError(msg)

    if not _is_valid_metadata(metadata):
        msg = f"Metadata must be a Dict, currently is a {type(metadata)}"
        logging.error(msg)
        raise ClientError(msg)

    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(url, headers=header, json=metadata)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        
        if response.status_code == 201:
            _log_debug_response("Record created succesfully",response)
            return response
        else:
            err_msg = f"Unexpected status code: {response.status_code} - {response.text}"
            logging.error(err_msg)
            raise APIError(err_msg,response=response) 
    except requests.exceptions.RequestException as e:
        err_msg = f"Request Error: {e}"
        logging.error(err_msg)
        raise APIError(err_msg)

def prepare_file_upload(url: str,token: str,file_name_list: List[str]) -> requests.Response:
    """Creates a location in the Invenio database record to store the files

    Args:
        url (str): url route to the invenio record draft, of form base_url/api/records/{record_id}/draft/files
        token (str): Personal access token
        file_name_list (List[str[]): List of names of file to be uploaded

    Returns:
        requests.Response: Response for preparing file upload

    Raises:
        APIError: If an error occurs during the API call. 
        ClientError: If an error occurs due to invalid message parameters
    """
    
    #sanitise incoming data
    valid_url_pattern = r".*/api/records/[^/]+/draft/files$"
    if re.search(valid_url_pattern,url) is None:
        msg = f"url: {url} is invalid, should be of form base_url/api/records/record_id/draft/files. API call terminated."
        logging.error(msg)
        raise ClientError(msg)
    
    for file_name in file_name_list:
        if not _is_valid_file_name(file_name):
            msg = f"{file_name} is a path, not a file name"
            logging.error(msg)
            raise ClientError(msg)

    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    #convert to JSON array with []
    body = [{"key": file_name} for file_name in file_name_list]
    
    try:
        response = requests.post(url,headers=header, json=body)
        response.raise_for_status()

        if response.status_code == 201:
            _log_debug_response("Files prepared for uploads", response)
            return response
        else:
            err_msg = f"Unexpected status code: {response.status_code} - {response.text}"
            logging.error(err_msg)
            raise APIError(err_msg,response=response)
    except requests.exceptions.RequestException as e:
        err_msg = f"Request Error: {e}"
        logging.error(err_msg)
        raise APIError(err_msg)

def upload_file(url: str, token: str, file_path: str) -> requests.Response:
    """Upload the specified file to the records location specified in the url

    Args:
        url (str): url route to location in records where file will be stored, of form baser_url/api/records/{record_id}/draft/files/{filename}/content
        token (str): User personal access token
        file_path (str): Path of file to be uploaded

    Returns:
        requests.Response: Upload response object
    
    Raises:
        APIError: If an error occurs during the API call. 
        ClientError: If an error occurs due to invalid message parameters
    """

    #sanitise incoming data
    file_name = file_path.split('/')[-1]

    valid_url_pattern = rf".*/api/records/[^/]+/draft/files/{file_name}/content$"
    if re.search(valid_url_pattern,url) is None:
        msg = f"url: {url} is invalid, should be of form base_url/api/records/record_id/draft/files/{file_name}/content. API call terminated."
        logging.error(msg)
        raise ClientError(msg)

    if not os.path.isfile(file_path):
        msg = f"File path: {file_path} does not exist or is not a file."
        logging.error(msg)
        raise ClientError(msg)

    #there is an optional size parameter, but we choose to ignore for now
    header = {
        "Content-Type": "application/octet-stream",
        "Authorization": f"Bearer {token}"
    }

    #open in binary mode, requests behaviour is file is streamed for upload, avoiding memory issues
    with open(file_path, "rb") as f:
        try:
            response = requests.put(url, headers=header, data=f)
            response.raise_for_status()
            
            if response.status_code == 200:
                _log_debug_response(f"File {file_path} uploaded successfully", response)
                return response
            else:
                err_msg = f"Unexpected status code: {response.status_code} - {response.text}"
                logging.error(err_msg)
                raise APIError(err_msg,response=response)
        except requests.exceptions.RequestException as e:
            err_msg = f"Request Error: {e}"
            logging.error(err_msg)
            raise APIError(err_msg)

def commit_file_upload(url: str, token: str, filename: str) -> requests.Response:
    """Save uploaded file in the specified url location to the repository

    Args:
        url (str): url route to location in records where file will be stored base_url/api/records/{record_id}/draft/files/{filename}/commit
        token (str): Personal access token
        filename (str): Name of file to be uploaded

    Returns:
        requests.Response: Commit response object

    Raises:
        APIError: If an error occurs during the API call. 
        ClientError: If an error occurs due to invalid message parameters
    """
    #sanitise incoming data
    if '/' in filename:
        msg = f"filename: {filename} is a path, not file"
        logging.error(msg)
        raise ClientError(msg)

    valid_url_pattern = rf".*/api/records/[^/]+/draft/files/{filename}/commit$"
    if re.search(valid_url_pattern,url) is None:
        msg = f"url: {url} is invalid, should be of form base_url/api/records/record_id/draft/files/{filename}/commit. API call terminated."
        logging.error(msg)
        raise ClientError(msg)

    header = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.post(url, headers=header)
        response.raise_for_status()
        
        if response.status_code == 200:
            _log_debug_response(f"File {filename} committed successfully",response)
            return response
        else:
            err_msg = f"Unexpected status code: {response.status_code} - {response.text}"
            logging.error(err_msg)
            raise APIError(err_msg,response=response)    
    except requests.exceptions.RequestException as e:
            err_msg = f"Request Error: {e}"
            logging.error(err_msg)
            raise APIError(err_msg)

def publish_draft(url: str, token: str) -> requests.Response:
    """Publish the specified draft on InvenioRDM

    Args:
        url (str): url route to draft to be published base_url/api/records/{record_id}/draft/actions/publish
        token (str): User personal access token

    Returns:
        requests.Response: Publish response object

    Raises:
        APIError: If an error occurs during the API call. 
        ClientError: If an error occurs due to invalid message parameters
    """
    
    #sanitise incoming data
    valid_url_pattern = rf".*/api/records/[^/]+/draft/actions/publish$"
    if re.search(valid_url_pattern,url) is None:
        msg = f"url: {url} is invalid, should be of form base_url/api/records/record_id/draft/actions/publish. API call terminated."
        logging.error(msg)
        raise ClientError(msg)

    header = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.post(url, headers=header)
        response.raise_for_status() #raise exception for bad status codes
        
        if response.status_code == 202:
            _log_debug_response(f"Draft published successfully.",response)
            return response
        else:
            err_msg = f"Unexpected status code: {response.status_code} - {response.text}"
            logging.error(err_msg)
            raise APIError(err_msg,response=response)     
    except requests.exceptions.RequestException as e:
        err_msg = f"Request Error: {e}"
        logging.error(err_msg)
        raise APIError(err_msg)

def delete_draft(url: str, token: str) -> requests.Response:
    """Delete a draft record

    Args:
        draft_url (str): url location of draft record base_url/api/records/{record_id}/draft
        token (str): Personal access token

    Returns:
        requests.Response: Delete response object

    Raises:
        APIError: If an error occurs during the API call. 
        ClientError: If an error occurs due to invalid message parameters
    """

    #sanitise incoming data
    valid_url_pattern = rf".*/api/records/[^/]+/draft$"
    if re.search(valid_url_pattern,url) is None:
        msg = f"url: {url} is invalid, should be of form base_url/api/records/record_id/draft. API call terminated."
        logging.error(msg)
        raise ClientError(msg)

    header = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.delete(url, headers=header)
        response.raise_for_status() #raise exception for bad status codes

        if response.status_code == 204:
            _log_debug_response(f"Draft deleted successfully.",response)
            return response
        else:
            err_msg = f"Unexpected status code: {response.status_code} - {response.text}"
            logging.error(err_msg)
            raise APIError(err_msg,response=response)     
    except requests.exceptions.RequestException as e:
        err_msg = f"Request Error: {e}"
        logging.error(err_msg)
        raise APIError(err_msg)

def get_community(url:str, token: str,community_slug: str) -> requests.Response:
    """Get community specified by the community slug or id

    Args:
        url (str): url to communities base_url/api/communities/community-id
        token (str): Personal access token
        community_slug (str): Community url slug or uuid

    Returns:
        requests.Response: Get community response

    Raises:
        APIError: If an error occurs during the API call. 
        ClientError: If an error occurs due to invalid message parameters
    """
    
    #sanitise incoming data
    valid_url_pattern = rf".*/api/communities/{community_slug}$"
    if re.search(valid_url_pattern,url) is None:
        msg = f"url: {url} is invalid, should be of form base_url/api/communities/community-id. API call terminated."
        logging.error(msg)
        raise ClientError(msg)

    header = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url,headers=header)
        response.raise_for_status()

        if response.status_code == 200:
            _log_debug_response(f"Successfully found community associated with {url}",response)
            return response
        else:
            err_msg = f"Unexpected status code: {response.status_code} - {response.text}"
            logging.error(err_msg)
            raise APIError(err_msg,response=response)     
    except requests.exceptions.RequestException as e:
        err_msg = f"Request Error: {e}"
        logging.error(err_msg)
        raise APIError(err_msg)

def submit_record_to_community(url: str,token: str,community_uuid:str) -> requests.Request:
    """Submit a record to a specified community

    Args:
        url (str): Record review url base_url/api/records/{record_id}/draft/review
        token (str): Personal access token
        community_uuid (str): Community UUID

    Returns:
        requests.Request: Community submission response
    
    Raises:
        APIError: If an error occurs during the API call. 
        ClientError: If an error occurs due to invalid message parameters
    """
    
    #sanitise incoming data
    valid_url_pattern = rf".*/api/records/[^/]+/draft/review$"
    if re.search(valid_url_pattern,url) is None:
        msg = f"url: {url} is invalid, should be of form base_url/api/records/record_id/draft/review. API call terminated."
        logging.error(msg)
        raise ClientError(msg)

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
        response = requests.put(url,headers=header,json=body)
        response.raise_for_status()

        if response.status_code == 200:
            _log_debug_response(f"Successfully submitted record {url} to community {community_uuid}",response)
            return response
        else:
            err_msg = f"Unexpected status code: {response.status_code} - {response.text}"
            logging.error(err_msg)
            raise APIError(err_msg,response=response)     
    except requests.exceptions.RequestException as e:
        err_msg = f"Request Error: {e}"
        logging.error(err_msg)
        raise APIError(err_msg)

def submit_record_for_review(url: str,token: str,payload: Dict[str,str]) -> requests.Response:
    """Once record is submmitted to community, submit it now for review

    Args:
        base_url (str): Base url base_url/api/records/{record_id}/draft/actions/submit-review
        token (str): Personal access token
        payload(str): Contains content and format
        
    Returns:
        requests.Response: Record review submission response
    
    Raises:
        APIError: If an error occurs during the API call. 
        ClientError: If an error occurs due to invalid message parameters
    """
    
    #sanitise incoming data
    if not _is_valid_comment_payload(payload):
        msg = f"Current payload {payload} is invalid. Should contain 'content': str and 'format': 'html'"
        logging.error(msg)
        raise ClientError(msg)

    valid_url_pattern = rf".*/api/records/[^/]+/draft/actions/submit-review$"
    if re.search(valid_url_pattern,url) is None:
        msg = f"url: {url} is invalid, should be of form base_url/api/records/record_id/draft/review. API call terminated."
        logging.error(msg)
        raise ClientError(msg)
        
    header = {"Authorization": f"Bearer {token}"}
    body = {"payload": payload}

    try: 
        response = requests.post(url,headers=header,json=body)
        response.raise_for_status()

        if response.status_code == 202:
            _log_debug_response(f"Record submitted to community for review",response)
            return response
        else:
            err_msg = f"Unexpected status code: {response.status_code} - {response.text}"
            logging.error(err_msg)
            raise APIError(err_msg,response=response)     
    except requests.exceptions.RequestException as e:
        err_msg = f"Request Error: {e}"
        logging.error(err_msg)
        raise APIError(err_msg)

def _is_valid_url(url:str,expected_ending:Optional[str]=None) -> bool:
    """Check whether url is of correct form i.e. base_url/expected_ending.
    If expected_ending is empty or None, then expect of form base_url 

    Args:
        url (str): url to check
        expected_ending (str): expected ending route

    Returns:
        bool: Whether the url is a valid API route
    """
    if url.endswith('/'):
        return False

    if expected_ending:
        return url.endswith(expected_ending)
    
    return True

def _log_debug_response(msg: str, response: requests.Response) -> None:
    """Log a debug statement to logger, with message and response.
    Will take form msg: response. For long responses, they are shortened when logged. 

    Args:
        msg (str): User defined message
        response (requests.Response): Request response 
    """
    try:
        response_data = response.json()
        if isinstance(response_data, dict) and len(response_data) > 10:
            response_data = {k: response_data[k] for k in list(response_data)[:10]}
            response_data['...'] = '...'
        elif isinstance(response_data, list) and len(response_data) > 10:
            response_data = response_data[:10] + ['...']
    except ValueError:
        response_data = response.text[:1000] + '...' if len(response.text) > 1000 else response.text

    logging.debug(f"{msg}: {response_data}")

def _is_valid_metadata(metadata: Dict[str,Any]) -> bool:
    #might want to introduce other checks
    return isinstance(metadata, dict)

def _is_valid_file_name(file_name:str) -> bool:
    """Check if the file name is valid by ensuring it does not contain any '/' characters.

    Args:
        file_name (str): The file name to check.

    Returns:
        bool: True if the file name is valid, False otherwise.
    """
    return '/' not in file_name

def _is_valid_comment_payload(payload: Dict[str,str]) -> bool:
    """Checks whether comment payload has correct format

    Args:
        payload (Dict[str,str]): Payload

    Returns:
        bool: Is valid
    """
    if len(payload) != 2:
        return False
    
    #must have format as html
    try:
        if payload["format"] != "html":
            return False
    except KeyError:
        return False
    
    #must havwe content as string
    try: 
        if not isinstance(payload["content"],str):
            return False
    except KeyError:
        return False
    
    return True