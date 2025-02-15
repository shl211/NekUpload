from NekUpload.metadataModule.user import InvenioOrgInfo,UserInfo,InvenioPersonInfo
from NekUpload.metadataModule.identifier import Identifier,IdentifierType
from typing import Union

def test_deserialisation_factory_org():    
    orcid = "0000-0002-1694-233X"
    identifier = Identifier(orcid,IdentifierType.ORCID)

    json = {
        "type": "organizational",
        "name": "Imperial College London",
        "identifiers": [identifier.to_json_serialisable()]
    }

    user_info: Union['InvenioOrgInfo','InvenioPersonInfo'] = UserInfo.from_json(json)

    assert isinstance(user_info,InvenioOrgInfo)

def test_deserialisation_factory_person():
    #create an identifier
    orcid = "0000-0002-1694-233X"
    identifier = Identifier(orcid,IdentifierType.ORCID)

    json = {
        "type": "personal",
        "given_name": "John",
        "family_name": "Smith",
        "identifiers": [identifier.to_json_serialisable()]
    }

    user_info: Union['InvenioOrgInfo','InvenioPersonInfo'] = UserInfo.from_json(json)

    assert isinstance(user_info,InvenioPersonInfo)