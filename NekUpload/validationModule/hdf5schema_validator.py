from abc import ABC, abstractmethod
import h5py
from typing import List,Tuple,Set,Dict
from types import MappingProxyType
from .custom_exceptions import HDF5SchemaExistenceException,HDF5SchemaMissingDatasetException,HDF5SchemaInconsistentException
from dataclasses import dataclass,field

class HDF5Definition(ABC):
    @abstractmethod
    def validate(self,h5py_file: h5py.File):
        pass

@dataclass(frozen=True)
class HDF5GroupDefinition(HDF5Definition):
    """Given an HDF5 file, responsible for checking group conforms to correct structure and contains
    the specified attributes. This is not an exclusive check, other non-specified attributes can also be present.
    All exceptions raised from this class are of type HDF5SchemaException or its children.

    Args:
        HDF5Definition (_type_): _description_
    """
    path: str
    attributes: List[str] = field(default_factory=list)

    def validate(self,f: h5py.File) -> bool:
        """_summary_

        Args:
            f (h5py.File): _description_

        Raises:
            HDF5SchemaException: _description_
            HDF5SchemaException: _description_
            HDF5SchemaException: _description_

        Returns:
            bool: _description_
        """
        if self.path not in f:
            raise HDF5SchemaExistenceException(f,f"HDF5 schema error, {self.path} is not in file")
        
        group: h5py.Group = f[self.path]
        if not isinstance(group, h5py.Group): 
            raise HDF5SchemaInconsistentException(f,f"HDF5 schema error, {self.path} is a {type(group)},not a group")

        #check attributes exist
        if not set(self.attributes).issubset(group.attrs.keys()):
            missing_attributes = set(self.attributes) - set(group.attrs.keys())
            if missing_attributes:
                raise HDF5SchemaInconsistentException(f, f"HDF5 schema error, missing attributes in {self.path}: {missing_attributes}")
    
        return True

    def __str__(self):
        return self.path

    def get_path(self):
        return self.path

@dataclass(frozen=True)
class HDF5DatasetDefinition(HDF5Definition):
    """Given an HDF5 file, responsible for checking if dataset conforms to schema expectations, such as shape constraints.
        All exceptions raised from this class are of type HDF5SchemaException or its children.

    Args:
        HDF5GroupDefinition (_type_): _description_
    """
    path: str
    dataset_shape: Tuple[int,...] = ()

    def validate(self, f: h5py.File) -> bool:
        """_summary_

        Args:
            f (h5py.File): _description_

        Raises:
            HDF5SchemaException: _description_
            HDF5SchemaException: _description_
            HDF5SchemaException: _description_
            HDF5SchemaException: _description_

        Returns:
            bool: _description_
        """
        if self.path not in f:
            raise HDF5SchemaExistenceException(f,f"HDF5 schema error, {self.path} is not in file")
        
        dataset: h5py.Dataset = f[self.path]
        if not isinstance(dataset,h5py.Dataset):
            raise HDF5SchemaInconsistentException(f,f"HDF5 schema error, {self.path} is a {type(dataset)}, not a dataset")
        
        #check dataset shape if it exists
        if self.dataset_shape:
            actual_shape: Tuple[int,...] = dataset.shape
            
            #check expected dimension
            if len(actual_shape) != len(self.dataset_shape):
                raise HDF5SchemaInconsistentException(f,f"HDF5 schema error, {self.path} has dataset shape {actual_shape}, but expecting {self.dataset_shape}")
            
            for size,constrained_size in zip(actual_shape,self.dataset_shape):
                # negatives denotes no size restriction on dataset shape
                #so only positive ones are constraints
                if constrained_size >= 0 and constrained_size != size:
                    raise HDF5SchemaInconsistentException(f,f"HDF5 schema error, {self.path} has dataset shape {actual_shape}, but expecting {self.dataset_shape}")
                
        return True
    
    def __str__(self):
        return self.path

    def get_path(self):
        return self.path

class GeometrySchemaHDF5Validator:
    NO_DIM_CONSTRAINTS = -1 #helper

    #TODO make these dict immutable
    #using immutable dictionary to define what structure of each group and dataset should look like regardless of geometry file
    #dict to help associate each set with a useful descriptor, which will be beneficial later on
    BASE_GROUPS: MappingProxyType[str,HDF5GroupDefinition] = MappingProxyType({"NEKTAR": HDF5GroupDefinition("NEKTAR"),
                                            "GEOMETRY": HDF5GroupDefinition("NEKTAR/GEOMETRY",attributes=["FORMAT_VERSION"]),
                                            "MAPS": HDF5GroupDefinition("NEKTAR/GEOMETRY/MAPS"),
                                            "MESH": HDF5GroupDefinition("NEKTAR/GEOMETRY/MESH")})

    DATASETS_MANDATORY_MAPS: MappingProxyType[str,HDF5DatasetDefinition] = MappingProxyType(
                                                            {"VERT": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/VERT",(NO_DIM_CONSTRAINTS,)),
                                                            "DOMAIN": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/DOMAIN",(NO_DIM_CONSTRAINTS,)),
                                                            "COMPOSITE": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/COMPOSITE",(NO_DIM_CONSTRAINTS,))
                                                            })

    DATASETS_MANDATORY_MESH: MappingProxyType[str,HDF5DatasetDefinition] = MappingProxyType(
                                                                {"CURVE_NODES": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/CURVE_NODES",(NO_DIM_CONSTRAINTS,3)),
                                                                "VERT": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/VERT",(NO_DIM_CONSTRAINTS,3)),
                                                                "DOMAIN": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/DOMAIN",(NO_DIM_CONSTRAINTS,)),
                                                                "COMPOSITE": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/COMPOSITE",(NO_DIM_CONSTRAINTS,))
                                                                })
    
    DATASETS_1D_MAPS: MappingProxyType[str,HDF5DatasetDefinition] = MappingProxyType(
                                                        {"SEG": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/SEG",(NO_DIM_CONSTRAINTS,)),
                                                        "CURVE_EDGE": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/CURVE_EDGE",(NO_DIM_CONSTRAINTS,))
                                                        })
    
    DATASETS_1D_MESH: MappingProxyType[str,HDF5DatasetDefinition] = MappingProxyType(
                                                        {"SEG": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/SEG",(NO_DIM_CONSTRAINTS,2)),
                                                        "CURVE_EDGE": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/CURVE_EDGE",(NO_DIM_CONSTRAINTS,3))
                                                        })

    DATASETS_2D_MAPS: MappingProxyType[str,HDF5DatasetDefinition] = MappingProxyType(
                                                        {"TRI": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/TRI",(NO_DIM_CONSTRAINTS,)),
                                                        "QUAD": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/QUAD",(NO_DIM_CONSTRAINTS,)),
                                                        "CURVE_FACE": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/CURVE_FACE",(NO_DIM_CONSTRAINTS,))
                                                        })
    
    DATASETS_2D_MESH: MappingProxyType[str,HDF5DatasetDefinition] = MappingProxyType(
                                                        {"TRI": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/TRI",(NO_DIM_CONSTRAINTS,3)),
                                                        "QUAD": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/QUAD",(NO_DIM_CONSTRAINTS,4)),
                                                        "CURVE_FACE": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/CURVE_FACE",(NO_DIM_CONSTRAINTS,3))
                                                        })

    DATASETS_3D_MAPS: MappingProxyType[str,HDF5DatasetDefinition] = MappingProxyType(
                                                        {"HEX": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/HEX",(NO_DIM_CONSTRAINTS,)),
                                                        "TET": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/TET",(NO_DIM_CONSTRAINTS,)),
                                                        "PYR": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/PYR",(NO_DIM_CONSTRAINTS,)),
                                                        "PRISM": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MAPS/PRISM",(NO_DIM_CONSTRAINTS,))
                                                        })

    DATASETS_3D_MESH: MappingProxyType[str,HDF5DatasetDefinition] = MappingProxyType(
                                                        {"HEX": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/HEX",(NO_DIM_CONSTRAINTS,6)),
                                                        "TET": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/TET",(NO_DIM_CONSTRAINTS,4)),
                                                        "PYR": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/PYR",(NO_DIM_CONSTRAINTS,5)),
                                                        "PRISM": HDF5DatasetDefinition("NEKTAR/GEOMETRY/MESH/PRISM",(NO_DIM_CONSTRAINTS,5))
                                                        })
    
    DATASETS_MAPS: MappingProxyType[str,HDF5DatasetDefinition] = MappingProxyType({**DATASETS_MANDATORY_MAPS,**DATASETS_1D_MAPS,
                                                                                   **DATASETS_2D_MAPS,**DATASETS_3D_MAPS})

    DATASETS_MESH: MappingProxyType[str,HDF5DatasetDefinition] = MappingProxyType({**DATASETS_MANDATORY_MESH,**DATASETS_1D_MESH,
                                                                                   **DATASETS_2D_MESH,**DATASETS_3D_MESH})

    def __init__(self,f: h5py.File):        
        self.file: h5py.File = f

        self.datasets_present: Set[str] = set()
        self.element_number: Dict[str] = {}
        
    def validate(self):
        #check mandatory groups and datasets first
        for group in GeometrySchemaHDF5Validator.BASE_GROUPS.values():
            group.validate(self.file)
        
        self._check_mandatory_dataset(GeometrySchemaHDF5Validator.DATASETS_MANDATORY_MAPS)
        self._check_mandatory_dataset(GeometrySchemaHDF5Validator.DATASETS_MANDATORY_MESH)
        self._check_mandatory_dataset(GeometrySchemaHDF5Validator.DATASETS_1D_MAPS)
        self._check_mandatory_dataset(GeometrySchemaHDF5Validator.DATASETS_1D_MESH)

        self._check_optional_dataset(GeometrySchemaHDF5Validator.DATASETS_2D_MAPS)
        self._check_optional_dataset(GeometrySchemaHDF5Validator.DATASETS_2D_MESH)
        self._check_optional_dataset(GeometrySchemaHDF5Validator.DATASETS_3D_MAPS)
        self._check_optional_dataset(GeometrySchemaHDF5Validator.DATASETS_3D_MESH)

        #now check that each pair exists and have consistent shapes
        #maps can't be defined without corresponding mesh and vice versa
        for key in self.datasets_present:
            #curve nodes only exception to above rule
            if key != "CURVE_NODES":
                self._check_pair_of_validated_datasets(GeometrySchemaHDF5Validator.DATASETS_MAPS.get(key),GeometrySchemaHDF5Validator.DATASETS_MESH.get(key))



    def _check_mandatory_dataset(self,mandatory_dataset: MappingProxyType[str,HDF5DatasetDefinition]) -> None:
        """Helper function. Checks mandatiory datasets and if valid, adds to self.datasets_present the key

        Args:
            mandatory_dataset (MappingProxyType[str,HDF5DatasetDefinition]): _description_
        
        Raises:
            HDF5SchemaException: _description_
        """
        for key,dataset in mandatory_dataset.items():
            if dataset.validate(self.file):
                self.datasets_present.add(key)

    def _check_optional_dataset(self,optional_dataset: MappingProxyType[str,HDF5DatasetDefinition]) -> None:
        """Helper function. Checks mandatiory datasets and if valid, adds to self.datasets_present the key

        Args:
            optional_dataset (MappingProxyType[str,HDF5DatasetDefinition]): _description_

        Raises:
            HDF5SchemaException: _description_
        """
        for key,dataset in optional_dataset.items():
            try:
                dataset.validate(self.file)
                self.datasets_present.add(key)
            except HDF5SchemaExistenceException:
                pass #optional, so allow if doesn't exist, but any other definition error should be re-raised
            except Exception:
                raise

    def _check_pair_of_validated_datasets(self, dataset_1: HDF5DatasetDefinition, dataset_2: HDF5DatasetDefinition):
        """_summary_

        Args:
            dataset_1 (HDF5DatasetDefinition): _description_
            dataset_2 (HDF5DatasetDefinition): _description_

        Raises:
            HDF5SchemaException: _description_
        """
        data1 = self.file.get(dataset_1.get_path())
        data2 = self.file.get(dataset_2.get_path())

        if (data1 is not None and data2 is None) or (data2 is not None and data1 is None):
            raise HDF5SchemaMissingDatasetException(self.file, f"HDF5 Schema Error: {dataset_1} and {dataset_2} should be defined together, but one exists and other doesn't")

        if data1 is not None and data2 is not None:
            if isinstance(data1, h5py.Dataset) and isinstance(data2, h5py.Dataset):
                shape1 = data1.shape
                shape2 = data2.shape
                if shape1[0] != shape2[0]:
                    raise HDF5SchemaInconsistentException(self.file, f"HDF5 Schema Error: {dataset_1} has shape {shape1} and {dataset_2} has shape {shape2}. Inconsistent lengths {shape1[0]} != {shape2[0]}")

    #TODO
    def _check_element_construction(self,datasets_present: Set[str]):
        #3D elements can only be defined if corresponding 2D elements are present
        pass

class OutputSchemaHDF5Validator:

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
        for group in OutputSchemaHDF5Validator.BASE_GROUPS:
            group.validate(self.file)

        for dataset in OutputSchemaHDF5Validator.EXPECTED_DATASETS:
            dataset.validate(self.file)

        #there should be other groups defined based on decomposition
        #DECOMPOSITION contains sequence of seven numbres, seventh number
        #is a hash denoting a group containing expansion information
        decomposition_dataset: h5py.Dataset = self.file["NEKTAR/DECOMPOSITION"]
        self._check_decomposition(decomposition_dataset)

    def _check_decomposition(self, decomposition_dataset: h5py.Dataset):
        if decomposition_dataset.shape[0] % 7 != 0:
            raise HDF5SchemaInconsistentException(self.file,"HDF5 Schema Error: Decomposition shape should be multiple of 7")

        expected_groups: List[HDF5GroupDefinition] = []
        for i in range(6,decomposition_dataset.shape[0],7):

            hash = decomposition_dataset[i]
            expected_groups.append(HDF5GroupDefinition(f"NEKTAR/{hash}",attributes=["BASIS","FIELDS","NUMMODESPERDIR","SHAPE"]))

        for group in expected_groups:
            group.validate(self.file)