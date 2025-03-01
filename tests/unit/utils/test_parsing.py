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

def test_get_hdf5_datasets_one_level_depth(valid_geometry_HDF5_files):
    nekg_files = valid_geometry_HDF5_files
    possible_datasets = [] #there are no datasets in first level of NEKTAR 

    for hdf5_file in nekg_files:
        with h5py.File(hdf5_file) as f:
            datasets: List[str] = parsing.get_hdf5_datasets_with_depth_limit(f,1)
            assert possible_datasets == datasets

def test_get_hdf5_datasets_multi_level_depth(valid_geometry_HDF5_files):
    nekg_files = valid_geometry_HDF5_files

    possible_datasets = ['NEKTAR/GEOMETRY/MAPS/COMPOSITE', 'NEKTAR/GEOMETRY/MAPS/CURVE_EDGE', 'NEKTAR/GEOMETRY/MAPS/CURVE_FACE', 'NEKTAR/GEOMETRY/MAPS/DOMAIN',
                        'NEKTAR/GEOMETRY/MAPS/HEX', 'NEKTAR/GEOMETRY/MAPS/PRISM', 'NEKTAR/GEOMETRY/MAPS/PYR', 'NEKTAR/GEOMETRY/MAPS/QUAD',
                        'NEKTAR/GEOMETRY/MAPS/SEG', 'NEKTAR/GEOMETRY/MAPS/TET', 'NEKTAR/GEOMETRY/MAPS/TRI', 'NEKTAR/GEOMETRY/MAPS/VERT',
                        'NEKTAR/GEOMETRY/MESH/COMPOSITE', 'NEKTAR/GEOMETRY/MESH/CURVE_EDGE', 'NEKTAR/GEOMETRY/MESH/CURVE_FACE',
                        'NEKTAR/GEOMETRY/MESH/CURVE_NODES', 'NEKTAR/GEOMETRY/MESH/DOMAIN', 'NEKTAR/GEOMETRY/MESH/HEX', 'NEKTAR/GEOMETRY/MESH/PRISM',
                        'NEKTAR/GEOMETRY/MESH/PYR', 'NEKTAR/GEOMETRY/MESH/QUAD', 'NEKTAR/GEOMETRY/MESH/SEG', 'NEKTAR/GEOMETRY/MESH/TET', 'NEKTAR/GEOMETRY/MESH/TRI',
                        'NEKTAR/GEOMETRY/MESH/VERT']
    
    for hdf5_file in nekg_files:
        with h5py.File(hdf5_file) as f:
            datasets: List[str] = parsing.get_hdf5_datasets_with_depth_limit(f,3,"NEKTAR")
            
            #geometry file doesn't have all 3d elements if not used
            #so just make sure all files are allowable
            for dataset in datasets:
                assert dataset in possible_datasets