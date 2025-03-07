from abc import ABC, abstractmethod
import h5py
import lxml
import numpy as np
from typing import Tuple

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

    def extract_min_max_coords(geometry_file: h5py.File,dataset_path: str) -> Tuple[np.ndarray,np.ndarray]:
        dataset: h5py.Dataset = geometry_file[dataset_path]
        shape = dataset.shape

        # Ensure dataset is at least 2D and has 3 columns
        if len(shape) < 2 or shape[1] != 3:
            raise ValueError(f"Expected a dataset with shape (N,3), but got {shape}")

        #initialise
        CHUNK_SIZE = 1000
        min_coord = np.full(3, np.inf)
        max_coord = np.full(3, -np.inf)
        
        for chunk_start in range(0,shape[0],CHUNK_SIZE):
            chunk_end = min(chunk_start + CHUNK_SIZE, shape[0])
            data_chunk = dataset[chunk_start:chunk_end, :]

            min_coord_in_chunk: np.ndarray = np.amin(data_chunk,axis=0)
            max_coord_in_chunk: np.ndarray = np.amax(data_chunk,axis=0)

            #in-place as memory allocations are expensive in Python
            np.minimum(min_coord,min_coord_in_chunk,out=min_coord)
            np.maximum(max_coord,max_coord_in_chunk,out=max_coord)

        return min_coord, max_coord

if __name__ == "__main__":
    with h5py.File("tests/datasets/ADRSolver/ADR_2D_TriQuad.fld") as f:
        v = HDF5Extractor.extract_attribute(f,"NEKTAR/Metadata/Provenance","NektarVersion")
        print(v)

    with h5py.File("tests/datasets/ADRSolver/ADR_2D_TriQuad.nekg") as f:
        coords = HDF5Extractor.extract_min_max_coords(f,"NEKTAR/GEOMETRY/MESH/VERT")
        print(coords)