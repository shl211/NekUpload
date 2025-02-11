from NekUpload.metadataModule.invenioMetadata import InvenioMetadata
from NekUpload.metadataModule.user import InvenioPersonInfo,InvenioOrgInfo
import pytest

@pytest.fixture
def default_metadata() -> InvenioMetadata:
    title = "TEST TITLE"
    publication_date = "2020-11-10"
    creator1 = InvenioPersonInfo("Boris","Johnson")
    creators = [creator1]

    metadata = InvenioMetadata(title,publication_date,creators)
    return metadata

def test_constructor_one_creator():
    
    title = "TEST TITLE"
    publication_date = "2020-11-10"
    creator1 = InvenioPersonInfo("Boris","Johnson")
    creators = [creator1]

    metadata = InvenioMetadata(title,publication_date,creators)
    metadata_payload = metadata.get_metadata_payload()

    assert metadata_payload["title"] == title
    assert metadata_payload["publication_date"] == publication_date

    expected_creators_payload = [
            {
            "person_or_org": {
                "given_name": "Boris",
                "family_name": "Johnson",
                "type": "personal"
            }},
        ]

    assert expected_creators_payload == metadata_payload["creators"]

def test_constructor_two_creators():
    
    title = "TEST TITLE"
    publication_date = "2020-11-10"
    creator1 = InvenioPersonInfo("Donald","Trump")
    creator2 = InvenioPersonInfo("Jong Un","Kim")
    creators = [creator1,creator2]

    metadata = InvenioMetadata(title,publication_date,creators)
    metadata_payload = metadata.get_metadata_payload()

    assert metadata_payload["title"] == title
    assert metadata_payload["publication_date"] == publication_date

    expected_creators_payload = [
            {
            "person_or_org": {
                "given_name": "Donald",
                "family_name": "Trump",
                "type": "personal"
            }
            },
            {
            "person_or_org": {
                "given_name": "Jong Un",
                "family_name": "Kim",
                "type": "personal"
            }
            }
        ]
    
    #GPT generated
    #Lists are order sensitive, so do this to get around this for comparison
    #just need to make sure list of dicts is valid
    assert sorted(expected_creators_payload, key=lambda x: sorted(x["person_or_org"].items())) == \
           sorted(metadata_payload["creators"], key=lambda x: sorted(x["person_or_org"].items()))
    
def test_add_version(default_metadata):

    metadata: InvenioMetadata = default_metadata
    version = "v1.2.3"
    metadata.add_version(version)
    metadata_payload = metadata.get_metadata_payload()

    assert metadata_payload["version"] == version

def test_add_version(default_metadata):
    metadata: InvenioMetadata = default_metadata
    version = "v1.2.3"
    metadata.add_version(version)
    metadata_payload = metadata.get_metadata_payload()

    assert metadata_payload["version"] == version

def test_add_description(default_metadata):
    metadata: InvenioMetadata = default_metadata
    description = "This is a test description"
    metadata.add_description(description)
    metadata_payload = metadata.get_metadata_payload()

    assert metadata_payload["description"] == description

def test_add_publisher(default_metadata):
    metadata: InvenioMetadata = default_metadata
    publisher = "InvenioRDM"
    metadata.add_publisher(publisher)
    metadata_payload = metadata.get_metadata_payload()

    assert metadata_payload["publisher"] == publisher
