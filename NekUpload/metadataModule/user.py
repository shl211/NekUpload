from abc import ABC,abstractmethod
from typing import Dict,Any,List,Set
import logging
from .identifier import Identifier,IdentifierType

class UserInfo(ABC):
    @abstractmethod
    def get_info(self) -> Dict[str,Any]:
        pass

class InvenioPersonInfo(UserInfo):
    def __init__(self, given_name: str, family_name: str) -> None:
        
        self.id_schemes: Set[IdentifierType] = set()

        if not isinstance(given_name, str) or not isinstance(family_name, str):
            msg = "Given name and family name must be strings."
            logging.error(msg)
            raise TypeError(msg)
        
        self.info: Dict[str, Any] = {
            "type": "personal",
            "given_name": given_name, 
            "family_name": family_name
            }

    def add_identifier(self,identifier: Identifier) -> None:
        id: str = identifier.get_id()
        id_type: IdentifierType = identifier.get_id_type()

        id_payload = {
            "scheme": id_type.value.lower(),
            "identifier": id
        }
        
        if id_type in self.id_schemes:
            raise ValueError(f"Cannot have duplicate identifiers of same type for one person {id_type}")        

        self.id_schemes.add(id_type)
        self.info.setdefault("identifiers", []).append(id_payload)

    def get_info(self) -> Dict[str,Any]:
        return self.info
    
class InvenioOrgInfo(UserInfo):
    def __init__(self, name: str) -> None:
        self.id_schemes: Set[IdentifierType] = set()
        
        self.info: Dict[str,Any] = {
            "type": "organizational",
            "name": name
        }

    def get_info(self) -> Dict[str,Any]:
        return self.info
    
    def add_identifier(self,identifier: Identifier) -> None:
        id: str = identifier.get_id()
        id_type: IdentifierType = identifier.get_id_type()

        id_payload = {
            "scheme": id_type.value.lower(),
            "identifier": id
        }
        
        if id_type in self.id_schemes:
            raise ValueError(f"Cannot have duplicate identifiers of same type for one organisation {id_type}")        

        self.id_schemes.add(id_type)
        self.info.setdefault("identifiers", []).append(id_payload)