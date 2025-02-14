from abc import ABC,abstractmethod
from typing import Dict,Any,List,Set,Type
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

        if not isinstance(given_name, str) or not isinstance(family_name, str):
            msg = "Given name and family name must be strings."
            logging.error(msg)
            raise TypeError(msg)
        
        self.id_schemes: Set[IdentifierType] = set()

        self.type: str = "personal"
        self.given_name: str = given_name
        self.family_name: str = family_name
        self.identifiers: List[Identifier] = []

    def add_identifier(self,identifier: Identifier) -> None:
        """_summary_

        Args:
            identifier (Identifier): _description_

        Raises:
            ValueError: _description_
        """
        id_type: IdentifierType = identifier.get_id_type()
        
        if id_type in self.id_schemes:
            raise ValueError(f"Cannot have duplicate identifiers of same type for one organisation {id_type}")        

        self.id_schemes.add(id_type)
        self.identifiers.append(identifier)

    def get_info(self) -> Dict[str,Any]:
        """_summary_

        Returns:
            Dict[str,Any]: _description_
        """

        identifier_payload = []
        for identifier in self.identifiers:
            payload = {
                "scheme": identifier.get_id_type().value.lower(),
                "identifier": identifier.get_id()
            }
            identifier_payload.append(payload)

        data = {
            "type": self.type,
            "given_name": self.given_name,
            "family_name": self.family_name,
        }

        if identifier_payload != []:
            data["identifiers"] = identifier_payload 

        return data
    
    def __str__(self):
        return f"Person: {self.given_name} {self.family_name}"

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
        self.type: str = "organizational"
        self.name: str = name
        self.identifiers: List[Identifier] = []

    def get_info(self) -> Dict[str,Any]:
        """_summary_

        Returns:
            Dict[str,Any]: _description_
        """

        identifier_payload = []
        for identifier in self.identifiers:
            payload = {
                "scheme": identifier.get_id_type().value.lower(),
                "identifier": identifier.get_id()
            }
            identifier_payload.append(payload)

        data = {
            "type": self.type,
            "name": self.name,
        }

        if identifier_payload != []:
            data["identifiers"] = identifier_payload 

        return data
    
    def add_identifier(self,identifier: Identifier) -> None:
        """_summary_

        Args:
            identifier (Identifier): _description_

        Raises:
            ValueError: _description_
        """
        id_type: IdentifierType = identifier.get_id_type()
        
        if id_type in self.id_schemes:
            raise ValueError(f"Cannot have duplicate identifiers of same type for one organisation {id_type}")        

        self.id_schemes.add(id_type)
        self.identifiers.append(identifier)

    def __str__(self):
        return f"Organisation: {self.name}"