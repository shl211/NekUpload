from NekUpload.metadataModule.user import InvenioOrgInfo
from typing import Dict,Any

def test_add_set_name():
    org_info = InvenioOrgInfo()
    org_info.set_name("Imperial College London")
    
    info: Dict[str,Any] = org_info.get_info()
    assert info["name"] == "Imperial College London"

def test_get_info():
    org_info = InvenioOrgInfo()
    org_info.set_name("Imperial College London")

    info: Dict[str,Any] = org_info.get_info()
    assert info["name"] == "Imperial College London"
    assert info["type"] == "organizational"
