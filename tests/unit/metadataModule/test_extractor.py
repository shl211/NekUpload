from NekUpload.metadataModule.extractor import HDF5Extractor
import h5py
import os

def test_hdf5_attr_extractor():

    # Create a new HDF5 file
    with h5py.File('testfile.h5', 'w') as f:
        # Create a group in the file
        grp = f.create_group('test_group')
        # Add an attribute to the group
        grp.attrs['test_attribute'] = 'test_value'


    with h5py.File('testfile.h5','r') as f:
        val = HDF5Extractor.extract_attribute(f,"test_group","test_attribute")
        assert val == "test_value"

    os.remove("testfile.h5")

def test_hdf5_attr_extractor():

    # Create a new HDF5 file
    with h5py.File('testfile.h5', 'w') as f:
        # Create a group in the file
        grp = f.create_group('test_group')
        # Add an attribute to the group
        grp.attrs['test_attribute'] = 'test_value'


    with h5py.File('testfile.h5','r') as f:
        val = HDF5Extractor.extract_attribute(f,"invalid_group","test_attribute")
        assert not val

    os.remove("testfile.h5")

def test_hdf5_attr_extractor():

    # Create a new HDF5 file
    with h5py.File('testfile.h5', 'w') as f:
        # Create a group in the file
        grp = f.create_group('test_group')
        # Add an attribute to the group
        grp.attrs['test_attribute'] = 'test_value'


    with h5py.File('testfile.h5','r') as f:
        val = HDF5Extractor.extract_attribute(f,"test_group","invalid_attribute")
        assert not val

    os.remove("testfile.h5")