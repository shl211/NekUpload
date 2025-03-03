from typing import Tuple, Optional
from .data_type import IntegrationPoint,BasisType,Elements
from abc import ABC, abstractmethod
import logging

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

#preferred interface for constructing data
class ExpansionBuilder(ABC):
    def __init__(self,element: Elements):
        self.expansion = ExpansionData(element)
        self.element = element
        if not self._verify():
            msg = f"{__class__}: Expansion not defined for {self.element}"
            raise ValueError(msg)

    def _verify(self) -> bool:
        valid_elements = {Elements.SEG,Elements.TRI,Elements.QUAD,Elements.HEX,
                          Elements.TET,Elements.PRISM,Elements.PYR}

        return self.element in valid_elements

    @abstractmethod
    def add_basis(self):
        pass

    @abstractmethod
    def add_points(self):
        pass

    @abstractmethod
    def add_num_modes(self,num_modes: int):
        pass

    @abstractmethod
    def add_fields(self):
        pass

    def getExpansion(self):
        return self.expansion

#see nektar/library/SpatialDomains/MeshGraph.cpp DefineBasisKeyFromExpansionType for default expansions
class ModifiedExpansionBuilder(ExpansionBuilder):
    def add_basis(self):
        basis_map = {
            Elements.SEG: (BasisType.MODIFIED_A,),
            Elements.QUAD: (BasisType.MODIFIED_A, BasisType.MODIFIED_A),
            Elements.HEX: (BasisType.MODIFIED_A, BasisType.MODIFIED_A, BasisType.MODIFIED_A),
            Elements.TRI: (BasisType.MODIFIED_A, BasisType.MODIFIED_B),
            Elements.TET: (BasisType.MODIFIED_A, BasisType.MODIFIED_B, BasisType.MODIFIED_C),
            Elements.PYR: (BasisType.MODIFIED_A, BasisType.MODIFIED_A, BasisType.MODIFIED_PYR_C),
            Elements.PRISM: (BasisType.MODIFIED_A, BasisType.MODIFIED_A, BasisType.MODIFIED_B)
        }

        self.expansion.add_basis(basis_map.get(self.element, ()))

    def add_points(self):
        integration_points_map = {
            Elements.SEG: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,),
            Elements.QUAD: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE),
            Elements.HEX: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE),
            Elements.TRI: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0),
            Elements.TET: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0, IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0),
            Elements.PYR: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0),
            Elements.PRISM: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
        }
        
        self.expansion.add_integration_points(integration_points_map.get(self.element, ()))

    def add_num_modes(self, num_modes: int) -> None:
        quad_offset = 1
        total_points = num_modes + quad_offset
        
        num_modes_map = {
            Elements.SEG: (num_modes,),
            Elements.QUAD: (num_modes, num_modes),
            Elements.HEX: (num_modes, num_modes, num_modes),
            Elements.TRI: (num_modes, num_modes),
            Elements.TET: (num_modes, num_modes, num_modes),
            Elements.PYR: (num_modes, num_modes, num_modes),
            Elements.PRISM: (num_modes, num_modes, num_modes)
        }
        
        num_points_map = {
            Elements.SEG: (total_points,),
            Elements.QUAD: (total_points, total_points),
            Elements.HEX: (total_points, total_points, total_points),
            Elements.TRI: (total_points, total_points - 1),
            Elements.TET: (total_points, total_points - 1, total_points - 1),
            Elements.PYR: (total_points, total_points, total_points),
            Elements.PRISM: (total_points, total_points, total_points - 1)
        }
        
        self.expansion.add_num_modes(num_modes_map.get(self.element, ()))
        self.expansion.add_num_points(num_points_map.get(self.element, ()))

    def add_fields(self):
        pass

class ModifiedQuadPlus1ExpansionBuilder(ModifiedExpansionBuilder):
    def add_num_modes(self, num_modes: int) -> None:
        quad_offset = 2
        total_points = num_modes + quad_offset
        
        num_modes_map = {
            Elements.SEG: (num_modes,),
            Elements.QUAD: (num_modes, num_modes),
            Elements.HEX: (num_modes, num_modes, num_modes),
            Elements.TRI: (num_modes, num_modes),
            Elements.TET: (num_modes, num_modes, num_modes),
            Elements.PYR: (num_modes, num_modes, num_modes),
            Elements.PRISM: (num_modes, num_modes, num_modes)
        }
        
        num_points_map = {
            Elements.SEG: (total_points,),
            Elements.QUAD: (total_points, total_points),
            Elements.HEX: (total_points, total_points, total_points),
            Elements.TRI: (total_points, total_points - 1),
            Elements.TET: (total_points, total_points - 1, total_points - 1),
            Elements.PYR: (total_points, total_points, total_points),
            Elements.PRISM: (total_points, total_points, total_points - 1)
        }
        
        self.expansion.add_num_modes(num_modes_map.get(self.element, ()))
        self.expansion.add_num_points(num_points_map.get(self.element, ()))

class ModifiedQuadPlus2ExpansionBuilder(ModifiedExpansionBuilder):
    def add_num_modes(self, num_modes: int) -> None:
        quad_offset = 3
        total_points = num_modes + quad_offset
        
        num_modes_map = {
            Elements.SEG: (num_modes,),
            Elements.QUAD: (num_modes, num_modes),
            Elements.HEX: (num_modes, num_modes, num_modes),
            Elements.TRI: (num_modes, num_modes),
            Elements.TET: (num_modes, num_modes, num_modes),
            Elements.PYR: (num_modes, num_modes, num_modes),
            Elements.PRISM: (num_modes, num_modes, num_modes)
        }
        
        num_points_map = {
            Elements.SEG: (total_points,),
            Elements.QUAD: (total_points, total_points),
            Elements.HEX: (total_points, total_points, total_points),
            Elements.TRI: (total_points, total_points - 1),
            Elements.TET: (total_points, total_points - 1, total_points - 1),
            Elements.PYR: (total_points, total_points, total_points),
            Elements.PRISM: (total_points, total_points, total_points - 1)
        }
        
        self.expansion.add_num_modes(num_modes_map.get(self.element, ()))
        self.expansion.add_num_points(num_points_map.get(self.element, ()))

class ModifiedGLLRadau10ExpansionBuilder(ModifiedExpansionBuilder):
    def add_points(self):
        integration_points_map = {
            Elements.SEG: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,),
            Elements.QUAD: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE),
            Elements.HEX: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE),
            Elements.TRI: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0),
            Elements.TET: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0, IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0),
            Elements.PYR: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0),
            Elements.PRISM: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
        }
        
        self.expansion.add_integration_points(integration_points_map.get(self.element, ()))

class GLLLagranageExpansionBuilder(ExpansionBuilder):
    def _verify(self) ->  bool:
        valid_elements = {Elements.SEG,Elements.TRI,Elements.QUAD,Elements.HEX}

        return self.element in valid_elements
    
    def add_basis(self):
        basis_map = {
            Elements.SEG: (BasisType.GLL_LAGRANGE,),
            Elements.TRI: (BasisType.GLL_LAGRANGE, BasisType.ORTHO_B),
            Elements.QUAD: (BasisType.GLL_LAGRANGE, BasisType.GLL_LAGRANGE),
            Elements.HEX: (BasisType.GLL_LAGRANGE, BasisType.GLL_LAGRANGE, BasisType.GLL_LAGRANGE)
        }

        self.expansion.add_basis(basis_map.get(self.element, ()))
        
    def add_points(self):
        integration_points_map = {
            Elements.SEG: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,),
            Elements.TRI: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0),
            Elements.QUAD: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE),
            Elements.HEX: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
        }

        self.expansion.add_integration_points(integration_points_map.get(self.element, ()))
        
    def add_num_modes(self, num_modes: int):
        quad_offset = 1
        total_points = num_modes + quad_offset
        
        num_modes_map = {
            Elements.SEG: (num_modes,),
            Elements.TRI: (num_modes, num_modes),
            Elements.QUAD: (num_modes, num_modes),
            Elements.HEX: (num_modes, num_modes, num_modes)
        }
        
        num_points_map = {
            Elements.SEG: (total_points,),
            Elements.TRI: (total_points, total_points - 1),
            Elements.QUAD: (total_points, total_points),
            Elements.HEX: (total_points, total_points, total_points)
        }
        
        self.expansion.add_num_modes(num_modes_map.get(self.element, ()))
        self.expansion.add_num_points(num_points_map.get(self.element, ()))
        
    def add_fields(self):
        pass

class GaussLagrangeExpansionBuilder(ExpansionBuilder):
    def _verify(self) ->  bool:
        valid_elements = {Elements.SEG,Elements.QUAD,Elements.HEX}

        return self.element in valid_elements        

    def add_basis(self):
        basis_map = {
            Elements.SEG: (BasisType.GAUSS_LAGRANGE,),
            Elements.QUAD: (BasisType.GAUSS_LAGRANGE, BasisType.GAUSS_LAGRANGE),
            Elements.HEX: (BasisType.GAUSS_LAGRANGE, BasisType.GAUSS_LAGRANGE, BasisType.GAUSS_LAGRANGE)
        }

        self.expansion.add_basis(basis_map.get(self.element, ()))

    def add_points(self):
        integration_points_map = {
            Elements.SEG: (IntegrationPoint.GAUSS_GAUSS_LEGENDRE,),
            Elements.QUAD: (IntegrationPoint.GAUSS_GAUSS_LEGENDRE, IntegrationPoint.GAUSS_GAUSS_LEGENDRE),
            Elements.HEX: (IntegrationPoint.GAUSS_GAUSS_LEGENDRE, IntegrationPoint.GAUSS_GAUSS_LEGENDRE, IntegrationPoint.GAUSS_GAUSS_LEGENDRE)
        }

        self.expansion.add_integration_points(integration_points_map.get(self.element, ()))

    def add_num_modes(self, num_modes):
        num_modes_map = {
            Elements.SEG: (num_modes,),
            Elements.QUAD: (num_modes, num_modes),
            Elements.HEX: (num_modes, num_modes, num_modes)
        }
        
        num_points_map = {
            Elements.SEG: (num_modes,),
            Elements.QUAD: (num_modes, num_modes),
            Elements.HEX: (num_modes, num_modes, num_modes)
        }
        
        self.expansion.add_num_modes(num_modes_map.get(self.element, ()))
        self.expansion.add_num_points(num_points_map.get(self.element, ()))
    
    def add_fields(self):
        pass

class OrthogonalExpansionBuilder(ExpansionBuilder):
    def _verify(self) -> bool:
        valid_elements = {Elements.SEG,Elements.TRI,Elements.QUAD,Elements.TET}
        return self.element in valid_elements

    def add_basis(self):
        basis_map = {
            Elements.SEG: (BasisType.ORTHO_A,),
            Elements.TRI: (BasisType.ORTHO_A, BasisType.ORTHO_B),
            Elements.QUAD: (BasisType.ORTHO_A, BasisType.ORTHO_A),
            Elements.TET: (BasisType.ORTHO_A, BasisType.ORTHO_B, BasisType.ORTHO_C)
        }

        self.expansion.add_basis(basis_map.get(self.element, ()))

    def add_points(self):
        integration_points_map = {
            Elements.SEG: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,),
            Elements.TRI: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0),
            Elements.QUAD: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE),
            Elements.TET: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0, IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0)
        }

        self.expansion.add_integration_points(integration_points_map.get(self.element, ()))

    def add_num_modes(self, num_modes):
        total_points = num_modes + 1
        num_modes_map = {
            Elements.SEG: (num_modes,),
            Elements.TRI: (num_modes, num_modes),
            Elements.QUAD: (num_modes, num_modes),
            Elements.TET: (num_modes, num_modes, num_modes)
        }
        
        num_points_map = {
            Elements.SEG: (total_points,),
            Elements.TRI: (total_points, total_points - 1),
            Elements.QUAD: (total_points, total_points),
            Elements.TET: (total_points, total_points - 1, total_points - 1)
        }
        
        self.expansion.add_num_modes(num_modes_map.get(self.element, ()))
        self.expansion.add_num_points(num_points_map.get(self.element, ()))
        
    def add_fields(self):
        pass

class GLLLagrangeSEMExpansionBuilder(GLLLagranageExpansionBuilder):
    def _verify(self) -> bool:
        valid_elements = {Elements.SEG, Elements.QUAD, Elements.HEX}
        return self.element in valid_elements

    def add_num_modes(self, num_modes: int):
        num_modes_map = {
            Elements.SEG: (num_modes,),
            Elements.QUAD: (num_modes, num_modes),
            Elements.HEX: (num_modes, num_modes, num_modes)
        }
        
        num_points_map = {
            Elements.SEG: (num_modes,),
            Elements.QUAD: (num_modes, num_modes),
            Elements.HEX: (num_modes, num_modes, num_modes)
        }
        
        self.expansion.add_num_modes(num_modes_map.get(self.element, ()))
        self.expansion.add_num_points(num_points_map.get(self.element, ()))

class FourierExpansionBuilder(ExpansionBuilder):
    def _verify(self) -> bool:
        valid_elements = {Elements.SEG, Elements.QUAD, Elements.HEX}
        return self.element in valid_elements

    def add_basis(self):
        basis_map = {
            Elements.SEG: (BasisType.FOURIER,),
            Elements.QUAD: (BasisType.FOURIER, BasisType.FOURIER),
            Elements.HEX: (BasisType.FOURIER, BasisType.FOURIER, BasisType.FOURIER)
        }
        
        self.expansion.add_basis(basis_map.get(self.element, ()))

    def add_points(self):
        integration_points_map = {
            Elements.SEG: (IntegrationPoint.FOURIER_EVENLY_SPACED,),
            Elements.QUAD: (IntegrationPoint.FOURIER_EVENLY_SPACED, IntegrationPoint.FOURIER_EVENLY_SPACED),
            Elements.HEX: (IntegrationPoint.FOURIER_EVENLY_SPACED, IntegrationPoint.FOURIER_EVENLY_SPACED, IntegrationPoint.FOURIER_EVENLY_SPACED)
        }
        
        self.expansion.add_integration_points(integration_points_map.get(self.element, ()))

    def add_num_modes(self, num_modes):
        num_modes_map = {
            Elements.SEG: (num_modes,),
            Elements.QUAD: (num_modes, num_modes),
            Elements.HEX: (num_modes, num_modes, num_modes)
        }
        
        num_points_map = {
            Elements.SEG: (num_modes,),
            Elements.QUAD: (num_modes, num_modes),
            Elements.HEX: (num_modes, num_modes, num_modes)
        }
        
        self.expansion.add_num_modes(num_modes_map.get(self.element, ()))
        self.expansion.add_num_points(num_points_map.get(self.element, ()))
        
    def add_fields(self):
        pass

class FourierSingleModeExpansionBuilder(FourierExpansionBuilder):
    def add_basis(self):
        basis_map = {
            Elements.SEG: (BasisType.FOURIER_SINGLE_MODE,),
            Elements.QUAD: (BasisType.FOURIER_SINGLE_MODE, BasisType.FOURIER_SINGLE_MODE),
            Elements.HEX: (BasisType.FOURIER_SINGLE_MODE, BasisType.FOURIER_SINGLE_MODE, BasisType.FOURIER_SINGLE_MODE)
        }
        
        self.expansion.add_basis(basis_map.get(self.element, ()))

    def add_points(self):
        integration_points_map = {
            Elements.SEG: (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,),
            Elements.QUAD: (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED, IntegrationPoint.FOURIER_SINGLE_MODE_SPACED),
            Elements.HEX: (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED, IntegrationPoint.FOURIER_SINGLE_MODE_SPACED, IntegrationPoint.FOURIER_SINGLE_MODE_SPACED)
        }
        
        self.expansion.add_integration_points(integration_points_map.get(self.element, ()))

class FourierHalfModeReExpansionBuilder(FourierSingleModeExpansionBuilder):
    def add_basis(self):
        basis_map = {
            Elements.SEG: (BasisType.FOURIER_HALF_MODE_RE,),
            Elements.QUAD: (BasisType.FOURIER_HALF_MODE_RE, BasisType.FOURIER_HALF_MODE_RE),
            Elements.HEX: (BasisType.FOURIER_HALF_MODE_RE, BasisType.FOURIER_HALF_MODE_RE, BasisType.FOURIER_HALF_MODE_RE)
        }
        
        self.expansion.add_basis(basis_map.get(self.element, ()))

class FourierHalfModeImExpansionBuilder(FourierSingleModeExpansionBuilder):
    def add_basis(self):
        basis_map = {
            Elements.SEG: (BasisType.FOURIER_HALF_MODE_IM,),
            Elements.QUAD: (BasisType.FOURIER_HALF_MODE_IM, BasisType.FOURIER_HALF_MODE_IM),
            Elements.HEX: (BasisType.FOURIER_HALF_MODE_IM, BasisType.FOURIER_HALF_MODE_IM, BasisType.FOURIER_HALF_MODE_IM)
        }
        
        self.expansion.add_basis(basis_map.get(self.element, ()))

class ChebyshevExpansionBuilder(ExpansionBuilder):
    def _verify(self) -> bool:
        valid_elements = {Elements.SEG, Elements.QUAD, Elements.HEX}
        return self.element in valid_elements

    def add_basis(self):
        basis_map = {
            Elements.SEG: (BasisType.CHEBYSHEV,),
            Elements.QUAD: (BasisType.CHEBYSHEV, BasisType.CHEBYSHEV),
            Elements.HEX: (BasisType.CHEBYSHEV, BasisType.CHEBYSHEV, BasisType.CHEBYSHEV)
        }
        
        self.expansion.add_basis(basis_map.get(self.element, ()))

    def add_points(self):
        integration_points_map = {
            Elements.SEG: (IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV,),
            Elements.QUAD: (IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV, IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV),
            Elements.HEX: (IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV, IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV, IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV)
        }
        
        self.expansion.add_integration_points(integration_points_map.get(self.element, ()))

    def add_num_modes(self, num_modes):
        num_modes_map = {
            Elements.SEG: (num_modes,),
            Elements.QUAD: (num_modes, num_modes),
            Elements.HEX: (num_modes, num_modes, num_modes)
        }
        
        num_points_map = {
            Elements.SEG: (num_modes,),
            Elements.QUAD: (num_modes, num_modes),
            Elements.HEX: (num_modes, num_modes, num_modes)
        }
        
        self.expansion.add_num_modes(num_modes_map.get(self.element, ()))
        self.expansion.add_num_points(num_points_map.get(self.element, ()))
        
    def add_fields(self):
        pass

class FourierChebyshevExpansionBuilder(ExpansionBuilder):
    def _verify(self) -> bool:
        valid_elements = {Elements.QUAD}
        return self.element in valid_elements

    def add_basis(self):
        if self.element == Elements.QUAD:
            self.expansion.add_basis((BasisType.FOURIER, BasisType.CHEBYSHEV))

    def add_points(self):
        if self.element == Elements.QUAD:
            self.expansion.add_integration_points((IntegrationPoint.FOURIER_EVENLY_SPACED, IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV))

    def add_num_modes(self, num_modes):
        if self.element == Elements.QUAD:
            self.expansion.add_num_modes((num_modes, num_modes))
            self.expansion.add_num_points((num_modes, num_modes))

    def add_fields(self):
        pass

class ChebyshevFourierExpansionBuilder(ExpansionBuilder):
    def _verify(self) -> bool:
        valid_elements = {Elements.QUAD}
        return self.element in valid_elements

    def add_basis(self):
        if self.element == Elements.QUAD:
            self.expansion.add_basis((BasisType.CHEBYSHEV, BasisType.FOURIER))

    def add_points(self):
        if self.element == Elements.QUAD:
            self.expansion.add_integration_points((IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV, IntegrationPoint.FOURIER_EVENLY_SPACED))

    def add_num_modes(self, num_modes):
        if self.element == Elements.QUAD:
            self.expansion.add_num_modes((num_modes, num_modes))
            self.expansion.add_num_points((num_modes, num_modes))

    def add_fields(self):
        pass

class ModifiedFourierExpansionBuilder(ExpansionBuilder):
    def _verify(self) -> bool:
        valid_elements = {Elements.QUAD}
        return self.element in valid_elements

    def add_basis(self):
        if self.element == Elements.QUAD:
            self.expansion.add_basis((BasisType.FOURIER, BasisType.MODIFIED_A))

    def add_points(self):
        if self.element == Elements.QUAD:
            self.expansion.add_integration_points((IntegrationPoint.FOURIER_EVENLY_SPACED, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE))

    def add_num_modes(self, num_modes):
        if self.element == Elements.QUAD:
            self.expansion.add_num_modes((num_modes, num_modes))
            self.expansion.add_num_points((num_modes, num_modes + 1))

    def add_fields(self):
        pass

#################################################################################
# Need to check what combos are actually allowed and whether there are any rules?
# Also untested
#
class Custom1DComboExpansionBuilder(ExpansionBuilder):
    def _is_input_dim_consistent(self,size: int) -> bool:
        if self.element == Elements.SEG:
            return size == 1
        if self.element == Elements.TRI or self.element == Elements.QUAD:
            return size == 2
        if self.element == Elements.HEX or self.element == Elements.TET or self.element == Elements.PRISM or self.element == Elements.PYR:
            return size == 3

        return False
    
    def add_basis(self,basis: Tuple[BasisType]) -> None:
        if self._is_input_dim_consistent(self,len(basis)):
            self.expansion.add_basis(basis)
        else:
            raise ValueError(f"{self.element} has  inconsistent dimensions with input basis: {basis}")

    def add_points(self,integr_points: Tuple[IntegrationPoint]):
        if self._is_input_dim_consistent(self,len(integr_points)):
            self.expansion.add_basis(integr_points)
        else:
            raise ValueError(f"{self.element} has  inconsistent dimensions with input integration points: {integr_points}")

    def add_num_modes(self, num_modes:Tuple[int], num_points:Tuple[int]):
        if self._is_input_dim_consistent(self,len(num_modes)):
            self.expansion.add_num_modes(num_modes)
        else:
            raise ValueError(f"{self.element} has  inconsistent dimensions with input num_modes: {num_modes}")

        if self._is_input_dim_consistent(self,len(num_points)):
            self.expansion.add_num_points(num_points)
        else:
            raise ValueError(f"{self.element} has  inconsistent dimensions with input num_points: {num_points}")

    def add_fields(self):
        pass
