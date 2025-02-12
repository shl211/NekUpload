from abc import ABC,abstractmethod
from typing import Dict,Any,List,Set
import logging
from .identifier import Identifier,IdentifierType

class UserInfo(ABC):
    """_summary_

    Args:
        ABC (_type_): _description_
    """
    @abstractmethod
    def get_info(self) -> Dict[str,Any]:
        """_summary_

        Returns:
            Dict[str,Any]: _description_
        """
        pass

class InvenioPersonInfo(UserInfo):
    """_summary_

    Args:
        UserInfo (_type_): _description_
    """
    def __init__(self, given_name: str, family_name: str) -> None:
        """_summary_

        Args:
            given_name (str): _description_
            family_name (str): _description_

        Raises:
            TypeError: _description_
        """
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
        """_summary_

        Args:
            identifier (Identifier): _description_

        Raises:
            ValueError: _description_
        """
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
    """_summary_

    Args:
        UserInfo (_type_): _description_
    """
    def __init__(self, name: str) -> None:
        """_summary_

        Args:
            name (str): _description_
        """
        self.id_schemes: Set[IdentifierType] = set()
        
        self.info: Dict[str,Any] = {
            "type": "organizational",
            "name": name
        }

    def get_info(self) -> Dict[str,Any]:
        """_summary_

        Returns:
            Dict[str,Any]: _description_
        """
        return self.info
    
    def add_identifier(self,identifier: Identifier) -> None:
        """_summary_

        Args:
            identifier (Identifier): _description_

        Raises:
            ValueError: _description_
        """
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