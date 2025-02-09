import pytest
import requests
from NekUpload.db import invenioRDM
from typing import Dict,Any

#here we unit test each individual api call, even if they are private functions
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
    mocker.patch("requests.post",return_value=mock_response)

    #now test api call
    db = invenioRDM()
    response = db._create_draft_record(sample_host_name,sample_token,sample_metadata)

    #assert for only information that code needs
    assert response.status_code == 201
    test_data = response.json()
    assert(test_data["id"] == sample_record_id)
    assert(test_data["metadata"] == sample_metadata)
    assert(test_data["links"]["publish"] == f"{sample_host_name}/api/records/{sample_record_id}/draft/actions/publish")
    assert(test_data["links"]["self"] == f"{sample_host_name}/api/records/{sample_record_id}/draft")
    assert(test_data["links"]["files"] == f"{sample_host_name}/api/records/{sample_record_id}/draft/files")
    assert(test_data["links"]["review"] == f"{sample_host_name}/api/records/{sample_record_id}/draft/review")

@pytest.mark.skip
def test_invalid_create_draft_record(mocker,sample_host_name,sample_metadata,sample_record_id,sample_token):
    pass

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
    mocker.patch("requests.post",return_value=mock_response)

    #now test api call
    db = invenioRDM()
    data = [{"key": "test.txt"}]
    url = f"{sample_host_name}/api/records/{sample_record_id}/draft/files"
    response = db._prepare_upload(url,sample_token,"test.txt")

    #assert for only information that code needs
    assert response.status_code == 201
    test_data = response.json()
    file_data = test_data["entries"][0]
    assert(file_data["key"] == "test.txt")
    assert(file_data["links"]["content"] == f"{sample_host_name}/api/records/{sample_record_id}/files/text.txt/content")
    assert(file_data["links"]["self"] == f"{sample_host_name}/api/records/{sample_record_id}/files/text.txt")
    assert(file_data["links"]["commit"] == f"{sample_host_name}/api/records/{sample_record_id}/files/text.txt/commit")

@pytest.mark.skip
def test_invalid_prepare_file_upload(mocker,sample_host_name,sample_metadata,sample_record_id,sample_token):
    pass

def test_valid_upload_file(mocker,sample_host_name,sample_record_id,sample_token):
    mock_response: requests.Response = mocker.Mock()
    mock_response.status_code = 200

    #include critical details in response
    file = "ADR_2D_TriQuad.xml"
    file_path = f"datasets/ADRSolver/{file}" #relative to tests root
    mock_response.json.return_value = {
        "key": "test.txt",
        "status": "pending",
        "links": {
            "content": f"{sample_host_name}/api/records/{sample_record_id}/draft/files/{file}/content",
            "self": f"{sample_host_name}/api/records/{sample_record_id}/draft/files/{file}",
            "commit": f"{sample_host_name}/api/records/{sample_record_id}/draft/files/{file}/commit"
        }
    }
    mocker.patch("requests.put",return_value=mock_response)

    #now test api call
    db = invenioRDM()
    data = [{"key": "test.txt"}]
    url = f"{sample_host_name}/api/records/{sample_record_id}/draft/files/{file}/content"
    response = db._do_upload(url,sample_token,file_path)

    #assert for only information that code needs
    assert response.status_code == 200
    test_data = response.json()
    assert(test_data["key"] == "test.txt")
    assert(test_data["links"]["content"] == f"{sample_host_name}/api/records/{sample_record_id}/draft/files/{file}/content")
    assert(test_data["links"]["self"] == f"{sample_host_name}/api/records/{sample_record_id}/draft/files/{file}")
    assert(test_data["links"]["commit"] == f"{sample_host_name}/api/records/{sample_record_id}/draft/files/{file}/commit")

@pytest.mark.skip
def test_invalid_upload_file(mocker,sample_host_name,sample_metadata,sample_record_id,sample_token):
    pass

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
    mocker.patch("requests.post",return_value=mock_response)

    #now make api call
    db = invenioRDM()
    url = f"{sample_host_name}/api/records/{sample_record_id}/draft/files/{file}/commit"
    response = db._commit_upload(url,sample_token,file_path)

    #assert for only information that is needed
    assert response.status_code == 200
    test_data = response.json()
    assert(test_data["key"] == "test.txt")
    assert(test_data["links"]["content"] == f"{sample_host_name}/api/records/{sample_record_id}/draft/files/{file}/content")
    assert(test_data["links"]["self"] == f"{sample_host_name}/api/records/{sample_record_id}/draft/files/{file}")
    assert(test_data["links"]["commit"] == f"{sample_host_name}/api/records/{sample_record_id}/draft/files/{file}/commit")

@pytest.mark.skip
def test_invalid_commit_file(mocker,sample_host_name,sample_record_id,sample_token):
    pass

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
    mocker.patch("requests.post",return_value=mock_response)

    #now make api call
    db = invenioRDM()
    url = f"{sample_host_name}/api/records/{sample_record_id}/draft/actions/publish"
    response = db._publish_draft(url,sample_token)

    #assert for only information that is needed
    assert response.status_code == 202
    test_data = response.json()
    assert test_data["id"] == sample_record_id
    assert test_data["metadata"] == sample_metadata
    assert(test_data["links"]["self"] == f"{sample_host_name}/api/records/{sample_record_id}")
    assert(test_data["links"]["files"] == f"{sample_host_name}/api/records/{sample_record_id}/files")

@pytest.mark.skip
def test_invalid_publish_draft(mocker,sample_host_name,sample_metadata,sample_record_id,sample_token):
    pass

def test_valid_delete_draft(mocker,sample_host_name,sample_metadata,sample_record_id,sample_token):
    mock_response: requests.Response = mocker.Mock()
    mock_response.status_code = 204

    #no content returned 
    mock_response.json.return_value = {}
    mocker.patch("requests.delete",return_value=mock_response)

    #now make api call
    db = invenioRDM()
    url = f"{sample_host_name}/api/records/{sample_record_id}/draft"
    response = db._delete_draft(url,sample_token)

    assert response.status_code == 204

@pytest.mark.skip
def test_invalid_delete_draft(mocker,sample_host_name,sample_metadata,sample_record_id,sample_token):
    pass

def test_valid_get_community(mocker,sample_host_name,sample_metadata,sample_record_id,sample_token):
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
    mocker.patch("requests.get",return_value=mock_response)

    #now make api call
    db = invenioRDM()
    url = f"{sample_host_name}/api/communities/{id}"
    response = db._get_community(url,sample_token,community_slug)

    assert response.status_code == 200

@pytest.mark.skip
def test_invalid_get_community(mocker,sample_host_name,sample_metadata,sample_record_id,sample_token):
    pass

def test_valid_submit_record_to_community(mocker,sample_host_name,sample_metadata,sample_record_id,sample_token):
    mock_response: requests.Response = mocker.Mock()
    mock_response.status_code = 200

    #keep most relevasnte data
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
    mocker.patch("requests.put",return_value=mock_response)

    #now make api call
    db = invenioRDM()
    url = f"{sample_host_name}/api/records/{sample_record_id}/draft/review"
    response = db._submit_record_to_community(url,sample_token,community_uuid)

    assert response.status_code == 200
    
@pytest.mark.skip
def test_invalid_submit_record_to_community(mocker,sample_host_name,sample_metadata,sample_record_id,sample_token):
    pass

def test_valid_submit_record_for_review(mocker,sample_host_name,sample_metadata,sample_record_id,sample_token):
    mock_response: requests.Response = mocker.Mock()
    mock_response.status_code = 202

    mock_response.json.return_value = {}
    mocker.patch("requests.post",return_value=mock_response)

    #now make api call
    db = invenioRDM()
    response = db._submit_record_for_review(sample_host_name,sample_token)

    assert response.status_code == 202

@pytest.mark.skip
def test_invalid_submit_record_for_review(mocker,sample_host_name,sample_metadata,sample_record_id,sample_token):
    pass