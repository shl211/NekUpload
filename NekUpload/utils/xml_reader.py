import logging
from typing import Optional, Type, List
import xml.etree.ElementTree as ET
from .custom_exception import XMLReaderException

class XMLReader:
    def __init__(self, filename: str, mode: str = "r") -> None:
        self.filename = filename
        self.mode = mode
        self.tree: Optional[ET.ElementTree] = None
    
    def __enter__(self) -> "XMLReader":
        try:
            self.tree = ET.parse(self.filename)
            return self # Return XMLReader instance
        except Exception as e:
            logging.fatal(f"Error opening XML file: {e}")
            raise e
        
    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[Type[BaseException]]) -> None:
        self.tree = None

    def get_structure(self) -> List[str]:
        """_summary_

        :raises XMLReaderException: _description_
        :return: _description_
        :rtype: List[str]
        """
        
        if not self.tree:
            raise XMLReaderException("XML tree is not loaded.")
        
        root = self.tree.getroot()
        structure = []

        def traverse(node, path=""):
            current_path = f"{path}/{node.tag}" if path else node.tag
            structure.append(current_path)
            for child in node:
                traverse(child, current_path)
        
        traverse(root)
        return structure
    