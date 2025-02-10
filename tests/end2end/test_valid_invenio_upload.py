import pytest
from dotenv import load_dotenv
import os
from NekUpload.db import invenioRDM
import NekUpload.db.invenio_rdm_api as invenioAPI 
from typing import Tuple
import requests
import socket

@pytest.fixture()
def load_env() -> Tuple[str,str,str]:
    URL,TOKEN,COMMUNITY_SLUG = load_env_helper()

    return URL,TOKEN,COMMUNITY_SLUG

#does exact same thing as fixture, but this is for pytest.mark.skipif condition
def load_env_helper()-> Tuple[str,str,str]:
    load_dotenv()
    
    #currently use Invenio RDM demo instance
    URL = os.getenv("INVENIO_RDM_DEMO_URL",None)
    TOKEN = os.getenv("INVENIO_RDM_DEMO_TOKEN",None)
    COMMUNITY_SLUG = os.getenv("INVENIO_RDM_TEST_COMMUNITY_SLUG",None)

    return URL,TOKEN,COMMUNITY_SLUG

def has_internet_helper() -> bool:
    URL,_,_ = load_env_helper()
    try:
        # Try to open a connection using requests (more robust)
        requests.get(URL, timeout=5) 
        return True
    except (requests.exceptions.RequestException, socket.timeout):
        return False
    
#test skipped if no internet or server unavailable or no environment variables
@pytest.mark.skipif(
    any(x is None for x in load_env_helper()) or not has_internet_helper(),  # Combined condition
    reason="Missing required environment variables or no internet connection"
)
def test_valid_invenio_upload(load_env):
    URL,TOKEN,COMMUNITY_SLUG = load_env
    
    metadata = {
        "metadata": {
            "title": "NEKTAR TEST UPLOAD AND PUBLISH TO COMMUNITY END-TO-END TEST",
            "creators": [
                {
                    "person_or_org": {
                        "given_name": "Stephen",
                        "family_name": "Liu",
                        "type": "personal",
                        "identifiers": [{"identifier": "0000-0002-1825-0097"}]
                    },
                    "affiliations": [{"name": "Imperial College London"}]
                }
            ],
            "publisher": "InvenioRDM",
            "publication_date": "2024-05-14",
            "resource_type": {"id": "dataset"}
        }
    }

    database = invenioRDM()
    
    #take tests as root
    files = ["../datasets/ADRSolver/ADR_2D_TriQuad.nekg",
            "../datasets/ADRSolver/ADR_2D_TriQuad.xml",
            "../datasets/ADRSolver/ADR_2D_TriQuad.fld",
            "../datasets/ADRSolver/ADR_2D_TriQuad_0.chk"]

    #get absolute path from wherever this is run
    files_abs_paths = [os.path.join(os.path.dirname(__file__),f) for f in files]

    try:
        database.upload_files(URL,TOKEN,files_abs_paths,metadata,COMMUNITY_SLUG)
    except Exception as e:
        assert False, "The upload should have succeeded, but it failed."

    #now use API from that package to check data
    record_id = database.record_id
    request_id = database.request_id

    get_record_response = invenioAPI.get_record(URL,TOKEN,record_id)
    record_data = get_record_response.json()

    #check uploaded metadata is correct
    data_to_check = ["title","publisher","publication_date"]
    for key in data_to_check:
        assert record_data["metadata"][key] == metadata["metadata"][key]

    affilliation = record_data["metadata"]["creators"][0]["affiliations"]
    expected_affiliation = metadata["metadata"]["creators"][0]["affiliations"]
    assert affilliation == expected_affiliation
    
    person_or_org = record_data["metadata"]["creators"][0]["person_or_org"]
    expected_person_or_org = metadata["metadata"]["creators"][0]["person_or_org"]

    assert person_or_org["given_name"] == expected_person_or_org["given_name"]
    assert person_or_org["family_name"] == expected_person_or_org["family_name"]
    assert person_or_org["type"] == expected_person_or_org["type"]
    assert person_or_org["identifiers"][0]["identifier"] == expected_person_or_org["identifiers"][0]["identifier"]

    assert record_data["metadata"]["resource_type"]["id"] == metadata["metadata"]["resource_type"]["id"]

    assert record_data["id"] == record_id
    assert record_data["is_published"] == False

    #clean up
    payload = {"content": "Cleaning up test","format": "html"}
    invenioAPI.cancel_review_request(URL,TOKEN,request_id,payload)
    invenioAPI.delete_draft(URL,TOKEN,record_id)
