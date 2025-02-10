from NekUpload.utils.hdf5_reader import HDF5Reader
from pytest import fixture
import h5py
import os
import numpy as np
from typing import Dict,Any

@fixture
def setup_hdf5_file():
    file_path = 'test_file.h5'

    with h5py.File(file_path, 'a') as f:
        group1 = f.create_group('ROOT/GROUP1')
        group2 = f.create_group('ROOT/GROUP2')

        #group 1 should have attributes
        data1 = np.random.random((100, 100))
        dataset1 = group1.create_dataset("dataset_with_attrs", data=data1)
        dataset1.attrs["description"] = "This dataset has attributes"
        dataset1.attrs["scale"] = 10

        #group 2 has no attributes
        data2 = np.array([10,20,30,40,50])
        group2.create_dataset("dataset_no_attrs", data=data2)

    data = {"file": file_path,
            "groups": ["ROOT/GROUP1","ROOT/GROUP2"],
            "group1_dataset": data1,
            "group1_attributes": ["description","scale"],
            "group2_dataset": data2,
            "group2_attributes": []  
        }

    yield data

    #clean up test files afterwards
    os.remove(file_path)

def test_get_shape(setup_hdf5_file):
    file_path = setup_hdf5_file["file"]
    with HDF5Reader(file_path) as reader:
        shape1 = reader.get_shape("ROOT/GROUP1/dataset_with_attrs")
        shape2 = reader.get_shape("ROOT/GROUP2/dataset_no_attrs")
        
        assert shape1 == setup_hdf5_file["group1_dataset"].shape
        assert shape2 == setup_hdf5_file["group2_dataset"].shape

def test_get_keys(setup_hdf5_file):
    file_path = setup_hdf5_file["file"]
    with HDF5Reader(file_path) as reader:
        keys = reader.get_keys()
        expected_keys = {
            "ROOT": "GROUP",
            "ROOT/GROUP1": "GROUP",
            "ROOT/GROUP1/dataset_with_attrs": "DATASET",
            "ROOT/GROUP1/dataset_with_attrs/@description": "ATTRIBUTE",
            "ROOT/GROUP1/dataset_with_attrs/@scale": "ATTRIBUTE",
            "ROOT/GROUP2": "GROUP",
            "ROOT/GROUP2/dataset_no_attrs": "DATASET"
        }
        assert keys == expected_keys

def test_get_dataset(setup_hdf5_file):
    file_path = setup_hdf5_file["file"]
    with HDF5Reader(file_path) as reader:
        dataset1 = reader.get_dataset("ROOT/GROUP1/dataset_with_attrs")
        dataset2 = reader.get_dataset("ROOT/GROUP2/dataset_no_attrs")
        
        np.testing.assert_array_equal(dataset1[...], setup_hdf5_file["group1_dataset"])
        np.testing.assert_array_equal(dataset2[...], setup_hdf5_file["group2_dataset"])

def test_get_attributes(setup_hdf5_file):
    file_path = setup_hdf5_file["file"]
    with HDF5Reader(file_path) as reader:
        attrs1 = reader.get_attributes("ROOT/GROUP1/dataset_with_attrs")
        attrs2 = reader.get_attributes("ROOT/GROUP2/dataset_no_attrs")
        
        expected_attrs1 = {
            "description": "This dataset has attributes",
            "scale": 10
        }
        expected_attrs2 = {}

        assert attrs1 == expected_attrs1
        assert attrs2 == expected_attrs2

def test_get_dtype(setup_hdf5_file):
    file_path = setup_hdf5_file["file"]
    with HDF5Reader(file_path) as reader:
        dtype1 = reader.get_dtype("ROOT/GROUP1/dataset_with_attrs")
        dtype2 = reader.get_dtype("ROOT/GROUP2/dataset_no_attrs")
        
        assert dtype1 == str(setup_hdf5_file["group1_dataset"].dtype)
        assert dtype2 == str(setup_hdf5_file["group2_dataset"].dtype)

def test_summary(setup_hdf5_file):
    file_path = setup_hdf5_file["file"]
    with HDF5Reader(file_path) as reader:
        summary = reader.summary()
        
        assert summary["File Name"] == file_path
        assert summary["Groups"] == 3
        assert summary["Datasets"] == 2
        assert summary["Attributes"] == 2

def test_dump_to_plain_file(setup_hdf5_file):
    file_path = setup_hdf5_file["file"]
    output_file = "output.txt"
    with HDF5Reader(file_path) as reader:
        reader.dump_to_plain_file(output_file)
        
    assert os.path.exists(output_file)
    
    with open(output_file, "r") as f:
        content = f.read()
        assert "Group: /ROOT/GROUP1" in content
        assert "Dataset: dataset_with_attrs" in content
        assert "Attributes:" in content
        assert "description: This dataset has attributes" in content
        assert "scale: 10" in content
        assert "Group: /ROOT/GROUP2" in content
        assert "Dataset: dataset_no_attrs" in content
    
    os.remove(output_file)