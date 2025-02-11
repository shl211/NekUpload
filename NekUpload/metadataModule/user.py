from abc import ABC,abstractmethod
from typing import Dict,Any
import logging

class UserInfo(ABC):
    @abstractmethod
    def get_info(self) -> Dict[str,Any]:
        pass

class InvenioPersonInfo(UserInfo):
    def __init__(self, given_name: str, family_name: str) -> None:
        
        if not isinstance(given_name, str) or not isinstance(family_name, str):
            msg = "Given name and family name must be strings."
            logging.error(msg)
            raise TypeError(msg)
        
        self.info: Dict[str, Any] = {
            "type": "personal",
            "given_name": given_name, 
            "family_name": family_name
            }

    def get_info(self) -> Dict[str,Any]:
        return self.info
    
class InvenioOrgInfo(UserInfo):
    def __init__(self, name: str) -> None:
        self.info: Dict[str,Any] = {
            "type": "organizational",
            "name": name
        }

    def get_info(self) -> Dict[str,Any]:
        return self.info