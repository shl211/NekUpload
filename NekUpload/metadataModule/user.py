from abc import ABC,abstractmethod
from typing import Dict,Any

class UserInfo(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_info(self) -> Dict[str,Any]:
        pass

class InvenioPersonInfo(UserInfo):
    """Class describing a person, as specified by Invenio RDM metadata schema
    """
    def __init__(self):
        self.info: Dict[str,Any] = {}
        self.info["type"] = "personal"

    def get_info(self):
        return self.info

    def set_given_name(self,name: str) -> None:
        self.info["given_name"] = name

    def set_family_name(self,name: str) -> None:
        self.info["family_name"] = name

    def add_identifiers(self,scheme:str,identifier:str) -> None:
        #do nothing for now
        pass

class InvenioOrgInfo(UserInfo):
    def __init__(self):
        self.info: Dict[str,Any] = {}
        self.info["type"] = "organizational"

    def get_info(self):
        return self.info

    def set_name(self,name:str):
        self.info["name"] = name

    def add_identifiers(self,scheme:str,identifier:str) -> None:
        #do nothing for now
        pass