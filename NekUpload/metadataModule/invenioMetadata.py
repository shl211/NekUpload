from .metadata import Metadata
from typing import Dict,Any,List
from .user import UserInfo

class InvenioMetadata(Metadata):
    def __init__(self,title: str,publication_date:str,creators: List[UserInfo],resource_type: str="dataset"):
        
        creators_payload: List[Dict[str,Any]] = []
        for creator in creators:
            creators_payload.append({
                "person_or_org": creator.get_info()
            })
                
        self.info: Dict[str,Any] = {
            "title": title,
            "publication_date": publication_date,
            "resource_type": {"id": resource_type},
            "creators": creators_payload
        }

    def get_metadata_payload(self) -> Dict[str,Any]:
        return self.info

    def add_version(self, version: str) -> None:
        self.info["version"] = version

    def add_description(self, description: str) -> None:
        self.info["description"] = description

    def add_publisher(self, publisher: str="InvenioRDM") -> None:
        self.info["publisher"] = publisher