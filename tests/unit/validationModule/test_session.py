from typing import List,Dict
from NekUpload.validationModule.session import ValidateSession
from NekUpload.validationModule.custom_exceptions import MissingInputFileException,MissingOutputFileException
import os

def test_schema(valid_session_XML_files,nektar_session_schema):
    session_xml_list: List[str] = valid_session_XML_files
    nektar_schema: str = nektar_session_schema

    for xml in session_xml_list:
        checker = ValidateSession(xml)
        assert (checker.is_valid_xml(xml,nektar_schema))

def test_check_schema(valid_session_XML_files):
    session_xml_list: List[str] = valid_session_XML_files
    
    for xml in session_xml_list:
        checker = ValidateSession(xml)
        
        try:
            assert (checker.check_schema())
        except:
            assert False, f"Validation failed for XML file: {xml}. Should have thrown an error upon failure, but didn't"

def test_check_other_files(ADR_dataset_abs_paths):
    datasets: List[Dict[str,str | List[str]]] = ADR_dataset_abs_paths

    for dataset in datasets:
        session: str = dataset["SESSION"]
        geometry: str = dataset["GEOMETRY"]
        chkpoint: List[str] = dataset["CHECKPOINT"]
        output: str = dataset["OUTPUT"]

        all_but_session_files = [os.path.basename(geometry)] + [os.path.basename(chk) for chk in chkpoint] + [os.path.basename(output)]

        validator = ValidateSession(session)
        assert validator.check_file_dependencies(all_but_session_files)   

def test_check_other_files_wrong_nekg(ADR_dataset_abs_paths):
    datasets: List[Dict[str,str | List[str]]] = ADR_dataset_abs_paths

    for dataset in datasets:
        session: str = dataset["SESSION"]
        geometry: str = "wrong.nekg"
        chkpoint: List[str] = dataset["CHECKPOINT"]
        output: str = dataset["OUTPUT"]

        all_but_session_files = [os.path.basename(geometry)] + [os.path.basename(chk) for chk in chkpoint] + [os.path.basename(output)]

        validator = ValidateSession(session)
        try:
            validator.check_file_dependencies(all_but_session_files)
            assert False, "Expected MissingInputFileException but no exception was raised"
        except Exception as e:
            #after checking correct instance, suppress the exception for testing
            assert isinstance(e,MissingInputFileException)

def test_check_other_files_wrong_num_chk(ADR_dataset_abs_paths):
    datasets: List[Dict[str,str | List[str]]] = ADR_dataset_abs_paths

    for dataset in datasets:
        session: str = dataset["SESSION"]
        geometry: str = dataset["GEOMETRY"]
        chkpoint: List[str] = dataset["CHECKPOINT"]
        output: str = dataset["OUTPUT"]

        chkpoint.append("too_many.chk")
        all_but_session_files = [os.path.basename(geometry)] + [os.path.basename(chk) for chk in chkpoint] + [os.path.basename(output)]

        validator = ValidateSession(session)
        try:
            validator.check_file_dependencies(all_but_session_files)
            assert False, "Expected MissingOutputFileException but no exception was raised"
        except Exception as e:
            #after checking correct instance, suppress the exception for testing
            assert isinstance(e,MissingOutputFileException)