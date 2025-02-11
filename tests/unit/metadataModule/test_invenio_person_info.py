from NekUpload.metadataModule.user import InvenioPersonInfo
from NekUpload.metadataModule.identifier import Identifier,IdentifierType
from typing import Dict,Any
import pytest

def test_constructor():
    given_name = "John"
    family_name = "Smith"

    user_info = InvenioPersonInfo(given_name,family_name)

    info: Dict[str,Any] = user_info.get_info()

    assert info["given_name"] == given_name
    assert info["family_name"] == family_name
    assert info["type"] == "personal"

def test_add_one_identifier():
    given_name = "John"
    family_name = "Smith"

    user_info = InvenioPersonInfo(given_name,family_name)
    
    #create an identifier
    orcid = "0000-0002-1694-233X"
    identifier = Identifier(orcid,IdentifierType.ORCID)

    user_info.add_identifier(identifier)

    info: Dict[str,Any] = user_info.get_info()
    
    assert info["identifiers"][0]["scheme"] == "orcid"
    assert info["identifiers"][0]["identifier"] == orcid

def test_add_duplicate_identifiers():
    given_name = "John"
    family_name = "Smith"

    user_info = InvenioPersonInfo(given_name,family_name)
    
    #create a identifiers
    orcid = "0000-0002-1694-233X"
    identifier1 = Identifier(orcid,IdentifierType.ORCID)
    identifier2 = Identifier(orcid,IdentifierType.ORCID)

    user_info.add_identifier(identifier1)

    try:
        user_info.add_identifier(identifier2)
        assert False, "Identifiers of same type cannot both be added"
    except Exception:
        pass

@pytest.mark.skip
def test_add_two_identifier_types():
    pass