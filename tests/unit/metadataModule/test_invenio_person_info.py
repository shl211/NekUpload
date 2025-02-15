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

def test_serialisation():
    given_name = "John"
    family_name = "Smith"

    user_info = InvenioPersonInfo(given_name,family_name)
    
    #create an identifier
    orcid = "0000-0002-1694-233X"
    identifier = Identifier(orcid,IdentifierType.ORCID)

    user_info.add_identifier(identifier)

    json: Dict[str,Any] = user_info.to_json_serialisable()

    json_expected = {
        "type": "personal",
        "given_name": given_name,
        "family_name": family_name,
        "identifiers": [identifier.to_json_serialisable()]
    }

    assert json == json_expected

def test_deserialisation():    
    #create an identifier
    orcid = "0000-0002-1694-233X"
    identifier = Identifier(orcid,IdentifierType.ORCID)

    json = {
        "type": "personal",
        "given_name": "John",
        "family_name": "Smith",
        "identifiers": [identifier.to_json_serialisable()]
    }

    person = InvenioPersonInfo.from_json(json)

    assert person.given_name == json["given_name"]
    assert person.family_name == json["family_name"]
    assert len(person.identifiers) == 1
    assert person.identifiers[0].id == identifier.get_id()
    assert person.identifiers[0].id_type == identifier.get_id_type()

def test_same():
    given_name = "Winston"
    last_name = "Churchill"

    person1 = InvenioPersonInfo(given_name,last_name)
    person2 = InvenioPersonInfo(given_name,last_name)

    assert person1 == person2

    orcid = "0000-0002-1694-233X"
    identifier = Identifier(orcid,IdentifierType.ORCID)

    person1.add_identifier(identifier)
    person2.add_identifier(identifier)

    assert person1 == person2

def test_diff_case1():
    given_name1 = "Josef"
    last_name1 = "Stalin"
    given_name2 = "Adolf"
    last_name2 = "Hitler"

    person1 = InvenioPersonInfo(given_name1,last_name1)
    person2 = InvenioPersonInfo(given_name2,last_name2)

    assert person1 != person2

def test_diff_case2():
    given_name = "Josef"
    last_name = "Stalin"

    person1 = InvenioPersonInfo(given_name,last_name)
    person2 = InvenioPersonInfo(given_name,last_name)

    id1 = "0000-0001-5109-3700"
    id2 = "0000-0002-1825-0097"

    person1.add_identifier(Identifier(id1,IdentifierType.ORCID))
    person2.add_identifier(Identifier(id2,IdentifierType.ORCID))

    assert person1 != person2