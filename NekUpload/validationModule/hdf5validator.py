from abc import ABC, abstractmethod
import h5py
from typing import List

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




