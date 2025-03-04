from typing import Tuple, Optional, Dict, Callable
from .data_type import IntegrationPoint,BasisType,Elements
from abc import ABC, abstractmethod
import logging
from types import MappingProxyType

class ExpansionValidationException(Exception):
    """Custom exception for errors in expansion validation."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

#Note -> See MeshGraph.cpp/DefineBasisKeyFromExpansionTypeHomo
#  ReadExpansionInfo etc. for more info in terms of how expansions are handled

class ExpansionDefinition():

    @staticmethod
    def _compute_tri_coefficients(num_modes_0,num_modes_1):
        return num_modes_0 * (num_modes_0 - 1) // 2 + num_modes_0 * (num_modes_1 - num_modes_0)

    #TODO optimise this if needed
    @staticmethod
    def _compute_tet_coefficients(num_modes_0,num_modes_1,num_modes_2):
        num_coeffs = 0
        for a in range(num_modes_0):
            for b in range(num_modes_1 - a):
                for c in range(num_modes_2-a-b):
                    num_coeffs += 1

        return num_coeffs
    
    #TODO optimise this if needed
    @staticmethod
    def _compute_pyr_coefficients(num_modes_0,num_modes_1,num_modes_2):
        num_coeffs = 0
        for a in range(num_modes_0):
            for b in range(num_modes_1):
                for c in range(num_modes_2-max(a,b)):
                    num_coeffs += 1

        return num_coeffs

    DIMENSIONS: MappingProxyType[Elements,int] = MappingProxyType({
                                        Elements.SEG: 1,
                                        Elements.QUAD: 2,Elements.TRI: 2,
                                        Elements.HEX: 3,Elements.TET: 3,Elements.PYR: 3, Elements.PRISM: 3
                                    })

    NUMBER_OF_COEFFICIENTS: MappingProxyType[Elements,Callable[[Tuple[int,...]],int]] = MappingProxyType({
                                        Elements.SEG: lambda num_modes: num_modes[0],
                                        Elements.QUAD: lambda num_modes: num_modes[0] * num_modes[1],
                                        Elements.TRI: lambda num_modes: ExpansionDefinition._compute_tri_coefficients(num_modes[0],num_modes[1]),
                                        Elements.HEX: lambda num_modes: num_modes[0]*num_modes[1]*num_modes[2],
                                        Elements.PYR: lambda num_modes: ExpansionDefinition._compute_pyr_coefficients(num_modes[0],num_modes[1],num_modes[2]),
                                        Elements.PRISM: lambda num_modes: num_modes[1] * ExpansionDefinition._compute_tri_coefficients(num_modes[0],num_modes[2]),
                                        Elements.TET: lambda num_modes: ExpansionDefinition._compute_tet_coefficients(num_modes[0],num_modes[1],num_modes[2]),
                                    })

    def __init__(self,
                element: Elements,
                basis_type: Tuple[BasisType,...]=None,
                num_modes: Tuple[int,...]=None,
                integration_point_type: Tuple[IntegrationPoint,...]=None,
                num_points: Tuple[int,...]=None,
                fields: Tuple[str,...]=None):
        
        self.element = element
        self.basis: Tuple[BasisType,...] = basis_type
        self.num_points: Tuple[int,...] = num_points
        self.integration_point_type: Tuple[IntegrationPoint,...] = integration_point_type
        self.num_modes: Tuple[int,...] = num_modes
        
        self.fields: Tuple[str] = fields
        
        #make sure only valid definitions lead to initialisation
        self._validate()

    def _validate(self):
        """Check expansion definition is correct.
        """
        expected_dim = ExpansionDefinition.DIMENSIONS[self.element]

        if len(self.num_modes) != expected_dim:
            raise ExpansionValidationException(f"Element {self.element} expects dimension {expected_dim}, modes are: {self.num_modes}")
        if len(self.num_points) != expected_dim:
            raise ExpansionValidationException(f"Element {self.element} expects dimension {expected_dim}, points are: {self.num_points}")
        if len(self.integration_point_type) != expected_dim:
            raise ExpansionValidationException(f"Element {self.element} expects dimension {expected_dim}, point types are: {self.integration_point_type}")
        if len(self.basis) != expected_dim:
            raise ExpansionValidationException(f"Element {self.element} expects dimension {expected_dim}, basis are: {self.basis}")

        return True

    def get_num_coefficients(self):
        """Given the expansion definition, compute number of coefficients to be computed for each
        element of this expansion type.

        Returns:
            _type_: _description_
        """
        num_coeff_callable: Callable[[Tuple[int,...]],int] = ExpansionDefinition.NUMBER_OF_COEFFICIENTS[self.element]
        return num_coeff_callable(self.num_modes)

#preferred interface for constructing data
class ExpansionFactory(ABC):
    BASIS_MAP: MappingProxyType[Elements,Tuple[BasisType,...]]
    INTEGRATION_POINTS_MAP: MappingProxyType[Elements,Tuple[IntegrationPoint,...]]
    NUM_MODES_MAP: MappingProxyType[Elements,Callable[[int],Tuple[int,...]]]
    NUM_POINTS_MAP: MappingProxyType[Elements,Callable[[int],Tuple[int,...]]]

    def __init__(self):
        pass

    def get_expansion(self,element: Elements, nummodes: int,fields: Optional[Tuple[str,...]]=None):
        basis: Optional[BasisType] = self.BASIS_MAP.get(element,None)
        integration_points: Optional[IntegrationPoint] = self.INTEGRATION_POINTS_MAP.get(element,None)
        
        num_modes_callable: Optional[Callable[[int],Tuple[int,...]]] = self.NUM_MODES_MAP.get(element,None)
        num_points_callable: Optional[Callable[[int],Tuple[int,...]]] = self.NUM_POINTS_MAP.get(element,None)
        
        if basis and integration_points and num_modes_callable and num_points_callable:
            num_modes = num_modes_callable(nummodes)
            num_points = num_points_callable(nummodes)
            return ExpansionDefinition(element,basis,num_modes,integration_points,num_points,fields)
        else:
            raise ExpansionValidationException(f"{self.__class__.__name__} has no default definition for {element}")

#see nektar/library/SpatialDomains/MeshGraph.cpp for default expansions
class ModifiedExpansionFactory(ExpansionFactory):
    BASIS_MAP: MappingProxyType[Elements,Tuple[BasisType,...]] = MappingProxyType({
            Elements.SEG: (BasisType.MODIFIED_A,),
            Elements.TRI: (BasisType.MODIFIED_A, BasisType.MODIFIED_B),
            Elements.QUAD: (BasisType.MODIFIED_A, BasisType.MODIFIED_A),
            Elements.HEX: (BasisType.MODIFIED_A, BasisType.MODIFIED_A, BasisType.MODIFIED_A),
            Elements.PRISM: (BasisType.MODIFIED_A, BasisType.MODIFIED_A, BasisType.MODIFIED_B),
            Elements.PYR: (BasisType.MODIFIED_A, BasisType.MODIFIED_A, BasisType.MODIFIED_PYR_C),
            Elements.TET: (BasisType.MODIFIED_A, BasisType.MODIFIED_B, BasisType.MODIFIED_C),
        })
    
    INTEGRATION_POINTS_MAP: MappingProxyType[Elements,Tuple[IntegrationPoint]] = MappingProxyType({
            Elements.SEG: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,),
            Elements.QUAD: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE),
            Elements.TRI: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0),
            Elements.HEX: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE),
            Elements.PRISM: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0),
            Elements.PYR: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0),
            Elements.TET: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0, IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0),
        })
    
    NUM_MODES_MAP: MappingProxyType[Elements,Callable[[int],Tuple[int,...]]] = MappingProxyType({
            Elements.SEG: lambda nummodes: (nummodes,),
            Elements.QUAD: lambda nummodes: (nummodes, nummodes),
            Elements.TRI: lambda nummodes: (nummodes, nummodes),
            Elements.HEX: lambda nummodes: (nummodes, nummodes, nummodes),
            Elements.PRISM: lambda nummodes: (nummodes, nummodes, nummodes),
            Elements.PYR: lambda nummodes: (nummodes, nummodes, nummodes),
            Elements.TET: lambda nummodes: (nummodes, nummodes, nummodes),
        })

    NUM_POINTS_MAP: MappingProxyType[Elements,Callable[[int],Tuple[int,...]]] = MappingProxyType({
        Elements.SEG: lambda nummodes,quad_offset=1: (nummodes+quad_offset,),
        Elements.QUAD: lambda nummodes,quad_offset=1: (nummodes+quad_offset,nummodes+quad_offset),
        Elements.TRI: lambda nummodes,quad_offset=1: (nummodes+quad_offset, nummodes+quad_offset-1),
        Elements.HEX: lambda nummodes, quad_offset=1: (nummodes+quad_offset, nummodes+quad_offset, nummodes+quad_offset),
        Elements.PRISM: lambda nummodes, quad_offset=1: (nummodes+quad_offset,nummodes+quad_offset,nummodes+quad_offset-1),
        Elements.PYR: lambda nummodes, quad_offset=1: (nummodes+quad_offset,nummodes+quad_offset,nummodes+quad_offset),
        Elements.TET: lambda nummodes, quad_offset=1: (nummodes+quad_offset, nummodes+quad_offset-1, nummodes+quad_offset-1),
    })

class ModifiedQuadPlus1ExpansionFactory(ModifiedExpansionFactory):
    NUM_POINTS_MAP: MappingProxyType[Elements,Callable[[int],Tuple[int,...]]] = MappingProxyType({
        Elements.SEG: lambda nummodes,quad_offset=2: (nummodes+quad_offset,),
        Elements.QUAD: lambda nummodes,quad_offset=2: (nummodes+quad_offset,nummodes+quad_offset),
        Elements.TRI: lambda nummodes,quad_offset=2: (nummodes+quad_offset, nummodes+quad_offset-1),
        Elements.HEX: lambda nummodes, quad_offset=2: (nummodes+quad_offset, nummodes+quad_offset, nummodes+quad_offset),
        Elements.PRISM: lambda nummodes, quad_offset=2: (nummodes+quad_offset,nummodes+quad_offset,nummodes+quad_offset-1),
        Elements.PYR: lambda nummodes, quad_offset=2: (nummodes+quad_offset,nummodes+quad_offset,nummodes+quad_offset),
        Elements.TET: lambda nummodes, quad_offset=2: (nummodes+quad_offset, nummodes+quad_offset-1, nummodes+quad_offset-1),
    })

class ModifiedQuadPlus2ExpansionFactory(ModifiedExpansionFactory):
    NUM_POINTS_MAP: MappingProxyType[Elements,Callable[[int],Tuple[int,...]]] = MappingProxyType({
        Elements.SEG: lambda nummodes,quad_offset=3: (nummodes+quad_offset,),
        Elements.QUAD: lambda nummodes,quad_offset=3: (nummodes+quad_offset,nummodes+quad_offset),
        Elements.TRI: lambda nummodes,quad_offset=3: (nummodes+quad_offset, nummodes+quad_offset-1),
        Elements.HEX: lambda nummodes, quad_offset=3: (nummodes+quad_offset, nummodes+quad_offset, nummodes+quad_offset),
        Elements.PRISM: lambda nummodes, quad_offset=3: (nummodes+quad_offset,nummodes+quad_offset,nummodes+quad_offset-1),
        Elements.PYR: lambda nummodes, quad_offset=3: (nummodes+quad_offset,nummodes+quad_offset,nummodes+quad_offset),
        Elements.TET: lambda nummodes, quad_offset=3: (nummodes+quad_offset, nummodes+quad_offset-1, nummodes+quad_offset-1),
    })

class ModifiedGLLRadau10ExpansionFactory(ModifiedExpansionFactory):
    INTEGRATION_POINTS_MAP: MappingProxyType[Elements,Tuple[IntegrationPoint]] = MappingProxyType({
            Elements.SEG: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,),
            Elements.QUAD: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE),
            Elements.TRI: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0),
            Elements.HEX: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE),
            Elements.PRISM: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0),
            Elements.PYR: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0),
            Elements.TET: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0, IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0),
        })

class GLLLagranageExpansionFactory(ExpansionFactory):
    BASIS_MAP: MappingProxyType[Elements,Tuple[BasisType,...]] = MappingProxyType({
            Elements.SEG: (BasisType.GLL_LAGRANGE,),
            Elements.QUAD: (BasisType.GLL_LAGRANGE, BasisType.GLL_LAGRANGE),
            Elements.TRI: (BasisType.GLL_LAGRANGE, BasisType.ORTHO_B),
            Elements.HEX: (BasisType.GLL_LAGRANGE, BasisType.GLL_LAGRANGE, BasisType.GLL_LAGRANGE)
        })

    INTEGRATION_POINTS_MAP: MappingProxyType[Elements,Tuple[IntegrationPoint]] = MappingProxyType({
            Elements.SEG: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,),
            Elements.QUAD: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE),
            Elements.TRI: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0),
            Elements.HEX: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
        })
        
    NUM_MODES_MAP: MappingProxyType[Elements,Callable[[int],Tuple[int,...]]] = MappingProxyType({
            Elements.SEG: lambda nummodes: (nummodes,),
            Elements.QUAD: lambda nummodes: (nummodes, nummodes),
            Elements.TRI: lambda nummodes: (nummodes, nummodes),
            Elements.HEX: lambda nummodes: (nummodes, nummodes, nummodes),
        })

    NUM_POINTS_MAP: MappingProxyType[Elements,Callable[[int],Tuple[int,...]]] = MappingProxyType({
        Elements.SEG: lambda nummodes,quad_offset=1: (nummodes+quad_offset,),
        Elements.QUAD: lambda nummodes,quad_offset=1: (nummodes+quad_offset,nummodes+quad_offset),
        Elements.TRI: lambda nummodes,quad_offset=1: (nummodes+quad_offset, nummodes+quad_offset-1),
        Elements.HEX: lambda nummodes, quad_offset=1: (nummodes+quad_offset, nummodes+quad_offset, nummodes+quad_offset),
    })
class GLLLagrangeSEMExpansionFactory(GLLLagranageExpansionFactory):
    NUM_MODES_MAP: MappingProxyType[Elements,Callable[[int],Tuple[int,...]]] = MappingProxyType({
        Elements.SEG: lambda nummodes: (nummodes,),
        Elements.QUAD: lambda nummodes: (nummodes, nummodes),
        Elements.HEX: lambda nummodes: (nummodes, nummodes, nummodes),
    })

    NUM_POINTS_MAP: MappingProxyType[Elements,Callable[[int],Tuple[int,...]]] = MappingProxyType({
        Elements.SEG: lambda nummodes: (nummodes,),
        Elements.QUAD: lambda nummodes: (nummodes,nummodes),
        Elements.HEX: lambda nummodes: (nummodes, nummodes, nummodes),
    })

class GaussLagrangeExpansionFactory(ExpansionFactory):
    BASIS_MAP: MappingProxyType[Elements,Tuple[BasisType,...]] = MappingProxyType({
            Elements.SEG: (BasisType.GAUSS_LAGRANGE,),
            Elements.QUAD: (BasisType.GAUSS_LAGRANGE, BasisType.GAUSS_LAGRANGE),
            Elements.HEX: (BasisType.GAUSS_LAGRANGE, BasisType.GAUSS_LAGRANGE, BasisType.GAUSS_LAGRANGE)
        })

    INTEGRATION_POINTS_MAP: MappingProxyType[Elements,Tuple[IntegrationPoint]] = MappingProxyType({
            Elements.SEG: (IntegrationPoint.GAUSS_GAUSS_LEGENDRE,),
            Elements.QUAD: (IntegrationPoint.GAUSS_GAUSS_LEGENDRE, IntegrationPoint.GAUSS_GAUSS_LEGENDRE),
            Elements.HEX: (IntegrationPoint.GAUSS_GAUSS_LEGENDRE, IntegrationPoint.GAUSS_GAUSS_LEGENDRE, IntegrationPoint.GAUSS_GAUSS_LEGENDRE)
        })
        
    NUM_MODES_MAP: MappingProxyType[Elements,Callable[[int],Tuple[int,...]]] = MappingProxyType({
            Elements.SEG: lambda nummodes: (nummodes,),
            Elements.QUAD: lambda nummodes: (nummodes, nummodes),
            Elements.HEX: lambda nummodes: (nummodes, nummodes, nummodes),
        })

    NUM_POINTS_MAP: MappingProxyType[Elements,Callable[[int],Tuple[int,...]]] = MappingProxyType({
        Elements.SEG: lambda nummodes: (nummodes,),
        Elements.QUAD: lambda nummodes: (nummodes,nummodes),
        Elements.HEX: lambda nummodes: (nummodes, nummodes, nummodes),
    })

class OrthogonalExpansionFactory(ExpansionFactory):
    BASIS_MAP: MappingProxyType[Elements,Tuple[BasisType,...]] = MappingProxyType({
            Elements.SEG: (BasisType.ORTHO_A,),
            Elements.QUAD: (BasisType.ORTHO_A, BasisType.ORTHO_A),
            Elements.TRI: (BasisType.ORTHO_A, BasisType.ORTHO_B),
            Elements.TET: (BasisType.ORTHO_A, BasisType.ORTHO_B, BasisType.ORTHO_C)
        })

    INTEGRATION_POINTS_MAP: MappingProxyType[Elements,Tuple[IntegrationPoint]] = MappingProxyType({
            Elements.SEG: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,),
            Elements.QUAD: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE),
            Elements.TRI: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0),
            Elements.TET: (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE, IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0, IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0)
        })
        
    NUM_MODES_MAP: MappingProxyType[Elements,Callable[[int],Tuple[int,...]]] = MappingProxyType({
            Elements.SEG: lambda nummodes: (nummodes,),
            Elements.QUAD: lambda nummodes: (nummodes, nummodes),
            Elements.TRI: lambda nummodes: (nummodes, nummodes),
            Elements.TET: lambda nummodes: (nummodes, nummodes, nummodes),
        })

    NUM_POINTS_MAP: MappingProxyType[Elements,Callable[[int],Tuple[int,...]]] = MappingProxyType({
        Elements.SEG: lambda nummodes: (nummodes+1,),
        Elements.QUAD: lambda nummodes: (nummodes+1,nummodes+1),
        Elements.TRI: lambda nummodes: (nummodes+1,nummodes),
        Elements.TET: lambda nummodes: (nummodes+1, nummodes, nummodes),
    })

class FourierExpansionFactory(ExpansionFactory):
    BASIS_MAP: MappingProxyType[Elements,Tuple[BasisType,...]] = MappingProxyType({
            Elements.SEG: (BasisType.FOURIER,),
            Elements.QUAD: (BasisType.FOURIER, BasisType.FOURIER),
            Elements.HEX: (BasisType.FOURIER, BasisType.FOURIER, BasisType.FOURIER)
        })

    INTEGRATION_POINTS_MAP: MappingProxyType[Elements,Tuple[IntegrationPoint]] = MappingProxyType({
            Elements.SEG: (IntegrationPoint.FOURIER_EVENLY_SPACED,),
            Elements.QUAD: (IntegrationPoint.FOURIER_EVENLY_SPACED, IntegrationPoint.FOURIER_EVENLY_SPACED),
            Elements.HEX: (IntegrationPoint.FOURIER_EVENLY_SPACED, IntegrationPoint.FOURIER_EVENLY_SPACED, IntegrationPoint.FOURIER_EVENLY_SPACED)
        })
        
    NUM_MODES_MAP: MappingProxyType[Elements,Callable[[int],Tuple[int,...]]] = MappingProxyType({
            Elements.SEG: lambda nummodes: (nummodes,),
            Elements.QUAD: lambda nummodes: (nummodes, nummodes),
            Elements.HEX: lambda nummodes: (nummodes, nummodes, nummodes),
        })

    NUM_POINTS_MAP: MappingProxyType[Elements,Callable[[int],Tuple[int,...]]] = MappingProxyType({
        Elements.SEG: lambda nummodes: (nummodes,),
        Elements.QUAD: lambda nummodes: (nummodes,nummodes),
        Elements.HEX: lambda nummodes: (nummodes, nummodes, nummodes),
    })

class FourierSingleModeExpansionFactory(FourierExpansionFactory):
    BASIS_MAP: MappingProxyType[Elements,Tuple[BasisType,...]] = MappingProxyType({
        Elements.SEG: (BasisType.FOURIER_SINGLE_MODE,),
        Elements.QUAD: (BasisType.FOURIER_SINGLE_MODE, BasisType.FOURIER_SINGLE_MODE),
        Elements.HEX: (BasisType.FOURIER_SINGLE_MODE, BasisType.FOURIER_SINGLE_MODE, BasisType.FOURIER_SINGLE_MODE)
    })

    INTEGRATION_POINTS_MAP: MappingProxyType[Elements,Tuple[IntegrationPoint]] = MappingProxyType({
            Elements.SEG: (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,),
            Elements.QUAD: (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED, IntegrationPoint.FOURIER_SINGLE_MODE_SPACED),
            Elements.HEX: (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED, IntegrationPoint.FOURIER_SINGLE_MODE_SPACED, IntegrationPoint.FOURIER_SINGLE_MODE_SPACED)
        })

class FourierHalfModeReExpansionFactory(FourierSingleModeExpansionFactory):
    BASIS_MAP: MappingProxyType[Elements,Tuple[BasisType,...]] = MappingProxyType({
        Elements.SEG: (BasisType.FOURIER_HALF_MODE_RE,),
        Elements.QUAD: (BasisType.FOURIER_HALF_MODE_RE, BasisType.FOURIER_HALF_MODE_RE),
        Elements.HEX: (BasisType.FOURIER_HALF_MODE_RE, BasisType.FOURIER_HALF_MODE_RE, BasisType.FOURIER_HALF_MODE_RE)
    })



class FourierHalfModeImExpansionFactory(FourierSingleModeExpansionFactory):
    BASIS_MAP: MappingProxyType[Elements,Tuple[BasisType,...]] = MappingProxyType({
        Elements.SEG: (BasisType.FOURIER_HALF_MODE_IM,),
        Elements.QUAD: (BasisType.FOURIER_HALF_MODE_IM, BasisType.FOURIER_HALF_MODE_IM),
        Elements.HEX: (BasisType.FOURIER_HALF_MODE_IM, BasisType.FOURIER_HALF_MODE_IM, BasisType.FOURIER_HALF_MODE_IM)
    })

class ChebyshevExpansionFactory(ExpansionFactory):
    BASIS_MAP: MappingProxyType[Elements,Tuple[BasisType,...]] = MappingProxyType({
        Elements.SEG: (BasisType.CHEBYSHEV,),
        Elements.QUAD: (BasisType.CHEBYSHEV, BasisType.CHEBYSHEV),
        Elements.HEX: (BasisType.CHEBYSHEV, BasisType.CHEBYSHEV, BasisType.CHEBYSHEV)
    })

    INTEGRATION_POINTS_MAP: MappingProxyType[Elements,Tuple[IntegrationPoint]] = MappingProxyType({
        Elements.SEG: (IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV,),
        Elements.QUAD: (IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV, IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV),
        Elements.HEX: (IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV, IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV, IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV)
    })

    NUM_MODES_MAP: MappingProxyType[Elements,Callable[[int],Tuple[int,...]]] = MappingProxyType({
            Elements.SEG: lambda nummodes: (nummodes,),
            Elements.QUAD: lambda nummodes: (nummodes, nummodes),
            Elements.HEX: lambda nummodes: (nummodes, nummodes, nummodes),
        })

    NUM_POINTS_MAP: MappingProxyType[Elements,Callable[[int],Tuple[int,...]]] = MappingProxyType({
        Elements.SEG: lambda nummodes: (nummodes,),
        Elements.QUAD: lambda nummodes: (nummodes,nummodes),
        Elements.HEX: lambda nummodes: (nummodes, nummodes, nummodes),
    })

class FourierChebyshevExpansionFactory(ExpansionFactory):
    BASIS_MAP: MappingProxyType[Elements,Tuple[BasisType,...]] = MappingProxyType({
        Elements.QUAD: (BasisType.FOURIER, BasisType.CHEBYSHEV),
    })

    INTEGRATION_POINTS_MAP: MappingProxyType[Elements,Tuple[IntegrationPoint]] = MappingProxyType({
        Elements.QUAD: (IntegrationPoint.FOURIER_EVENLY_SPACED, IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV),
    })

    NUM_MODES_MAP: MappingProxyType[Elements,Callable[[int],Tuple[int,...]]] = MappingProxyType({
            Elements.QUAD: lambda nummodes: (nummodes, nummodes),
        })

    NUM_POINTS_MAP: MappingProxyType[Elements,Callable[[int],Tuple[int,...]]] = MappingProxyType({
        Elements.QUAD: lambda nummodes: (nummodes,nummodes),
    })

class ChebyshevFourierExpansionFactory(FourierChebyshevExpansionFactory):
    BASIS_MAP: MappingProxyType[Elements,Tuple[BasisType,...]] = MappingProxyType({
        Elements.QUAD: (BasisType.CHEBYSHEV, BasisType.FOURIER),
    })

    INTEGRATION_POINTS_MAP: MappingProxyType[Elements,Tuple[IntegrationPoint]] = MappingProxyType({
        Elements.QUAD: (IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV, IntegrationPoint.FOURIER_EVENLY_SPACED),
    })

class ModifiedFourierExpansionFactory(ExpansionFactory):
    BASIS_MAP: MappingProxyType[Elements,Tuple[BasisType,...]] = MappingProxyType({
        Elements.QUAD: (BasisType.FOURIER, BasisType.MODIFIED_A),
    })

    INTEGRATION_POINTS_MAP: MappingProxyType[Elements,Tuple[IntegrationPoint]] = MappingProxyType({
        Elements.QUAD: (IntegrationPoint.FOURIER_EVENLY_SPACED, IntegrationPoint.GAUSS_LOBATTO_LEGENDRE),
    })

    NUM_MODES_MAP: MappingProxyType[Elements,Callable[[int],Tuple[int,...]]] = MappingProxyType({
            Elements.QUAD: lambda nummodes: (nummodes, nummodes),
        })

    NUM_POINTS_MAP: MappingProxyType[Elements,Callable[[int],Tuple[int,...]]] = MappingProxyType({
        Elements.QUAD: lambda nummodes: (nummodes,nummodes+1),
    })