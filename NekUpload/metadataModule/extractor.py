from abc import ABC, abstractmethod
import h5py
import lxml

class Extractor(ABC):
    def __init__(self):
        pass

class HDF5Extractor(Extractor):
    def __init__(self):
        pass

    @staticmethod
    def extract_attribute(output_file: h5py.File,group_path: str, attribute: str) -> str:

        try:
            group = output_file[group_path]

            if not isinstance(group,h5py.Group):
                raise ValueError

            return group.attrs[attribute].strip()

        except Exception:
            return None
        
if __name__ == "__main__":
    with h5py.File("tests/datasets/ADRSolver/ADR_2D_TriQuad.fld") as f:
        v = HDF5Extractor.extract_attribute(f,"NEKTAR/Metadata/Provenance","NektarVersion")
        print(v)