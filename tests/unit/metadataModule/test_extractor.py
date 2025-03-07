from NekUpload.metadataModule.extractor import HDF5Extractor
import h5py
import os
import numpy as np

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

def test_hdf5_attr_extractor_bad_group():

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

def test_hdf5_attr_extractor_bad_attribute():

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

def test_hdf5_attr_geometry_streaming():

    # Create a new HDF5 file
    with h5py.File('testfile.h5', 'w') as f:
        # Create a group in the file
        grp = f.create_group('test_group')
        # Create a dataset with 1000 coordinates with random numbers between 0 and 100
        data = np.random.randint(0, 100, size=(1000, 3))
        
        #make sure min is 0 and max is 100
        data[400][0] = 0
        data[304][1] = 0
        data[999][2] = 0

        data[123][0] = 100
        data[2][1] = 100
        data[555][2] = 100

        grp.create_dataset('coordinates', data=data)


    with h5py.File('testfile.h5','r') as f:
        min_coord,max_coord = HDF5Extractor.extract_min_max_coords(f,"test_group/coordinates")
        assert np.array_equal(min_coord, np.array([0,0,0]))
        assert np.array_equal(max_coord,np.array([100,100,100]))

    os.remove("testfile.h5")
