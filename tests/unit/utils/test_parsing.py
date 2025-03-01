from NekUpload.utils import parsing
import pytest
import h5py
from typing import List

def test_split_equals_expr():
    expr = "abc def = 1234    "
    lhs = "abc def"
    rhs = "1234"

    expr_lhs,expr_rhs = parsing.get_both_sides_of_equals(expr)

    assert expr_lhs == lhs
    assert expr_rhs == rhs

def test_resolve_expr_no_eval():
    data = {"PARAM1": "10",
            "PARAM2" : "20"}
    expected = {"PARAM1": 10,
            "PARAM2" : 20}
    
    result = parsing.evaluate_parameters(data)
    assert result == expected

def test_resolve_expr_sub_only():
    data = {"PARAM1": "10",
            "PARAM2" : "PARAM1"}
    expected = {"PARAM1": 10,
            "PARAM2" : 10}
    
    result = parsing.evaluate_parameters(data)
    assert result == expected

def test_resolve_expr_sub_with_literal():
    data = {"PARAM1": "10",
            "PARAM2" : "PARAM1 + 5"}
    expected = {"PARAM1": 10,
            "PARAM2" : 15}
    
    result = parsing.evaluate_parameters(data)
    assert result == expected

def test_resolve_expr_sub_with_var():
    data = {"PARAM1": "10",
            "PARAM2" : "2",
            "PARAM3" : "PARAM1 * PARAM2"}
    expected = {"PARAM1": 10,
            "PARAM2": 2,
            "PARAM3" : 20}
    
    result = parsing.evaluate_parameters(data)
    assert result == expected

def test_get_files_with_extension_normal():
    files = ["a.py","b.py","c.xml","d.xml","e.py"]
    files_py = ["a.py","b.py","e.py"]

    py = parsing.get_all_files_with_extension(files,".py")
    assert py == files_py

def test_get_files_with_extension_cases():
    files = ["a.py","b.py","c.xml","d.XML","e.py"]
    files_xml = ["c.xml","d.XML"]

    xml = parsing.get_all_files_with_extension(files,".xml")
    assert xml == files_xml

def test_get_files_with_extension_missing_dot_extension():
    files = ["a.py","b.py","c.xml","d.XML","e.py"]
    files_xml = ["c.xml","d.XML"]

    xml = parsing.get_all_files_with_extension(files,"xml")
    assert xml == files_xml

def test_get_files_with_extension_missing_dot_extension():
    files = ["a.py","b.py","c.xml","d.XML","e.py"]
    files_rst = []

    rst = parsing.get_all_files_with_extension(files,".rst")
    assert rst == files_rst

def test_get_hdf5_groups_one_level_depth(valid_geometry_HDF5_files):
    nekg_files = valid_geometry_HDF5_files
    expected_root_groups = ["","NEKTAR"] #HDF5 files have a parent directory where everythin is derived from

    for hdf5_file in nekg_files:
        with h5py.File(hdf5_file) as f:
            groups: List[str] = parsing.get_hdf5_groups_with_depth_limit(f,1)
            assert groups == expected_root_groups

def test_get_hdf5_groups_multi_level_depth(valid_geometry_HDF5_files):
    nekg_files = valid_geometry_HDF5_files
    #HDF5 files have a parent directory where everythin is derived from
    expected_root_groups = ["","NEKTAR","NEKTAR/GEOMETRY","NEKTAR/GEOMETRY/MAPS","NEKTAR/GEOMETRY/MESH"] 

    for hdf5_file in nekg_files:
        with h5py.File(hdf5_file) as f:
            groups: List[str] = parsing.get_hdf5_groups_with_depth_limit(f,5)
            assert groups == expected_root_groups

def test_get_hdf5_groups_multi_level_depth_new_start_point(valid_geometry_HDF5_files):
    nekg_files = valid_geometry_HDF5_files
    expected_groups = ["NEKTAR/GEOMETRY","NEKTAR/GEOMETRY/MAPS","NEKTAR/GEOMETRY/MESH"] 

    for hdf5_file in nekg_files:
        with h5py.File(hdf5_file) as f:
            groups: List[str] = parsing.get_hdf5_groups_with_depth_limit(f,1,"NEKTAR/GEOMETRY")
            assert groups == expected_groups

def test_get_hdf5_groups_test_limit(valid_geometry_HDF5_files):
    nekg_files = valid_geometry_HDF5_files

    #any more, and difficult to test as each file has different number of datasets
    all_groups = ["","NEKTAR/GEOMETRY","NEKTAR/GEOMETRY/MAPS","NEKTAR/GEOMETRY/MESH"]

    max_groups = range(0,5)
    expected_nums = [min(max_num,len(all_groups)) for max_num in max_groups]

    for hdf5_file in nekg_files:
        with h5py.File(hdf5_file) as f:
            for max_num,expected_num in zip(max_groups,expected_nums):
                groups: List[str] = parsing.get_hdf5_groups_with_depth_limit(f,3,"NEKTAR",max_num)
                assert expected_num == len(groups)

def test_get_hdf5_datasets_one_level_depth(valid_geometry_HDF5_files):
    nekg_files = valid_geometry_HDF5_files
    possible_datasets = [] #there are no datasets in first level of NEKTAR 

    for hdf5_file in nekg_files:
        with h5py.File(hdf5_file) as f:
            datasets: List[str] = parsing.get_hdf5_datasets_with_depth_limit(f,1)
            assert possible_datasets == datasets

def test_get_hdf5_datasets_multi_level_depth(valid_geometry_HDF5_files,geometry_possible_datasets):
    nekg_files = valid_geometry_HDF5_files

    possible_datasets: List[str] = geometry_possible_datasets
    
    for hdf5_file in nekg_files:
        with h5py.File(hdf5_file) as f:
            datasets: List[str] = parsing.get_hdf5_datasets_with_depth_limit(f,3,"NEKTAR")
            
            #geometry file doesn't have all 3d elements if not used
            #so just make sure all files are allowable
            for dataset in datasets:
                assert dataset in possible_datasets

def test_get_hdf5_datasets_test_limit(valid_geometry_HDF5_files):
    nekg_files = valid_geometry_HDF5_files

    #any more, and difficult to test as each file has different number of datasets
    max_datasets = [0,1,2,3,4,5,6,7,8]  

    for hdf5_file in nekg_files:
        with h5py.File(hdf5_file) as f:
            for max_num in max_datasets:
                datasets: List[str] = parsing.get_hdf5_datasets_with_depth_limit(f,3,"NEKTAR",max_num)
                assert max_num == len(datasets)