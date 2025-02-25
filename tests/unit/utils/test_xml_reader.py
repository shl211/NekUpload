from NekUpload.utils.xml_reader import XMLReader
import os
import pytest
import lxml.etree as ET

@pytest.fixture
def change_test_dir():
    original_dir = os.getcwd()
    test_dir = os.path.dirname(__file__)
    os.chdir(test_dir)
    yield
    os.chdir(original_dir)

def test_merge(change_test_dir):
    file1 = "file1.xml"
    file2 = "file2.xml"

    with XMLReader(file1) as f:
        f.merge_first_level_elements_with(file2, "output.xml")

    #may want to check formatting at some point in future, but currently looks good
    assert xml_files_are_equal("expected_merge.xml","output.xml")

    #remove file on success, otherwise leave for viewing purposes
    if os.path.exists("output.xml"):
        os.remove("output.xml")

def xml_files_are_equal(file1: str, file2: str) -> bool:
    """Compares two XML files for content equality, ignoring formatting differences."""
    tree1 = ET.parse(file1)
    tree2 = ET.parse(file2)

    # Convert both XMLs into a canonicalized string format
    xml1 = ET.tostring(tree1, method="c14n")
    xml2 = ET.tostring(tree2, method="c14n")

    return xml1 == xml2
