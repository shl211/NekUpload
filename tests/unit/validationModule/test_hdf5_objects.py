from NekUpload.validationModule.hdf5schema_validator import *
from NekUpload.validationModule.custom_exceptions import HDF5SchemaException,HDF5SchemaExistenceException
import pytest
import h5py
import numpy as np

"""
    TEST GROUP VALIDATOR
"""

def test_hdf5_group_no_attribute(valid_geometry_HDF5_files):
    
    nekg_files: List[str] = valid_geometry_HDF5_files

    for geometry_file in nekg_files:
        group_def = HDF5GroupDefinition("NEKTAR")
        
        with h5py.File(geometry_file,"r") as f:
            assert group_def.validate(f)

def test_hdf5_group_attribute(valid_geometry_HDF5_files):
    
    nekg_files: List[str] = valid_geometry_HDF5_files

    for geometry_file in nekg_files:
        group_def = HDF5GroupDefinition("NEKTAR/GEOMETRY",["FORMAT_VERSION"])
        
        with h5py.File(geometry_file,"r") as f:
            assert group_def.validate(f)

def test_hdf5_group_wrong(valid_geometry_HDF5_files):
    
    nekg_files: List[str] = valid_geometry_HDF5_files

    for geometry_file in nekg_files:
        group_def = HDF5GroupDefinition("NEKTAR/INVALID")
        
        with h5py.File(geometry_file,"r") as f:
            try:
                group_def.validate(f) #should fail
                assert False, f"{geometry_file} should fail, but didn't"
            except HDF5SchemaExistenceException:
                #this is what should happen
                pass
            except HDF5SchemaException as e:
                assert False, f"{geometry_file} did not fail in defined manner: {e}"
            except Exception as e:
                assert False, f"{geometry_file} failed in unpredictable way: {e}"

def test_hdf5_group_missing_attribute(valid_geometry_HDF5_files):
    
    nekg_files: List[str] = valid_geometry_HDF5_files

    for geometry_file in nekg_files:
        group_def = HDF5GroupDefinition("NEKTAR",["NO_ATTRIBUTE"])
        
        with h5py.File(geometry_file,"r") as f:
            try:
                group_def.validate(f) #should fail
                assert False, f"{geometry_file} should fail, but didn't"
            except HDF5SchemaInconsistentException:
                #this is what should happen
                pass
            except HDF5SchemaException as e:
                assert False, f"{geometry_file} did not fail in defined manner: {e}"
            except Exception as e:
                assert False, f"{geometry_file} failed in unpredictable way: {e}"

def test_hdf5_group_too_many_attribute(valid_geometry_HDF5_files):
    
    nekg_files: List[str] = valid_geometry_HDF5_files

    for geometry_file in nekg_files:
        group_def = HDF5GroupDefinition("NEKTAR/GEOMETRY",["FORMAT_VERSION","NO_ATTRIBUTE"])
        
        with h5py.File(geometry_file,"r") as f:
            try:
                group_def.validate(f) #should fail
                assert False, f"{geometry_file} should fail, but didn't"
            except HDF5SchemaInconsistentException:
                #this is what should happen
                pass
            except HDF5SchemaException as e:
                assert False, f"{geometry_file} did not fail in defined manner: {e}"
            except Exception as e:
                assert False, f"{geometry_file} failed in unpredictable way: {e}"

"""
    TEST DATASET VALIDATOR
"""

def test_hdf5_dataset_no_constraints(valid_geometry_HDF5_files):
    nekg_files: List[str] = valid_geometry_HDF5_files

    for geometry_file in nekg_files:
        dataset_def = HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/COMPOSITE")
        
        with h5py.File(geometry_file,"r") as f:
            assert dataset_def.validate(f)

def test_hdf5_dataset_1d_dataset_constraints(valid_geometry_HDF5_files):    
    nekg_files: List[str] = valid_geometry_HDF5_files

    for geometry_file in nekg_files:
        #-1 denotes no constraint in that dimension
        dataset_def = HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/COMPOSITE",(-1,))
        
        with h5py.File(geometry_file,"r") as f:
            assert dataset_def.validate(f)

def test_hdf5_dataset_2d_dataset_constraints(valid_geometry_HDF5_files):    
    nekg_files: List[str] = valid_geometry_HDF5_files

    for geometry_file in nekg_files:
        #-1 denotes no constraint in that dimension
        # SEG is always defined
        dataset_def = HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/SEG",(-1,2))
        
        with h5py.File(geometry_file,"r") as f:
            assert dataset_def.validate(f)

def test_hdf5_dataset_nonexistent_dataset(valid_geometry_HDF5_files):
    nekg_files: List[str] = valid_geometry_HDF5_files
    
    for geometry_file in nekg_files:
        dataset_def = HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/NOTEXIST")
        
        with h5py.File(geometry_file,"r") as f:
            try:
                dataset_def.validate(f) #should fail
                assert False, f"{geometry_file} should fail, but didn't"
            except HDF5SchemaExistenceException:
                #this is what should happen
                pass
            except HDF5SchemaException as e:
                assert False, f"{geometry_file} did not fail in defined manner: {e}"
            except Exception as e:
                assert False, f"{geometry_file} failed in unpredictable way: {e}"

def test_hdf5_dataset_invalid_dataset_constraints(valid_geometry_HDF5_files):
    nekg_files: List[str] = valid_geometry_HDF5_files
    
    for geometry_file in nekg_files:
        # SEG is always defined, should be X by 2, but we'll define it incorrectly
        dataset_def = HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/SEG",(-1,5))
        
        with h5py.File(geometry_file,"r") as f:
            try:
                dataset_def.validate(f) #should fail
                assert False, f"{geometry_file} should fail, but didn't"
            except HDF5SchemaInconsistentException:
                #this is what should happen
                pass
            except HDF5SchemaException as e:
                assert False, f"{geometry_file} did not fail in defined manner: {e}"
            except Exception as e:
                assert False, f"{geometry_file} failed in unpredictable way: {e}"

"""
    TEST COMBINED
"""
def test_hdf5_geometry_validator_accept(valid_geometry_HDF5_files):
    nekg_files: List[str] = valid_geometry_HDF5_files

    for geometry_file in nekg_files:
        with h5py.File(geometry_file) as f:
            validator = GeometrySchemaHDF5Validator(f)
            try:
                validator.validate()        
            except Exception as e:
                assert False,f"{geometry_file} failed geometry hdf5 validation. Should succeed. Error: {e}"

def test_hdf5_geometry_validator_reject_wrong_files(valid_output_fld_HDF5_files):
    nekg_files: List[str] = valid_output_fld_HDF5_files

    for geometry_file in nekg_files:
        with h5py.File(geometry_file) as f:
            validator = GeometrySchemaHDF5Validator(f)
            try:
                validator.validate()  
                assert False,f"{geometry_file} succeeded geometry hdf5 validation. Should fail."
            except HDF5SchemaException:
                pass
            except Exception as e:
                assert False,e

def test_hdf5_geometry_validator_missing_mesh_pair(create_missing_mesh_pair):
    file = create_missing_mesh_pair

    with h5py.File(file) as f:
        validator = GeometrySchemaHDF5Validator(f)

        try:
            validator.validate()  
            assert False,f"{file} succeeded geometry hdf5 validation. Should fail as MAPS/HEX exists but MESH/HEX doesn't."
        except HDF5SchemaMissingDatasetException:
            pass
        except Exception as e:
            assert False,e

def test_hdf5_geometry_validator_missing_maps_pair(create_missing_maps_pair):
    file = create_missing_maps_pair

    with h5py.File(file) as f:
        validator = GeometrySchemaHDF5Validator(f)

        try:
            validator.validate()  
            assert False,f"{file} succeeded geometry hdf5 validation. Should fail as MESH/HEX exists but MAPS/HEX doesn't."
        except HDF5SchemaMissingDatasetException:
            pass
        except Exception as e:
            assert False,e

def test_hdf5_geometry_validator_inconsistent_definitions(create_missing_inconsistent_pair):
    file = create_missing_inconsistent_pair

    with h5py.File(file) as f:
        validator = GeometrySchemaHDF5Validator(f)

        try:
            validator.validate()  
            assert False,f"{file} succeeded geometry hdf5 validation. Should fail as MESH/HEX and MAPS/HEX have inconsistent definitions."
        except HDF5SchemaInconsistentException:
            pass
        except Exception as e:
            assert False,e

def test_hdf5_geometry_validator_hex_but_no_quad(create_hex_with_missing_2d):
    file = create_hex_with_missing_2d

    with h5py.File(file) as f:
        validator = GeometrySchemaHDF5Validator(f)

        try:
            validator.validate()  
            assert False,f"{file} succeeded geometry hdf5 validation. Should fail as HEX exist, but no QUADS."
        except HDF5SchemaMissingDefinitionException:
            pass
        except Exception as e:
            assert False,e

def test_hdf5_geometry_validator_tet_but_no_tri(create_tet_with_missing_2d):
    file = create_tet_with_missing_2d

    with h5py.File(file) as f:
        validator = GeometrySchemaHDF5Validator(f)

        try:
            validator.validate()  
            assert False,f"{file} succeeded geometry hdf5 validation. Should fail as TET exist, but no TRIS."
        except HDF5SchemaMissingDefinitionException:
            pass
        except Exception as e:
            assert False,e

def test_hdf5_geometry_validator_pyr_but_no_quad(create_pyr_with_missing_2d_quad):
    file = create_pyr_with_missing_2d_quad

    with h5py.File(file) as f:
        validator = GeometrySchemaHDF5Validator(f)

        try:
            validator.validate()  
            assert False,f"{file} succeeded geometry hdf5 validation. Should fail as PYR exist, but no QUADS."
        except HDF5SchemaMissingDefinitionException:
            pass
        except Exception as e:
            assert False,e

def test_hdf5_geometry_validator_pyr_but_no_tris(create_pyr_with_missing_2d_tri):
    file = create_pyr_with_missing_2d_tri

    with h5py.File(file) as f:
        validator = GeometrySchemaHDF5Validator(f)

        try:
            validator.validate()  
            assert False,f"{file} succeeded geometry hdf5 validation. Should fail as PYR exist, but no TRIS."
        except HDF5SchemaMissingDefinitionException:
            pass
        except Exception as e:
            assert False,e

def test_hdf5_geometry_validator_prism_but_no_quad(create_prism_with_missing_2d_quad):
    file = create_prism_with_missing_2d_quad

    with h5py.File(file) as f:
        validator = GeometrySchemaHDF5Validator(f)

        try:
            validator.validate()  
            assert False,f"{file} succeeded geometry hdf5 validation. Should fail as PRISM exist, but no QUADS."
        except HDF5SchemaMissingDefinitionException:
            pass
        except Exception as e:
            assert False,e

def test_hdf5_geometry_validator_prism_but_no_tris(create_prism_with_missing_2d_tri):
    file = create_prism_with_missing_2d_tri

    with h5py.File(file) as f:
        validator = GeometrySchemaHDF5Validator(f)

        try:
            validator.validate()  
            assert False,f"{file} succeeded geometry hdf5 validation. Should fail as PRISM exist, but no TRIS."
        except HDF5SchemaMissingDefinitionException:
            pass
        except Exception as e:
            assert False,e

def test_hdf5_geometry_validator_prism_but_no_tris(create_hex_with_insufficient_quads):
    file = create_hex_with_insufficient_quads

    with h5py.File(file) as f:
        validator = GeometrySchemaHDF5Validator(f)

        try:
            validator.validate()  
            assert False,f"{file} succeeded geometry hdf5 validation. Should fail as HEX exist, but insufficeint QUADS."
        except HDF5SchemaMissingDefinitionException:
            pass
        except Exception as e:
            assert False,e

def test_hdf5_geometry_validator_dangerous_group(create_dangerous_group):
    file = create_dangerous_group

    with h5py.File(file) as f:
        validator = GeometrySchemaHDF5Validator(f)

        try:
            validator.validate()  
            assert False,f"{file} succeeded geometry hdf5 validation. Should fail as extra groups exist."
        except HDF5SchemaExtraDefinitionException:
            pass
        except Exception as e:
            assert False,e

def test_hdf5_geometry_validator_multiple_group(create_multiple_dangerous_group):
    file = create_multiple_dangerous_group

    with h5py.File(file) as f:
        validator = GeometrySchemaHDF5Validator(f)

        try:
            validator.validate()  
            assert False,f"{file} succeeded geometry hdf5 validation. Should fail as extra groups exist."
        except HDF5SchemaExtraDefinitionException:
            pass
        except Exception as e:
            assert False,e

def test_hdf5_geometry_validator_dangerous_dataset(create_dangerous_dataset):
    file = create_dangerous_dataset

    with h5py.File(file) as f:
        validator = GeometrySchemaHDF5Validator(f)

        try:
            validator.validate()  
            assert False,f"{file} succeeded geometry hdf5 validation. Should fail as extra datasets exist."
        except HDF5SchemaExtraDefinitionException:
            pass
        except Exception as e:
            assert False,e

def test_hdf5_geometry_validator_multiple_dataset(create_multiple_dangerous_dataset):
    file = create_multiple_dangerous_dataset

    with h5py.File(file) as f:
        validator = GeometrySchemaHDF5Validator(f)

        try:
            validator.validate()  
            assert False,f"{file} succeeded geometry hdf5 validation. Should fail as extra datasets exist."
        except HDF5SchemaExtraDefinitionException:
            pass
        except Exception as e:
            assert False,e

@pytest.mark.skip
def test_hdf5_output_validator_accept(valid_output_fld_HDF5_files):
    fld_files: List[str] = valid_output_fld_HDF5_files

    for output_file in fld_files:
        with h5py.File(output_file) as f:
            validator = OutputSchemaHDF5Validator(f)
            try:
                validator.validate()        
            except Exception as e:
                assert False,f"{output_file} failed output hdf5 validation. Should succeed. Error: {e}"

def test_hdf5_output_validator_reject_wrong_files(valid_geometry_HDF5_files):
    fld_files: List[str] = valid_geometry_HDF5_files

    for output_file in fld_files:
        with h5py.File(output_file) as f:
            validator = OutputSchemaHDF5Validator(f)
            try:
                validator.validate()        
                assert False,f"{output_file} succeeded output hdf5 validation. Should fail."
            except HDF5SchemaException:
                pass
            except Exception as e:
                assert False,e

def test_hdf5_output_validator_reject_extra_datasets(create_output_dangerous_datasets):
    output_file: str = create_output_dangerous_datasets
    print(output_file)
    with h5py.File(output_file) as f:
        validator = OutputSchemaHDF5Validator(f)
        try:
            validator.validate()        
            assert False,f"{output_file} succeeded output hdf5 validation. Should fail as extra datasets present."
        except HDF5SchemaExtraDefinitionException:
            pass
        except Exception as e:
            assert False,e

def test_hdf5_output_validator_reject_one_extra_dataset(create_output_one_dangerous_datasets):
    output_file: str = create_output_one_dangerous_datasets
    print(output_file)
    with h5py.File(output_file) as f:
        validator = OutputSchemaHDF5Validator(f)
        try:
            validator.validate()        
            assert False,f"{output_file} succeeded output hdf5 validation. Should fail as extra datasets present."
        except HDF5SchemaExtraDefinitionException:
            pass
        except Exception as e:
            assert False,e

def test_hdf5_output_validator_reject_extra_groups(create_output_dangerous_groups):
    output_file: str = create_output_dangerous_groups
    print(output_file)
    with h5py.File(output_file) as f:
        validator = OutputSchemaHDF5Validator(f)
        try:
            validator.validate()        
            assert False,f"{output_file} succeeded output hdf5 validation. Should fail as extra groups present."
        except HDF5SchemaExtraDefinitionException:
            pass
        except Exception as e:
            assert False,e

def test_hdf5_output_validator_reject_one_extra_groups(create_output_one_dangerous_groups):
    output_file: str = create_output_one_dangerous_groups
    print(output_file)
    with h5py.File(output_file) as f:
        validator = OutputSchemaHDF5Validator(f)
        try:
            validator.validate()        
            assert False,f"{output_file} succeeded output hdf5 validation. Should fail as extra groups present."
        except HDF5SchemaExtraDefinitionException:
            pass
        except Exception as e:
            assert False,e
