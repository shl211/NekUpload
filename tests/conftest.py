import os
import pytest
from typing import List, Dict

@pytest.fixture(autouse=True)
def set_test_directory():
    original_cwd = os.getcwd()

    # Change the working directory to the directory where the tests are
    test_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(test_dir)
    yield
    os.chdir(original_cwd)

@pytest.fixture
def ADR_dataset_rel_paths() -> List[Dict[str, str | List[str] | None]]:
    dir = "datasets/ADRSolver"

    set_1_session = "ADR_2D_TriQuad.xml"
    set_1_geometry = "ADR_2D_TriQuad.nekg"
    set_1_checkpoint = ["ADR_2D_TriQuad_0.chk"]
    set_1_output = "ADR_2D_TriQuad.fld"

    set_2_session = "ADR_3D_AllElmt.xml"
    set_2_geometry = "ADR_3D_AllElmt.nekg"
    set_2_checkpoint = ["ADR_3D_AllElmt_0.chk","ADR_3D_AllElmt_1.chk"]
    set_2_output = "ADR_3D_AllElmt.fld"

    session_files = [set_1_session,set_2_session]
    geometry_files = [set_1_geometry,set_2_geometry]
    checkpoint_files = [set_1_checkpoint,set_2_checkpoint]
    output_files = [set_1_output,set_2_output]

    datasets = []
    for session,geometry,checkpoint_list,output in zip(session_files,geometry_files,checkpoint_files,output_files):
        session_path = os.path.join(dir, session)
        geometry_path = os.path.join(dir, geometry)
        output_path = os.path.join(dir, output)
        checkpoint_list_path = [os.path.join(dir,chk) for chk in checkpoint_list]
        
        datasets.append({
            "SESSION": session_path,
            "GEOMETRY": geometry_path,
            "CHECKPOINT": checkpoint_list_path,
            "OUTPUT": output_path
        })

    return datasets

@pytest.fixture()
def ADR_dataset_abs_paths(ADR_dataset_rel_paths) -> List[Dict[str, str | List[str] | None]]:
    #use dataset from relative path to ensure data presented in same order
    rel_dataset = ADR_dataset_rel_paths
    
    dataset_abs = []
    for dataset in rel_dataset:
        session_abs_path = os.path.abspath(dataset["SESSION"])
        geometry_abs_path = os.path.abspath(dataset["GEOMETRY"])
        output_abs_path = os.path.abspath(dataset["OUTPUT"])
        checkpoint_list_abs_path = [os.path.abspath(file) for file in dataset["CHECKPOINT"]]

        dataset_abs.append({
            "SESSION": session_abs_path,
            "GEOMETRY": geometry_abs_path,
            "CHECKPOINT": checkpoint_list_abs_path,
            "OUTPUT": output_abs_path
        })

    return dataset_abs

@pytest.fixture()
def valid_session_XML_files() -> List[str]:
    dir = "datasets" #relative to root

    #find all files recursively
    xml_files = []
    for root, _, files in os.walk(dir):
        for file in files:
            if file.endswith(".xml"):
                xml_files.append(os.path.abspath(os.path.join(root, file)))
    return xml_files

@pytest.fixture()
def nektar_session_schema() -> str:
    return os.path.join("../NekUpload/validationModule/nektar.xsd") #path from test root to validation    