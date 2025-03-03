from typing import Tuple, Optional
from .data_type import IntegrationPoint,BasisType,Elements

#Note -> See MeshGraph.cpp/DefineBasisKeyFromExpansionTypeHomo
#  ReadExpansionInfo etc. for more info in terms of how expansions are handled

class ExpansionData():
    def __init__(self,element: Elements):
        self.element = element
        
        self.num_modes = None
        self.num_points = None
        self.fields = None
        self.num_integration_points = None
        self.integration_point_type = None
        self.basis = None

    def add_basis(self,basis_type: Tuple[BasisType]):
        self.basis = basis_type

    def add_integration_points(self,integration_points: Tuple[IntegrationPoint]):
        self.integration_point_type = integration_points

    def add_num_modes(self,num_modes: Tuple[int]):
        self.num_modes = num_modes

    def add_num_points(self,num_points: Tuple[int]):
        self.num_points = num_points

    def verify():
        pass