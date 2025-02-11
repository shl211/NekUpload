from NekUpload.metadataModule.user import InvenioOrgInfo
from typing import Dict,Any

def test_add_set_name():
    org_name = "Imperial College London"
    org_info = InvenioOrgInfo(org_name)
    
    info: Dict[str,Any] = org_info.get_info()
    
    assert info["name"] == org_name
    assert info["type"] == "organizational"