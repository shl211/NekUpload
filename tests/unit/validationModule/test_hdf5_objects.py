from NekUpload.validationModule.hdf5validator import *

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
            assert not group_def.validate(f)

def test_hdf5_group_missing_attribute(valid_geometry_HDF5_files):
    
    nekg_files: List[str] = valid_geometry_HDF5_files

    for geometry_file in nekg_files:
        group_def = HDF5GroupDefinition("NEKTAR",["NO_ATTRIBUTE"])
        
        with h5py.File(geometry_file,"r") as f:
            assert not group_def.validate(f)

def test_hdf5_group_too_many_attribute(valid_geometry_HDF5_files):
    
    nekg_files: List[str] = valid_geometry_HDF5_files

    for geometry_file in nekg_files:
        group_def = HDF5GroupDefinition("NEKTAR/GEOMETRY",["FORMAT_VERSION","NO_ATTRIBUTE"])
        
        with h5py.File(geometry_file,"r") as f:
            assert not group_def.validate(f)

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
