from abc import ABC,abstractmethod
from typing import Dict,Any,List
from .user import UserInfo

class Metadata:
    def __init__(self,title: str,publication_date:str,creators: List[UserInfo],resource_type):
        pass

    @abstractmethod
    def get_metadata_payload(self) -> Dict[str,Any]:
        pass

    @abstractmethod
    def add_version(self, version: str) -> None:
        pass

    @abstractmethod
    def add_description(self, description: str) -> None:
        pass

    @abstractmethod
    def add_publisher(self, publisher: str) -> None:
        pass

    @abstractmethod
    def to_json_serialisable(self) -> Dict[str,Any]:
        pass

    @classmethod
    @abstractmethod
    def from_json(cls,data: Dict[str,Any]) -> 'Metadata':
        pass