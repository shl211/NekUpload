from abc import ABC,abstractmethod
from enum import Enum
import re
import logging

class IdentifierType(Enum):
    ORCID = "orcid"
    GND = "gnd"
    ISNI = "isni"
    ROR = "ror"

class Identifier:
    def __init__(self, id: str, id_type: IdentifierType):
        self.id_type: str = id_type

        #"""Will fix at some point
        if not self._check_valid_id(id,id_type):
            msg =f"ID {id} is not of type {id_type}"
            logging.error(msg)
            raise ValueError(msg)
        #"""

        self.id = id
    
    def get_id_type(self) -> IdentifierType:
        return self.id_type
    
    def get_id(self) -> str:
        return self.id
    
    def _check_valid_id(self,id:str,id_type:IdentifierType) -> bool:
        validation_methods = {
            IdentifierType.ORCID: self._is_valid_orcid_id,
            IdentifierType.GND: self._is_valid_gnd_id,
            IdentifierType.ISNI: self._is_valid_isni_id,
            IdentifierType.ROR: self._is_valid_ror_id,
        }
        
        validate = validation_methods.get(id_type)
        if validate:
            return validate(id)
        return False

    def _is_valid_orcid_id(self,id: str) -> bool:
        
        #orcid id of form xxxx-xxxx-xxxx-xxxx, all numbers, last num (checksum) optionally capital 'X' for 10
        pattern = r'^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$'
        if not re.match(pattern, id):
            return False

        base_digits = id.replace("-", "")[:-1]
        calculated_checksum = self._generate_check_digit(base_digits)
        return calculated_checksum == id[-1]    
    
    def _is_valid_gnd_id(self,id:str) -> bool:
        #TODO
        return True
    
    def _is_valid_isni_id(self,id:str) -> bool:
        
        #isni of form xxxxxxxxxxxxxxxx, all numbers (16 of them), last num (checksum) optionally capital 'X' for 10
        pattern = r'^\d{15}[\dX]$'
        if not re.match(pattern, id[:-1]):
            return False

        calculated_checksum = self._generate_check_digit(id[:-1])
        return calculated_checksum == id[-1]    
    
    def _is_valid_ror_id(self,id:str) -> bool:
        #TODO
        return True

    def _generate_check_digit(self,base_digits: str) -> str:
        #checksum code adapted from
        #https://support.orcid.org/hc/en-us/articles/360006897674-Structure-of-the-ORCID-Identifier

        total = 0
        for digit in base_digits:
            total = (total + int(digit)) * 2

        remainder = total % 11
        result = (12 - remainder) % 11
        return "X" if result == 10 else str(result)