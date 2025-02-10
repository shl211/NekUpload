import NekUpload.db.invenio_rdm_api as invenioAPI
import pytest
from typing import Dict,Any
import requests

@pytest.fixture
def sample_metadata() -> Dict[str,Any]:
    metadata =  {
                "creators": [
                {
                    "person_or_org": {
                    "family_name": "Brown",
                    "given_name": "Troy",
                    "type": "personal"
                    }
                },
                {
                    "person_or_org": {
                    "family_name": "Collins",
                    "given_name": "Thomas",
                    "identifiers": [
                        {"scheme": "orcid", "identifier": "0000-0002-1825-0097"}
                    ],
                    "name": "Collins, Thomas",
                    "type": "personal"
                    },
                    "affiliations": [
                    {
                        "id": "01ggx4157",
                        "name": "Entity One"
                    }
                    ]
                }
                ],
            }
    
    return metadata

@pytest.fixture
def sample_record_id() -> str:
    return "id12345"

@pytest.fixture
def sample_host_name() -> str:
    return "https://api.example.com"

@pytest.fixture
def sample_token() -> str:
    return "token12345"

def test_valid_create_draft_record(mocker,sample_host_name,sample_metadata, sample_record_id,sample_token):
    mock_response: requests.Response = mocker.Mock()
    mock_response.status_code = 201
    
    #include critical details in response
    mock_response.json.return_value = {
        "metadata": sample_metadata,
        "id": sample_record_id,
        "links": {
            "latest": f"{sample_host_name}/api/records/{sample_record_id}/versions/latest",
            "versions": f"{sample_host_name}/api/records/{sample_record_id}/versions",
            "self_html": f"{sample_host_name}/uploads/{sample_record_id}",
            "publish": f"{sample_host_name}/api/records/{sample_record_id}/draft/actions/publish",
            "latest_html": f"{sample_host_name}/records/{sample_record_id}/latest",
            "self": f"{sample_host_name}/api/records/{sample_record_id}/draft",
            "files": f"{sample_host_name}/api/records/{sample_record_id}/draft/files",
            "access_links": f"{sample_host_name}/api/records/{sample_record_id}/access/links",
            "review": f"{sample_host_name}/api/records/{sample_record_id}/draft/review", #not included in draft docs, but is in quickstart docs
        }
    }
    mock_post = mocker.patch("requests.post",return_value=mock_response)

    #now test api call
    response = invenioAPI.create_record(sample_host_name,sample_token,metadata=sample_metadata)

    # check behaviour
    assert response.status_code == 201
    assert response.json() == mock_response.json.return_value

    # verify call
    mock_post.assert_called_once()
    call_args = mock_post.call_args  # get all call arguments
    
    # Compare URLs
    expected_url = sample_host_name + "/api/records"
    called_url = call_args[0][0]
    assert called_url == expected_url, f"Expected URL: {expected_url}, Actual URL: {called_url}"

    # Compare headers
    called_headers = call_args[1]['headers']
    expected_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {sample_token}"
    }
    assert called_headers == expected_headers

    # Compare body
    called_body = call_args[1]['json']
    assert called_body == sample_metadata

def test_valid_prepare_file_upload(mocker,sample_host_name,sample_record_id,sample_token):
    mock_response: requests.Response = mocker.Mock()
    mock_response.status_code = 201

    #include critical details in response
    mock_response.json.return_value = {
        "entries": [
            {
            "key": "test.txt",
            "links": 
                {
                "content": f"{sample_host_name}/api/records/{sample_record_id}/files/text.txt/content",
                "self": f"{sample_host_name}/api/records/{sample_record_id}/files/text.txt",
                "commit": f"{sample_host_name}/api/records/{sample_record_id}/files/text.txt/commit",
                },
            },
        ]
    }
    mock_post = mocker.patch("requests.post",return_value=mock_response)

    #now test api call
    response = invenioAPI.prepare_file_upload(sample_host_name,sample_token,sample_record_id,["test.txt"])

    #assert correct behaviour
    assert response.status_code == 201
    assert response.json() == mock_response.json.return_value

    #verify call
    mock_post.assert_called_once()
    call_args = mock_post.call_args#get all call arguments
    
    # Compare URLs
    expected_url = f"{sample_host_name}/api/records/{sample_record_id}/draft/files"
    called_url = call_args[0][0]
    assert called_url == expected_url, f"Expected URL: {expected_url}, Actual URL: {called_url}"

    #compare headers
    called_headers = call_args[1]['headers']
    expected_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {sample_token}"
    }
    assert called_headers == expected_headers

    #compare body
    expected_data = [{"key": "test.txt"}]
    called_body = call_args[1]['json']
    assert called_body == expected_data

def test_valid_upload_file(mocker,sample_host_name,sample_record_id,sample_token):
    mock_response: requests.Response = mocker.Mock()
    mock_response.status_code = 200

    #include critical details in response
    file = "ADR_2D_TriQuad.xml"
    file_path = f"datasets/ADRSolver/{file}" #relative to tests root
    mock_response.json.return_value = {
        "key": file,
        "status": "pending",
        "links": {
            "content": f"{sample_host_name}/api/records/{sample_record_id}/draft/files/{file}/content",
            "self": f"{sample_host_name}/api/records/{sample_record_id}/draft/files/{file}",
            "commit": f"{sample_host_name}/api/records/{sample_record_id}/draft/files/{file}/commit"
        }
    }
    mock_put = mocker.patch("requests.put",return_value=mock_response)

    #now test api call
    response = invenioAPI.upload_file(sample_host_name,sample_token,sample_record_id,file_path)

    #assert correct behaviour
    assert response.status_code == 200
    assert response.json() == mock_response.json.return_value

    #verify call
    mock_put.assert_called_once()
    call_args = mock_put.call_args#get all call arguments
    
    #compare url
    expected_url = f"{sample_host_name}/api/records/{sample_record_id}/draft/files/{file}/content"
    called_url = call_args[0][0]
    assert called_url == expected_url, f"Expected URL: {expected_url}, Actual URL: {called_url}"

    #compare headers, no body for this one
    called_headers = call_args[1]['headers']
    expected_headers = {
        "Content-Type": "application/octet-stream",
        "Authorization": f"Bearer {sample_token}"
    }
    assert called_headers == expected_headers

def test_valid_commit_file(mocker,sample_host_name,sample_record_id,sample_token):
    mock_response: requests.Response = mocker.Mock()
    mock_response.status_code = 200

    #just detail most important parts
    file = "test.txt"
    file_path = "path/to/file/test.txt"
    mock_response.json.return_value = {
        "key": f"{file}",
        "version_id": "123",
        "file_id": "456",
        "bucket_id": "789",
        "size": 100,
        "links": {
            "self": f"{sample_host_name}/api/records/{sample_record_id}/draft/files/{file}",
            "content": f"{sample_host_name}/api/records/{sample_record_id}/draft/files/{file}/content",
            "commit": f"{sample_host_name}/api/records/{sample_record_id}/draft/files/{file}/commit",
        }
    }
    mock_post = mocker.patch("requests.post",return_value=mock_response)

    #now make api call
    response = invenioAPI.commit_file_upload(sample_host_name,sample_token,sample_record_id,file)

    #assert correct behaviour
    assert response.status_code == 200
    assert response.json() == mock_response.json.return_value
    
    #verify call
    mock_post.assert_called_once()
    call_args = mock_post.call_args#get all call arguments
    
    #compare urls
    expected_url = f"{sample_host_name}/api/records/{sample_record_id}/draft/files/{file}/commit"
    called_url = call_args[0][0]
    assert called_url == expected_url, f"Expected URL: {expected_url}, Actual URL: {called_url}"

    #compare headers, no body for this one
    called_headers = call_args[1]['headers']
    expected_headers = {"Authorization": f"Bearer {sample_token}"}
    assert called_headers == expected_headers

def test_valid_publish_draft(mocker,sample_host_name,sample_metadata,sample_record_id,sample_token):
    mock_response: requests.Response = mocker.Mock()
    mock_response.status_code = 202

    #just detail most important parts
    mock_response.json.return_value = {
        "id": sample_record_id,
        "is_published": True,
        "metadata": sample_metadata,
        "links": {
            "self": f"{sample_host_name}/api/records/{sample_record_id}",
            "files": f"{sample_host_name}/api/records/{sample_record_id}/files",
        }
    }
    mock_post = mocker.patch("requests.post",return_value=mock_response)

    #now make api call
    response = invenioAPI.publish_draft(sample_host_name,sample_token,sample_record_id)

    #assert correct behaviour
    assert response.status_code == 202
    assert response.json() == mock_response.json.return_value

    #verify call
    mock_post.assert_called_once()
    call_args = mock_post.call_args#get all call arguments
    
    #compare urls
    expected_url = f"{sample_host_name}/api/records/{sample_record_id}/draft/actions/publish"
    called_url = call_args[0][0]
    assert called_url == expected_url, f"Expected URL: {expected_url}, Actual URL: {called_url}"

    #compare headers, no body to check for this one
    called_headers = call_args[1]['headers']
    expected_headers = {"Authorization": f"Bearer {sample_token}"}
    assert called_headers == expected_headers

def test_valid_delete_draft(mocker,sample_host_name,sample_record_id,sample_token):
    mock_response: requests.Response = mocker.Mock()
    mock_response.status_code = 204

    #no content returned 
    mock_response.json.return_value = {}
    mock_delete = mocker.patch("requests.delete",return_value=mock_response)

    #now make api call
    response = invenioAPI.delete_draft(sample_host_name,sample_token,sample_record_id)

    #assert correct behaviour
    assert response.status_code == 204
    assert response.json() == mock_response.json.return_value

    #verify call
    mock_delete.assert_called_once()
    call_args = mock_delete.call_args#get all call arguments
    
    #compare urls
    expected_url = f"{sample_host_name}/api/records/{sample_record_id}/draft"
    called_url = call_args[0][0]
    assert called_url == expected_url, f"Expected URL: {expected_url}, Actual URL: {called_url}"

    #compare headers, no body for this one 
    called_headers = call_args[1]['headers']
    expected_headers = {"Authorization": f"Bearer {sample_token}"}
    assert called_headers == expected_headers

def test_valid_get_community(mocker,sample_host_name,sample_metadata,sample_token):
    mock_response: requests.Response = mocker.Mock()
    mock_response.status_code = 200
    
    #just detail most important parts
    id = "slug"
    community_slug = "slug"
    community_uuid = "123-abc-789"

    mock_response.json.return_value = {
        "id": community_uuid,
        "slug": community_slug,
        "metadata": sample_metadata,
        "links": {
            "self": f"{sample_host_name}/api/communities/{id}",
        }
    }
    mock_get = mocker.patch("requests.get",return_value=mock_response)

    #now make api call
    response = invenioAPI.get_community(sample_host_name,sample_token,community_slug)

    #assert correct behaviour
    assert response.status_code == 200
    assert response.json() == mock_response.json.return_value

    #verify call
    mock_get.assert_called_once()
    call_args = mock_get.call_args#get all call arguments
    
    #compare urls
    expected_url = f"{sample_host_name}/api/communities/{id}"
    called_url = call_args[0][0]
    assert called_url == expected_url, f"Expected URL: {expected_url}, Actual URL: {called_url}"

    #compare headers,  no body to check for this
    called_headers = call_args[1]['headers']
    expected_headers = {"Authorization": f"Bearer {sample_token}"}
    assert called_headers == expected_headers

def test_valid_submit_record_to_community(mocker,sample_host_name,sample_metadata,sample_record_id,sample_token):
    mock_response: requests.Response = mocker.Mock()
    mock_response.status_code = 200

    #keep most relevant data
    request_id = "12345"
    community_uuid = "a1b2c3"
    mock_response.json.return_value = {
        "links": {
            "actions": {
            "submit": f"{sample_host_name}/api/requests/{request_id}/actions/submit"
            },
            "comments": f"{sample_host_name}/api/requests/{request_id}/comments",
            "self": f"{sample_host_name}/api/requests/{request_id}",
            "timeline": f"{sample_host_name}/api/requests/{request_id}/timeline"
        },
        "receiver": {
            "community": community_uuid
        }
    }
    mock_put = mocker.patch("requests.put",return_value=mock_response)

    #now make api call
    response = invenioAPI.submit_record_to_community(sample_host_name,sample_token,community_uuid,sample_record_id)

    #assert correct behaviour
    assert response.status_code == 200
    assert response.json() == mock_response.json.return_value

    #verify call
    mock_put.assert_called_once()
    call_args = mock_put.call_args#get all call arguments
    
    #compare urls
    expected_url = f"{sample_host_name}/api/records/{sample_record_id}/draft/review"
    called_url = call_args[0][0]
    assert called_url == expected_url, f"Expected URL: {expected_url}, Actual URL: {called_url}"

    #compare headers
    called_headers = call_args[1]['headers']
    expected_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {sample_token}"
    }
    assert called_headers == expected_headers

    #compare body
    expected_data = {
        "receiver" : {
            "community": f"{community_uuid}"
        },
        "type": "community-submission"
    }
    called_body = call_args[1]['json']
    assert called_body == expected_data

def test_valid_submit_record_for_review(mocker,sample_host_name,sample_record_id,sample_token):
    mock_response: requests.Response = mocker.Mock()
    mock_response.status_code = 202

    mock_response.json.return_value = {}
    mock_post = mocker.patch("requests.post",return_value=mock_response)

    #now make api call
    payload = {
        "content": "TEST",
        "format": "html"
    }
    response = invenioAPI.submit_record_for_review(sample_host_name,sample_token,sample_record_id,payload)

    #assert correct behaviour
    assert response.status_code == 202
    assert response.json() == mock_response.json.return_value

    #verify call
    mock_post.assert_called_once()
    call_args = mock_post.call_args#get all call arguments
    
    #compare urls
    expected_url = sample_host_name + f"/api/records/{sample_record_id}/draft/actions/submit-review"
    called_url = call_args[0][0]
    assert called_url == expected_url, f"Expected URL: {expected_url}, Actual URL: {called_url}"

    #copmare headers
    called_headers = call_args[1]['headers']
    expected_headers = {"Authorization": f"Bearer {sample_token}"}
    assert called_headers == expected_headers

    #compare body
    expected_data = {"payload": payload}
    called_body = call_args[1]['json']
    assert called_body == expected_data

def test_valid_get_record(mocker,sample_host_name,sample_metadata, sample_record_id,sample_token):
    mock_response: requests.Response = mocker.Mock()
    mock_response.status_code = 200
    
    #include critical details in response
    mock_response.json.return_value = {
        "metadata": sample_metadata,
        "id": sample_record_id,
        "links": {
            "latest": f"{sample_host_name}/api/records/{sample_record_id}/versions/latest",
            "versions": f"{sample_host_name}/api/records/{sample_record_id}/versions",
            "self_html": f"{sample_host_name}/uploads/{sample_record_id}",
            "publish": f"{sample_host_name}/api/records/{sample_record_id}/draft/actions/publish",
            "latest_html": f"{sample_host_name}/records/{sample_record_id}/latest",
            "self": f"{sample_host_name}/api/records/{sample_record_id}/draft",
            "files": f"{sample_host_name}/api/records/{sample_record_id}/draft/files",
            "access_links": f"{sample_host_name}/api/records/{sample_record_id}/access/links",
            "review": f"{sample_host_name}/api/records/{sample_record_id}/draft/review", #not included in draft docs, but is in quickstart docs
        }
    }
    mock_get = mocker.patch("requests.get",return_value=mock_response)

    #now test api call
    response = invenioAPI.get_record(sample_host_name,sample_token,sample_record_id)

    # check behaviour
    assert response.status_code == 200
    assert response.json() == mock_response.json.return_value

    # verify call
    mock_get.assert_called_once()
    call_args = mock_get.call_args  # get all call arguments
    
    # Compare URLs
    expected_url = sample_host_name + f"/api/records/{sample_record_id}/draft"
    called_url = call_args[0][0]
    assert called_url == expected_url, f"Expected URL: {expected_url}, Actual URL: {called_url}"

    # Compare headers, no body in this one
    called_headers = call_args[1]['headers']
    expected_headers = {"Authorization": f"Bearer {sample_token}"}
    assert called_headers == expected_headers

def test_valid_delete_review_request(mocker,sample_host_name,sample_metadata, sample_record_id,sample_token):
    mock_response: requests.Response = mocker.Mock()
    mock_response.status_code = 204
    
    #include critical details in response
    mock_response.json.return_value = {}
    mock_delete = mocker.patch("requests.delete",return_value=mock_response)

    #now test api call
    response = invenioAPI.delete_review_request(sample_host_name,sample_token,sample_record_id)

    # check behaviour
    assert response.status_code == 204
    assert response.json() == mock_response.json.return_value

    # verify call
    mock_delete.assert_called_once()
    call_args = mock_delete.call_args  # get all call arguments
    
    # Compare URLs
    expected_url = sample_host_name + f"/api/records/{sample_record_id}/draft/review"
    called_url = call_args[0][0]
    assert called_url == expected_url, f"Expected URL: {expected_url}, Actual URL: {called_url}"

    # Compare headers, no body in this one
    called_headers = call_args[1]['headers']
    expected_headers = {"Authorization": f"Bearer {sample_token}"}
    assert called_headers == expected_headers

def test_valid_cancel_review_request(mocker,sample_host_name,sample_metadata, sample_record_id,sample_token):
    mock_response: requests.Response = mocker.Mock()
    mock_response.status_code = 200
    
    #include critical details in response
    mock_response.json.return_value = {}
    mock_post = mocker.patch("requests.post",return_value=mock_response)

    #now test api call
    request_id = "1234"
    payload = {"content": "Didn't mean to do that!", "format": "html"}
    response = invenioAPI.cancel_review_request(sample_host_name,sample_token,request_id,payload)

    # check behaviour
    assert response.status_code == 200
    assert response.json() == mock_response.json.return_value

    # verify call
    mock_post.assert_called_once()
    call_args = mock_post.call_args  # get all call arguments
    
    # Compare URLs
    expected_url = sample_host_name + f"/api/requests/{request_id}/actions/cancel"
    called_url = call_args[0][0]
    assert called_url == expected_url, f"Expected URL: {expected_url}, Actual URL: {called_url}"

    # Compare headers, no body in this one
    called_headers = call_args[1]['headers']
    expected_headers = {"Authorization": f"Bearer {sample_token}"}
    assert called_headers == expected_headers

    #compare body
    expected_data = {"payload": payload}
    called_body = call_args[1]['json']
    assert called_body == expected_data