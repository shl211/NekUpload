from NekUpload.validationModule.output import ValidateOutput
from NekUpload.validationModule.custom_exceptions import HDF5SchemaException,OutputFileException
from typing import List

def test_check_schema_valid(valid_output_fld_HDF5_files):
    fld_files: List[str] = valid_output_fld_HDF5_files
    
    for file in fld_files:
        checker = ValidateOutput(file)
        try:
            checker.check_schema()
        except Exception as e:
            assert False, f"Schema check failed for {file} when it should have succeeded: {e}"

def test_check_schema_invalid_output(valid_geometry_HDF5_files):
    invalid_fld_files: List[str] = valid_geometry_HDF5_files
    
    for file in invalid_fld_files:
        checker = ValidateOutput(file)
        try:
            checker.check_schema()
            assert False, f"Schema check succeeded but should fail {file}: {e}"
        except HDF5SchemaException:
            pass #expected failure
        except Exception as e:
            assert False, f"Schema check failed unpredictably for {file}: {e}"

def test_check_schema_invalid_hdf5(valid_session_XML_files):
    invalid_fld_files: List[str] = valid_session_XML_files
    
    for file in invalid_fld_files:
        checker = ValidateOutput(file)
        try:
            checker.check_schema()
            assert False, f"Schema check succeeded but should fail {file}: {e}"
        except OutputFileException:
            pass #expected failure
        except Exception as e:
            assert False, f"Schema check failed unpredictably for {file}: {e}"