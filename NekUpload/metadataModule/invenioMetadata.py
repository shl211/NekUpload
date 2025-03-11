from .metadata import Metadata
from typing import Dict,Any,List,Union
from .user import UserInfo
from .relations import Relations

class InvenioMetadata(Metadata):
    """_summary_

    Args:
        Metadata (_type_): _description_
    """
    def __init__(self,title: str,publication_date:str,creators: List[UserInfo],resource_type: str="dataset"):
        """_summary_

        Args:
            title (str): _description_
            publication_date (str): _description_
            creators (List[UserInfo]): _description_
            resource_type (str, optional): _description_. Defaults to "dataset".
        """
        #mandatory fields
        self.title = title
        self.publication_date = publication_date
        self.creators: List[UserInfo] = creators
        self.resource_type = resource_type

        #optional fields
        self.version: str = None
        self.description: str = None
        self.publisher: str = None
        self.related_identifiers: List[Relations] = []

    def get_metadata_payload(self) -> Dict[str,Any]:
        """_summary_

        Returns:
            Dict[str,Any]: _description_
        """
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

        if self.related_identifiers:
            relation_list_json = [relation.to_json() for relation in self.related_identifiers]
            data["related_identifiers"] = relation_list_json

        return data

    def add_version(self, version: str) -> None:
        """_summary_

        Args:
            version (str): _description_
        """
        self.version = version

    def add_description(self, description: str) -> None:
        """_summary_

        Args:
            description (str): _description_
        """
        self.description = description

    def add_publisher(self, publisher: str="InvenioRDM") -> None:
        """_summary_

        Args:
            publisher (str, optional): _description_. Defaults to "InvenioRDM".
        """
        self.publisher = publisher

    def add_related_identifier(self,relation: Relations):
        self.related_identifiers.append(relation)

    def to_json_serialisable(self):        
        """_summary_

        Returns:
            _type_: _description_
        """
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

        if self.related_identifiers:
            relation_list_json = [relation.to_json() for relation in self.related_identifiers]
            data["related_identifiers"] = relation_list_json

        return data    
    
    @classmethod
    def from_json(cls,data: Dict[str,Any]) -> 'InvenioMetadata':
        """_summary_

        Args:
            data (Dict[str,Any]): _description_

        Returns:
            InvenioMetadata: _description_
        """
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

        if related_identifiers := data.get("related_identifiers",None):
            for identifier_json in related_identifiers:
                import logging
                logging.error(identifier_json)
                metadata.add_related_identifier(Relations.from_json(identifier_json))

        return metadata