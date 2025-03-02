from NekUpload.validator import NektarValidator
from typing import List,Dict

def test_ADR_valid(ADR_dataset_abs_paths):
    ADR_datasets: List[Dict[str, str | List[str] | None]] = ADR_dataset_abs_paths

    for dataset in ADR_datasets:
        session: str = dataset["SESSION"]
        geometry: str = dataset["GEOMETRY"]
        output: str = dataset["OUTPUT"]
        checkpoints: List[str] = dataset["CHECKPOINT"]

        validator = NektarValidator(session,geometry,output,checkpoints,[])

        try:
            validator.validate()
        except Exception as e:
            assert False,e

def test_mixed_up_geometry_output(ADR_dataset_abs_paths):
    ADR_datasets: List[Dict[str, str | List[str] | None]] = ADR_dataset_abs_paths

    for dataset in ADR_datasets:
        session: str = dataset["SESSION"]
        output: str = dataset["GEOMETRY"]
        geometry: str = dataset["OUTPUT"]
        checkpoints: List[str] = dataset["CHECKPOINT"]

        validator = NektarValidator(session,geometry,output,checkpoints,[])

        try:
            validator.validate()
            assert False,f"{dataset} should have failed but did not"
        except Exception:
            pass