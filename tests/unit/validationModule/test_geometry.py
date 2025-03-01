from NekUpload.validationModule.geometry import ValidateGeometry
from typing import List
from NekUpload.validationModule.custom_exceptions import HDF5SchemaException,GeometryFileException

def test_check_schema_valid(valid_geometry_HDF5_files):
    nekg_files: List[str] = valid_geometry_HDF5_files
    
    for file in nekg_files:
        checker = ValidateGeometry(file)
        try:
            checker.check_schema()
        except Exception as e:
            assert False, f"Schema check failed for {file} when it should have succeeded: {e}"

def test_check_schema_invalid_geometry(valid_output_fld_HDF5_files):
    invalid_nekg_files: List[str] = valid_output_fld_HDF5_files
    
    for file in invalid_nekg_files:
        checker = ValidateGeometry(file)
        try:
            checker.check_schema()
        except HDF5SchemaException:
            pass #expected failure
        except Exception as e:
            assert False, f"Schema check failed for {file} when it should have succeeded: {e}"

def test_check_schema_invalid_hdf5(valid_session_XML_files):
    invalid_nekg_files: List[str] = valid_session_XML_files
    
    for file in invalid_nekg_files:
        checker = ValidateGeometry(file)
        try:
            checker.check_schema()
        except GeometryFileException:
            pass #expected failure
        except Exception as e:
            assert False, f"Schema check failed for {file} when it should have succeeded: {e}"