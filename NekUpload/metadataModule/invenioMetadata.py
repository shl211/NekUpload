from .metadata import Metadata
from typing import Dict,Any,List,Union
from .user import UserInfo

class InvenioMetadata(Metadata):
    def __init__(self,title: str,publication_date:str,creators: List[UserInfo],resource_type: str="dataset"):
        #mandatory fields
        self.title = title
        self.publication_date = publication_date
        self.creators: List[UserInfo] = creators
        self.resource_type = resource_type

        #optional fields
        self.version: str = None
        self.description: str = None
        self.publisher: str = None

    def get_metadata_payload(self) -> Dict[str,Any]:
        creators_payload: List[Dict[str,Any]] = []
        for creator in self.creators:
            creators_payload.append({
                "person_or_org": creator.get_info()
            })
        
        data = {
            "title": self.title,
            "publication_date": self.publication_date,
            "resource_type": {"id": self.resource_type},
            "creators": creators_payload
        }

        if self.version:
            data["version"] = self.version
        
        if self.description:
            data["description"] = self.description

        if self.publisher:
            data["publisher"] = self.publisher

        return data

    def add_version(self, version: str) -> None:
        self.version = version

    def add_description(self, description: str) -> None:
        self.description = description

    def add_publisher(self, publisher: str="InvenioRDM") -> None:
        self.publisher = publisher

    def to_json_serialisable(self):        
        data = {
            "title": self.title,
            "publication_date": self.publication_date,
            "resource_type": self.resource_type,
            "creators": [creator.to_json_serialisable() for creator in self.creators]
        }

        if self.version:
            data["version"] = self.version
        
        if self.description:
            data["description"] = self.description

        if self.publisher:
            data["publisher"] = self.publisher

        return data    
    
    @classmethod
    def from_json(cls,data: Dict[str,Any]) -> 'InvenioMetadata':
        title = data["title"]
        publication_date = data["publication_date"]
        resource_type = data["resource_type"]
        creators: List[UserInfo] = [UserInfo.from_json(creator) for creator in data["creators"]]

        metadata = InvenioMetadata(title,publication_date,creators,resource_type)

        #only add the following optional data if present in serialisation
        if version := data.get("version",None):
            metadata.add_version(version)

        if description := data.get("description",None):
            metadata.add_description(description)

        if publisher := data.get("publisher",None):
            metadata.add_publisher(publisher)

        return metadata