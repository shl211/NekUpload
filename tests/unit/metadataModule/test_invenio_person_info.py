from NekUpload.metadataModule.user import InvenioPersonInfo
from typing import Dict,Any

def test_add_set_given_name():
    given_name = "John"
    family_name = "Smith"

    user_info = InvenioPersonInfo(given_name,family_name)

    info: Dict[str,Any] = user_info.get_info()

    assert info["given_name"] == given_name
    assert info["family_name"] == family_name
    assert info["type"] == "personal"
