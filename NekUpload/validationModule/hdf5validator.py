from abc import ABC, abstractmethod
import h5py
from typing import List,Tuple

class HDF5Definition(ABC):
    @abstractmethod
    def validate(self,h5py_file: h5py.File):
        pass

class HDF5GroupDefinition(HDF5Definition):
    def __init__(self,path: str, attributes: List[str]=None):
        self.path = path
        self.attributes: List[str] = attributes if attributes is not None else []

    def validate(self,f: h5py.File) -> bool:
        if self.path not in f:
            return False
        
        group: h5py.Group = f[self.path]
        if not isinstance(group, h5py.Group): 
            return False

        #check attributes exist
        return set(self.attributes).issubset(group.attrs.keys())
    
class HDF5DatasetDefinition(HDF5GroupDefinition):
    def __init__(self,path: str, dataset_shape: Tuple[int,...]=None):
        self.path = path
        self.dataset_shape = dataset_shape

    def validate(self, f: h5py.File) -> bool:
        if self.path not in f:
            return False
        
        dataset: h5py.Dataset = f[self.path]
        if not isinstance(dataset,h5py.Dataset):
            return False
        
        #check dataset shape if it exists
        if self.dataset_shape:
            shape: Tuple[int,...] = dataset.shape
            
            #check expected dimension
            if len(shape) != len(self.dataset_shape):
                return False
            
            for size,constrained_size in zip(shape,self.dataset_shape):
                # negatives denotes no size restriction on dataset shape
                #so only positive ones are constraints
                if constrained_size >= 0 and constrained_size != size:
                    return False
                
        return True
    


class GeometryHDF5Validator:
    NO_DIM_CONSTRAINTS = -1 #helper

    BASE_GROUPS: Tuple[HDF5GroupDefinition] = (HDF5GroupDefinition("NEKTAR"),
                                         HDF5GroupDefinition("NEKTAR/GEOMETRY",attributes=["FORMAT_VERSION"]),
                                         HDF5GroupDefinition("NEKTAR/GEOMETRY/MAPS"),
                                         HDF5GroupDefinition("NEKTAR/GEOMETRY/MESH"))

    DATASETS_MANDATORY_MAPS: Tuple[HDF5DatasetDefinition] = (HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/VERT",(NO_DIM_CONSTRAINTS,)),
                                                             HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/DOMAIN"),(NO_DIM_CONSTRAINTS,),
                                                             HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/COMPOSITE"),(NO_DIM_CONSTRAINTS,))

    DATASETS_MANDATORY_MESH: Tuple[HDF5DatasetDefinition] = (HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/CURVE_NODES",(NO_DIM_CONSTRAINTS,3)),
                                                             HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/VERT",(NO_DIM_CONSTRAINTS,3)),
                                                             HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/DOMAIN",(NO_DIM_CONSTRAINTS,)),
                                                             HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/COMPOSITE",(NO_DIM_CONSTRAINTS,)))
    
    DATASETS_1D_MAPS: Tuple[HDF5DatasetDefinition] = (HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/SEG",(NO_DIM_CONSTRAINTS,)),
                                                      HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/CURVE_EDGE",(NO_DIM_CONSTRAINTS,)))
    
    DATASETS_1D_MESH: Tuple[HDF5DatasetDefinition] = (HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/SEG",(NO_DIM_CONSTRAINTS,2)),
                                                      HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/CURVE_EDGE",(NO_DIM_CONSTRAINTS,3)))
    
    DATASETS_2D_MAPS: Tuple[HDF5DatasetDefinition] = (HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/TRI",(NO_DIM_CONSTRAINTS,)),
                                                      HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/QUAD",(NO_DIM_CONSTRAINTS,)),
                                                      HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/CURVE_FACE",(NO_DIM_CONSTRAINTS,)))
    
    DATASETS_2D_MESH: Tuple[HDF5DatasetDefinition] = (HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/TRI",(NO_DIM_CONSTRAINTS,3)),
                                                      HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/QUAD",(NO_DIM_CONSTRAINTS,4)),
                                                      HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/CURVE_FACE",(NO_DIM_CONSTRAINTS,3)))

    DATASETS_2D_MAPS: Tuple[HDF5DatasetDefinition] = (HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/HEX",(NO_DIM_CONSTRAINTS,)),
                                                      HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/TET",(NO_DIM_CONSTRAINTS,)),
                                                      HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/PYR",(NO_DIM_CONSTRAINTS,)),
                                                      HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/PRISM",(NO_DIM_CONSTRAINTS,)))

    DATASETS_2D_MESH: Tuple[HDF5DatasetDefinition] = (HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/HEX",(NO_DIM_CONSTRAINTS,6)),
                                                      HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/TET",(NO_DIM_CONSTRAINTS,4)),
                                                      HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/PYR",(NO_DIM_CONSTRAINTS,5)),
                                                      HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/PRISM",(NO_DIM_CONSTRAINTS,5)))
    
    def __init__(self):
        pass