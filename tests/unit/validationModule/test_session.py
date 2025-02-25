from typing import List
from NekUpload.validationModule.session import ValidateSession

def test_schema(valid_session_XML_files,nektar_session_schema):
    session_xml_list: List[str] = valid_session_XML_files
    nektar_schema: str = nektar_session_schema

    for xml in session_xml_list:
        checker = ValidateSession(xml)
        assert (checker.is_valid_xml(xml,nektar_schema))

def test_validate(valid_session_XML_files):
    session_xml_list: List[str] = valid_session_XML_files
    
    for xml in session_xml_list:
        checker = ValidateSession(xml)
        
        try:
            assert (checker.validate())
        except:
            assert False, f"Validation failed for XML file: {xml}. Should have thrown an error upon failure, but didn't"