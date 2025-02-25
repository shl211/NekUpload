from lxml import etree
from .custom_exceptions import XMLSchemaException

class ValidateSession:
    def __init__(self,file_path: str):
        self.file_path = file_path

    def is_valid_xml(self,xml_file: str,schema_file_path: str) -> bool:
        xsd_file = schema_file_path
        
        with open(xsd_file,"rb") as xsd:
            schema_root = etree.XML(xsd.read())
            schema = etree.XMLSchema(schema_root)

        with open(xml_file,"rb") as xml:
            xml_tree = etree.XML(xml.read())
        
        if schema.validate(xml_tree):
            return True
        else:
            raise XMLSchemaException(self.file_path,schema.error_log)