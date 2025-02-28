from abc import ABC, abstractmethod
import h5py
from typing import List,Tuple
from .custom_exceptions import HDF5SchemaException

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
            raise HDF5SchemaException(f,f"HDF5 schema error, {self.path} is not in file")
        
        group: h5py.Group = f[self.path]
        if not isinstance(group, h5py.Group): 
            raise HDF5SchemaException(f,f"HDF5 schema error, {self.path} is a {type(group)},not a group")

        #check attributes exist
        if not set(self.attributes).issubset(group.attrs.keys()):
            missing_attributes = set(self.attributes) - set(group.attrs.keys())
            if missing_attributes:
                raise HDF5SchemaException(f, f"HDF5 schema error, missing attributes in {self.path}: {missing_attributes}")
    
        return True

class HDF5DatasetDefinition(HDF5GroupDefinition):
    def __init__(self,path: str, dataset_shape: Tuple[int,...]=None):
        self.path = path
        self.dataset_shape: Tuple[int,...] = dataset_shape
        self.actual_shape: Tuple[int,...] = None

    def validate(self, f: h5py.File) -> bool:
        if self.path not in f:
            raise HDF5SchemaException(f,f"HDF5 schema error, {self.path} is not in file")
        
        dataset: h5py.Dataset = f[self.path]
        if not isinstance(dataset,h5py.Dataset):
            raise HDF5SchemaException(f,f"HDF5 schema error, {self.path} is a {type(dataset)}, not a dataset")
        
        #check dataset shape if it exists
        if self.dataset_shape:
            self.shape: Tuple[int,...] = dataset.shape
            
            #check expected dimension
            if len(self.shape) != len(self.dataset_shape):
                raise HDF5SchemaException(f,f"HDF5 schema error, {self.path} has dataset shape {self.shape}, but expecting {self.dataset_shape}")
            
            for size,constrained_size in zip(self.shape,self.dataset_shape):
                # negatives denotes no size restriction on dataset shape
                #so only positive ones are constraints
                if constrained_size >= 0 and constrained_size != size:
                    raise HDF5SchemaException(f,f"HDF5 schema error, {self.path} has dataset shape {self.shape}, but expecting {self.dataset_shape}")
                
        return True

    def get_shape(self) -> Tuple[int,...]:
        return self.actual_shape

class GeometryHDF5Validator:
    NO_DIM_CONSTRAINTS = -1 #helper

    BASE_GROUPS: Tuple[HDF5GroupDefinition] = (HDF5GroupDefinition("NEKTAR"),
                                         HDF5GroupDefinition("NEKTAR/GEOMETRY",attributes=["FORMAT_VERSION"]),
                                         HDF5GroupDefinition("NEKTAR/GEOMETRY/MAPS"),
                                         HDF5GroupDefinition("NEKTAR/GEOMETRY/MESH"))

    DATASETS_MANDATORY_MAPS: Tuple[HDF5DatasetDefinition] = (HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/VERT",(NO_DIM_CONSTRAINTS,)),
                                                             HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/DOMAIN",(NO_DIM_CONSTRAINTS,)),
                                                             HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/COMPOSITE",(NO_DIM_CONSTRAINTS,)))

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
    
    def __init__(self,f: h5py.File):        
        self.file: h5py.File = f

    def validate(self):
        #check mandatory groups and datasets first
        for group in GeometryHDF5Validator.BASE_GROUPS:
            group.validate(self.file)
                
        for group in GeometryHDF5Validator.DATASETS_MANDATORY_MAPS:
            group.validate(self.file)

        for group in GeometryHDF5Validator.DATASETS_MANDATORY_MESH:
            group.validate(self.file)
        
        #1d datasets should all be present too
        for group in GeometryHDF5Validator.DATASETS_1D_MAPS:
            group.validate(self.file)

        for group in GeometryHDF5Validator.DATASETS_1D_MESH:
            group.validate(self.file)

        #not all 2d datasets are present
        for group in GeometryHDF5Validator.DATASETS_2D_MAPS:
            try:
                group.validate(self.file)
            except HDF5SchemaException:
                pass
            except Exception:
                raise

        for group in GeometryHDF5Validator.DATASETS_2D_MESH:
            try:
                group.validate(self.file)
            except HDF5SchemaException:
                pass
            except Exception:
                raise

        for group in GeometryHDF5Validator.DATASETS_2D_MAPS:
            try:
                group.validate(self.file)
            except HDF5SchemaException:
                pass
            except Exception:
                raise

        ##
        # Check that all groups and datasets in the file are valid  


class OutputHDF5Validator:

    NO_DIM_CONSTRAINTS = -1 #helper

    BASE_GROUPS = (HDF5GroupDefinition("NEKTAR",["FORMAT_VERSION"]),
                   HDF5GroupDefinition("NEKTAR/Metadata",attributes=["ChkFileNum","Time"]), #TODO
                   HDF5GroupDefinition("NEKTAR/Metadata/Provenance",attributes=["GitBranch","GitSHA1","Hostname","NektarVersion","Timestamp"]))

    EXPECTED_DATASETS = (HDF5DatasetDefinition("NEKTAR/DATA",(NO_DIM_CONSTRAINTS,)),
                         HDF5DatasetDefinition("NEKTAR/DECOMPOSITION",(NO_DIM_CONSTRAINTS,)),
                         HDF5DatasetDefinition("NEKTAR/ELEMENTIDS",(NO_DIM_CONSTRAINTS,)))

    def __init__(self,f: h5py.File):        
        self.file: h5py.File = f

    def validate(self):
        for group in OutputHDF5Validator.BASE_GROUPS:
            group.validate(self.file)

        for dataset in OutputHDF5Validator.EXPECTED_DATASETS:
            dataset.validate(self.file)

        #there should be other groups defined based on decomposition
        #DECOMPOSITION contains sequence of seven numbres, seventh number
        #is a hash denoting a group containing expansion information
        decomposition_dataset: h5py.Dataset = self.file["NEKTAR/DECOMPOSITION"]
        self._check_decomposition(decomposition_dataset)

    def _check_decomposition(self, decomposition_dataset: h5py.Dataset):
        if decomposition_dataset.shape[0] % 7 != 0:
            raise HDF5SchemaException(self.file,"HDF5 Schema Error: Decomposition shape should be multiple of 7")

        expected_groups: List[HDF5GroupDefinition] = []
        for i in range(6,decomposition_dataset.shape[0],7):

            hash = decomposition_dataset[i]
            expected_groups.append(HDF5GroupDefinition(f"NEKTAR/{hash}",attributes=["BASIS","FIELDS","NUMMODESPERDIR","SHAPE"]))

        for group in expected_groups:
            group.validate(self.file)