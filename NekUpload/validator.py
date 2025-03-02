from .validationModule import ValidateSession,ValidateOutput,ValidateGeometry
from typing import List
import logging

class NektarValidator:
    def __init__(self,session_file: str, geometry_file: str, output_file: str, chk_files: str,supporting_files: List[str]):        
        self.session_file: str = session_file
        self.geometry_file: str = geometry_file
        self.output_fld_file: str = output_file
        self.output_chk_files: List[str] = chk_files
        self.supporrting_files: List[str] = supporting_files 

        self.session_validator = ValidateSession(self.session_file)
        self.geometry_validator = ValidateGeometry(self.geometry_file)
        self.output_validator = ValidateOutput(self.output_fld_file)

    def validate(self) -> bool:
        
        self.session_validator.check_schema()
        self.geometry_validator.check_schema()
        self.output_validator.check_schema()

        return True
