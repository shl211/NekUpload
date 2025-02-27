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