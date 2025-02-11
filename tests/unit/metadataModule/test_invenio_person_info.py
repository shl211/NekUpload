from NekUpload.metadataModule.user import InvenioPersonInfo
from typing import Dict,Any

def test_add_set_given_name():
    user_info = InvenioPersonInfo()
    user_info.set_given_name("John")
    
    info: Dict[str,Any] = user_info.get_info()
    assert info["given_name"] == "John"

def test_add_set_family_name():
    user_info = InvenioPersonInfo()
    user_info.set_family_name("John")
    
    info: Dict[str,Any] = user_info.get_info()
    assert info["family_name"] == "John"

def test_get_info():
    user_info = InvenioPersonInfo()
    user_info.set_given_name("John")
    user_info.set_family_name("Smith")

    info: Dict[str,Any] = user_info.get_info()
    assert info["given_name"] == "John"
    assert info["family_name"] == "Smith"
    assert info["type"] == "personal"
