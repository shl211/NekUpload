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