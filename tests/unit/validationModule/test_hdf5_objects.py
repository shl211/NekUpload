from NekUpload.validationModule.hdf5schema_validator import *
from NekUpload.validationModule.custom_exceptions import HDF5SchemaException
import pytest
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
            except HDF5SchemaException:
                #this is what should happen
                pass
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
            except HDF5SchemaException:
                #this is what should happen
                pass
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
            except HDF5SchemaException:
                #this is what should happen
                pass
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
            except HDF5SchemaException:
                #this is what should happen
                pass
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
            except HDF5SchemaException:
                #this is what should happen
                pass
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
                assert False,f"{geometry_file} succeeded geometry hdf5 validation. Should fail. Error: {e}"
            except HDF5SchemaException:
                pass
            except Exception as e:
                assert False,e

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
                assert False,f"{output_file} succeeded output hdf5 validation. Should fail. Error: {e}"
            except HDF5SchemaException:
                pass
            except Exception as e:
                assert False,e
