from NekUpload.metadataModule.relations import *

def test_to_json():
    
    id = "123456"
    relation = Relations(id,RelationsSchemes.DOI,RelationType.CONTINUES,ResourceType.DATASET)
    
    expected_json = {
        "identifier": id,
        "scheme": "doi",
        "relation_type": {
            "id": "continues",
            "title": {
                "en": "Continues"
            }
        },
        "resource_type": {
            "id": "dataset",
            "title": {
                "en": "Dataset"
            }
        }
    }
    
    assert expected_json == relation.to_json()

def test_from_json():
    json_data = {
        "identifier": "123456",
        "scheme": "doi",
        "relation_type": {
            "id": "continues",
            "title": {
                "en": "Continues"
            }
        },
        "resource_type": {
            "id": "dataset",
            "title": {
                "en": "Dataset"
            }
        }
    }

    relation = Relations.from_json(json_data)

    assert relation.id == "123456"
    assert relation.scheme == RelationsSchemes.DOI
    assert relation.relation_type == RelationType.CONTINUES
    assert relation.resource_type == ResourceType.DATASET
