from NekUpload.metadataModule.user import InvenioOrgInfo
from typing import Dict,Any
from NekUpload.metadataModule.identifier import Identifier,IdentifierType
import pytest

def test_add_set_name():
    org_name = "Imperial College London"
    org_info = InvenioOrgInfo(org_name)
    
    info: Dict[str,Any] = org_info.get_info()
    
    assert info["name"] == org_name
    assert info["type"] == "organizational"

def test_add_one_identifier():
    org_name = "Imperial College London"
    org_info = InvenioOrgInfo(org_name)
    
    #create an identifier
    orcid = "0000-0002-1694-233X"
    identifier = Identifier(orcid,IdentifierType.ORCID)

    org_info.add_identifier(identifier)

    info: Dict[str,Any] = org_info.get_info()
    
    assert info["identifiers"][0]["scheme"] == "orcid"
    assert info["identifiers"][0]["identifier"] == orcid


def test_add_duplicate_identifiers():
    org_name = "Imperial College London"
    org_info = InvenioOrgInfo(org_name)
    
    #create a identifiers
    orcid = "0000-0002-1694-233X"
    identifier1 = Identifier(orcid,IdentifierType.ORCID)
    identifier2 = Identifier(orcid,IdentifierType.ORCID)

    org_info.add_identifier(identifier1)

    try:
        org_info.add_identifier(identifier2)
        assert False, "Identifiers of same type cannot both be added"
    except Exception:
        pass

@pytest.mark.skip
def test_add_two_identifier_types():
    pass

def test_serialisation():
    org_name = "Imperial College London"
    org_info = InvenioOrgInfo(org_name)
    
    #create an identifier
    orcid = "0000-0002-1694-233X"
    identifier = Identifier(orcid,IdentifierType.ORCID)

    org_info.add_identifier(identifier)

    json: Dict[str,Any] = org_info.to_json_serialisable()

    json_expected = {
        "type": "organizational",
        "name": org_name,
        "identifiers": [identifier.to_json_serialisable()]
    }

    assert json == json_expected
    
def test_deserialisation():
    #create an identifier
    orcid = "0000-0002-1694-233X"
    identifier = Identifier(orcid,IdentifierType.ORCID)

    json = {
        "type": "organizational",
        "name": "Imperial College London",
        "identifiers": [identifier.to_json_serialisable()]
    }

    org = InvenioOrgInfo.from_json(json)

    assert org.name == json["name"]
    assert len(org.identifiers) == 1
    assert org.identifiers[0].id == identifier.get_id()
    assert org.identifiers[0].id_type == identifier.get_id_type()

def test_same():
    name = "UCL"

    org1 = InvenioOrgInfo(name)
    org2 = InvenioOrgInfo(name)

    assert org1 == org2

    orcid = "0000-0002-1694-233X"
    identifier = Identifier(orcid,IdentifierType.ORCID)

    org1.add_identifier(identifier)
    org2.add_identifier(identifier)

    assert org1 == org2

def test_diff_case1():
    name1 = "UCL"
    name2 = "KCL"

    org1 = InvenioOrgInfo(name1)
    org2 = InvenioOrgInfo(name2)

    assert org1 != org2

def test_diff_case2():
    name = "UCL"

    org1 = InvenioOrgInfo(name)
    org2 = InvenioOrgInfo(name)

    id1 = "0000-0001-5109-3700"
    id2 = "0000-0002-1825-0097"

    org1.add_identifier(Identifier(id1,IdentifierType.ORCID))
    org2.add_identifier(Identifier(id2,IdentifierType.ORCID))

    assert org1 != org2