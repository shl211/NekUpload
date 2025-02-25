from typing import List,Any
from lxml import etree

class XMLSchemaException(Exception):
    """Exception raised for errors in the XML schema."""
    
    def __init__(self, file: str, schema_error_log: List[etree._LogEntry],message="Error in the XML schema"):        
        errors = "\n".join(f"Line {error.line}, Col {error.column}: {error.message}" for error in schema_error_log)
        full_message = f"{message} for file {file}\n{errors}" if errors else f"{message} for file {file}\n(No detailed errors found)"
        
        super().__init__(full_message)