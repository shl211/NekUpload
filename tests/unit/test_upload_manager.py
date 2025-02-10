from NekUpload.upload_manager import UploadManager
import os
from pytest import fixture
from typing import Generator, Tuple, Dict, List, Union
import tempfile
import shutil

@fixture
def setup_valid_directory() -> Generator[Tuple[str, Dict[str, Union[str, List[str]]]], None, None]:
    temp_dir = tempfile.mkdtemp()
    files: Dict[str, Union[str, List[str]]] = {
        "SESSION": "test.xml",
        "GEOMETRY": "test.nekg",
        "OUTPUT": "test.fld",
        "CHECKPOINTS": ["test1.chk", "test2.chk"],
        "FILTERS": ["test1.fce", "test2.fce"]
    }
    
    # Create all files
    for value in files.values():
        if isinstance(value, str):  # Single filename
            open(os.path.join(temp_dir, value), 'a').close()
        elif isinstance(value, list):  # List of filenames
            for file in value:
                open(os.path.join(temp_dir, file), 'a').close()

    yield temp_dir, files  # Provide directory and file mapping to the test
    
    shutil.rmtree(temp_dir)  # Cleanup after test


def get_abs_path_helper(path: str) -> str:
    return os.path.abspath(path)

def test_valid_add_session_file():
    session_file = "test.xml"
    upload_manager = UploadManager()
    upload_manager.add_session_file(session_file)

    assert(get_abs_path_helper(session_file) == upload_manager.session_file)

def test_valid_add_geometry_file():
    geometry_file = "test.nekg"
    upload_manager = UploadManager()
    upload_manager.add_geometry_file(geometry_file)

    assert(get_abs_path_helper(geometry_file) == upload_manager.geometry_file)

def test_valid_add_output_file():
    output_file = "test.fld"
    upload_manager = UploadManager()
    upload_manager.add_output_file(output_file)

    assert(get_abs_path_helper(output_file) == upload_manager.output_file)

def test_valid_add_checkpoint_files():
    chk_files = ["test1.chk","test2.chk"]
    chk_abs_paths = [get_abs_path_helper(f) for f in chk_files]
    
    upload_manager = UploadManager()
    upload_manager.add_checkpoint_files(chk_files)

    assert(chk_abs_paths == upload_manager.checkpoint_files)

def test_valid_add_filter_files():
    filter_files = ["test1.fce","test2.fce"]
    filter_abs_paths = [get_abs_path_helper(f) for f in filter_files]
    
    upload_manager = UploadManager()
    upload_manager.add_filter_files(filter_files)

    assert(filter_abs_paths == upload_manager.filter_files)

def test_valid_add_directory(setup_valid_directory):
    tmp_dir,files = setup_valid_directory

    upload_manager = UploadManager()
    upload_manager.add_files_from_directory(tmp_dir)

    # Convert to absolute paths
    # files are originally given relative to tmp_dir
    expected_session_file = get_abs_path_helper(os.path.join(tmp_dir, files["SESSION"]))
    expected_geometry_file = get_abs_path_helper(os.path.join(tmp_dir, files["GEOMETRY"]))
    expected_output_file = get_abs_path_helper(os.path.join(tmp_dir, files["OUTPUT"]))
    expected_checkpoint_files = [get_abs_path_helper(os.path.join(tmp_dir, f)) for f in files["CHECKPOINTS"]]
    expected_filter_files = [get_abs_path_helper(os.path.join(tmp_dir, f)) for f in files["FILTERS"]]

    assert(expected_session_file == upload_manager.session_file)
    assert(expected_geometry_file == upload_manager.geometry_file)
    assert(expected_output_file == upload_manager.output_file)

    #order not important in the list
    assert(set(expected_checkpoint_files) == set(upload_manager.checkpoint_files))
    assert(set(expected_filter_files) == set(upload_manager.filter_files))