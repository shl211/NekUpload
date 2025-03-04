from NekUpload.NekData.data_type import Elements,BasisType,IntegrationPoint
import NekUpload.NekData.expansions as nd
import pytest
from typing import Dict

#######################################################################
# Expansion Definition functionality
#

def test_get_uniorder_coefficients():
    expansion_factory = nd.ModifiedExpansionFactory()

    num_modes = 5
    element_coeffs: Dict[Elements,int] = {Elements.SEG: 5,
                                    Elements.QUAD: 25,
                                    Elements.TRI: 10,
                                    Elements.HEX: 125,
                                    Elements.PRISM: 50,
                                    Elements.TET: 35,
                                    Elements.PYR: 55,
                                }

    for elmt,expected_coeff in element_coeffs.items():
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(elmt,num_modes)
        assert expansion.get_num_coefficients() == expected_coeff

def test_get_polyorder_coefficients_2d():
    expansion = nd.ExpansionDefinition(Elements.QUAD,
                                    (BasisType.MODIFIED_A,BasisType.MODIFIED_A),
                                    (5,6),
                                    (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE),
                                    (6,6))
    
    expected_coeff = 30
    assert expansion.get_num_coefficients() == expected_coeff

    expansion = nd.ExpansionDefinition(Elements.TRI,
                                    (BasisType.MODIFIED_A,BasisType.MODIFIED_B),
                                    (5,6),
                                    (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE),
                                    (6,6))
    
    expected_coeff = 15
    assert expansion.get_num_coefficients() == expected_coeff

def test_get_polyorder_coefficients_3d():
    expansion = nd.ExpansionDefinition(Elements.HEX,
                                    (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_A),
                                    (5,6,7),
                                    (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE),
                                    (6,6,6))
    
    expected_coeff = 210
    assert expansion.get_num_coefficients() == expected_coeff

    expansion = nd.ExpansionDefinition(Elements.TET,
                                    (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_A),
                                    (5,6,7),
                                    (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE),
                                    (6,6,6))
    
    expected_coeff = 75
    assert expansion.get_num_coefficients() == expected_coeff

    expansion = nd.ExpansionDefinition(Elements.PYR,
                                    (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_A),
                                    (5,6,7),
                                    (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE),
                                    (6,6,6))
    
    expected_coeff = 115
    assert expansion.get_num_coefficients() == expected_coeff

    expansion = nd.ExpansionDefinition(Elements.PRISM,
                                    (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_A),
                                    (5,6,7),
                                    (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE),
                                    (6,6,6))
    
    expected_coeff = 120
    assert expansion.get_num_coefficients() == expected_coeff

########################################################################
# Modified Expansion Factory
#
def test_modified_expansion_seg():
    expansion_factory = nd.ModifiedExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.SEG,num_modes)

    expected_modes = (5,)
    expected_points = (6,)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_modified_expansion_tri():
    expansion_factory = nd.ModifiedExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TRI,num_modes)

    expected_modes = (5,5)
    expected_points = (6,5)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_B)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_expansion_quad():
    expansion_factory = nd.ModifiedExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.QUAD,num_modes)

    expected_modes = (5,5)
    expected_points = (6,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_expansion_hex():
    expansion_factory = nd.ModifiedExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.HEX,num_modes)

    expected_modes = (5,5,5)
    expected_points = (6,6,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_A)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_expansion_tet():
    expansion_factory = nd.ModifiedExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TET,num_modes)

    expected_modes = (5,5,5)
    expected_points = (6,5,5)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0,IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_B,BasisType.MODIFIED_C)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_expansion_pyr():
    expansion_factory = nd.ModifiedExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PYR,num_modes)

    expected_modes = (5,5,5)
    expected_points = (6,6,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_PYR_C)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_expansion_prism():
    expansion_factory = nd.ModifiedExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PRISM,num_modes)

    expected_modes = (5,5,5)
    expected_points = (6,6,5)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_B)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

########################################################################
# Modified Quad Plus One Expansion Factory
#
def test_modified_plus_1_expansion_seg():
    expansion_factory = nd.ModifiedQuadPlus1ExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.SEG,num_modes)

    expected_modes = (5,)
    expected_points = (7,)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_modified_plus_1_expansion_tri():
    expansion_factory = nd.ModifiedQuadPlus1ExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TRI,num_modes)

    expected_modes = (5,5)
    expected_points = (7,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_B)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_plus_1_expansion_quad():
    expansion_factory = nd.ModifiedQuadPlus1ExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.QUAD,num_modes)

    expected_modes = (5,5)
    expected_points = (7,7)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_plus_1_expansion_hex():
    expansion_factory = nd.ModifiedQuadPlus1ExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.HEX,num_modes)

    expected_modes = (5,5,5)
    expected_points = (7,7,7)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_A)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_plus_1_expansion_tet():
    expansion_factory = nd.ModifiedQuadPlus1ExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TET,num_modes)

    expected_modes = (5,5,5)
    expected_points = (7,6,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0,IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_B,BasisType.MODIFIED_C)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_plus_1_expansion_pyr():
    expansion_factory = nd.ModifiedQuadPlus1ExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PYR,num_modes)

    expected_modes = (5,5,5)
    expected_points = (7,7,7)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_PYR_C)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_plus_1_expansion_prism():
    expansion_factory = nd.ModifiedQuadPlus1ExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PRISM,num_modes)

    expected_modes = (5,5,5)
    expected_points = (7,7,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_B)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

########################################################################
# Modified Quad Plus Two Expansion Factory
#
def test_modified_plus_2_expansion_seg():
    expansion_factory = nd.ModifiedQuadPlus2ExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.SEG,num_modes)

    expected_modes = (5,)
    expected_points = (8,)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_modified_plus_2_expansion_tri():
    expansion_factory = nd.ModifiedQuadPlus2ExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TRI,num_modes)

    expected_modes = (5,5)
    expected_points = (8,7)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_B)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_plus_2_expansion_quad():
    expansion_factory = nd.ModifiedQuadPlus2ExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.QUAD,num_modes)

    expected_modes = (5,5)
    expected_points = (8,8)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_plus_2_expansion_hex():
    expansion_factory = nd.ModifiedQuadPlus2ExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.HEX,num_modes)

    expected_modes = (5,5,5)
    expected_points = (8,8,8)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_A)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_plus_2_expansion_tet():
    expansion_factory = nd.ModifiedQuadPlus2ExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TET,num_modes)

    expected_modes = (5,5,5)
    expected_points = (8,7,7)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0,IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_B,BasisType.MODIFIED_C)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_plus_2_expansion_pyr():
    expansion_factory = nd.ModifiedQuadPlus2ExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PYR,num_modes)

    expected_modes = (5,5,5)
    expected_points = (8,8,8)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_PYR_C)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_plus_2_expansion_prism():
    expansion_factory = nd.ModifiedQuadPlus2ExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PRISM,num_modes)

    expected_modes = (5,5,5)
    expected_points = (8,8,7)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_B)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

########################################################################
# Modified GLL Expansion Factory
#
def test_modified_GLL_radau_expansion_seg():
    expansion_factory = nd.ModifiedGLLRadau10ExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.SEG,num_modes)

    expected_modes = (5,)
    expected_points = (6,)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_modified_GLL_radau_expansion_tri():
    expansion_factory = nd.ModifiedGLLRadau10ExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TRI,num_modes)

    expected_modes = (5,5)
    expected_points = (6,5)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_B)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_GLL_radau_expansion_quad():
    expansion_factory = nd.ModifiedGLLRadau10ExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.QUAD,num_modes)

    expected_modes = (5,5)
    expected_points = (6,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_GLL_radau_expansion_hex():
    expansion_factory = nd.ModifiedGLLRadau10ExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.HEX,num_modes)

    expected_modes = (5,5,5)
    expected_points = (6,6,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_A)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_GLL_radau_expansion_tet():
    expansion_factory = nd.ModifiedGLLRadau10ExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TET,num_modes)

    expected_modes = (5,5,5)
    expected_points = (6,5,5)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_B,BasisType.MODIFIED_C)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_GLL_radau_expansion_pyr():
    expansion_factory = nd.ModifiedGLLRadau10ExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PYR,num_modes)

    expected_modes = (5,5,5)
    expected_points = (6,6,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_PYR_C)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_GLL_radau_expansion_prism():
    expansion_factory = nd.ModifiedGLLRadau10ExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PRISM,num_modes)

    expected_modes = (5,5,5)
    expected_points = (6,6,5)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_B)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

########################################################################
# GLL Lagrange Expansion Factory
#
def test_GLL_lagrange_expansion_seg():
    expansion_factory = nd.GLLLagranageExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.SEG,num_modes)

    expected_modes = (5,)
    expected_points = (6,)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,)
    expected_field = ("")
    expected_basis = (BasisType.GLL_LAGRANGE,)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_GLL_lagrange_expansion_tri():
    expansion_factory = nd.GLLLagranageExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TRI,num_modes)

    expected_modes = (5,5)
    expected_points = (6,5)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.GLL_LAGRANGE,BasisType.ORTHO_B)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_GLL_lagrange_expansion_quad():
    expansion_factory = nd.GLLLagranageExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.QUAD,num_modes)

    expected_modes = (5,5)
    expected_points = (6,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.GLL_LAGRANGE,BasisType.GLL_LAGRANGE)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_GLL_lagrange_expansion_hex():
    expansion_factory = nd.GLLLagranageExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.HEX,num_modes)

    expected_modes = (5,5,5)
    expected_points = (6,6,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.GLL_LAGRANGE,BasisType.GLL_LAGRANGE,BasisType.GLL_LAGRANGE)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_GLL_lagrange_expansion_tet():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.GLLLagranageExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TET,num_modes)

        msg = "TET should not have a GLL Lagrange Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_GLL_lagrange_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.GLLLagranageExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PYR,num_modes)

        msg = "PYR should not have a GLL Lagrange Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_GLL_lagrange_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.GLLLagranageExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PRISM,num_modes)

        msg = "PRISM should not have a GLL Lagrange Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

########################################################################
# Gauss Lagrange Expansion Factory
#
def test_gauss_lagrange_expansion_seg():
    expansion_factory = nd.GaussLagrangeExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.SEG,num_modes)

    expected_modes = (5,)
    expected_points = (5,)
    expected_integr_type = (IntegrationPoint.GAUSS_GAUSS_LEGENDRE,)
    expected_field = ("")
    expected_basis = (BasisType.GAUSS_LAGRANGE,)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_gauss_lagrange_expansion_tri():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.GaussLagrangeExpansionFactory()
        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TRI,num_modes)
        msg = "TRI should not have a Gauss Lagrange Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_gauss_lagrange_expansion_quad():
    expansion_factory = nd.GaussLagrangeExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.QUAD,num_modes)

    expected_modes = (5,5)
    expected_points = (5,5)
    expected_integr_type = (IntegrationPoint.GAUSS_GAUSS_LEGENDRE,IntegrationPoint.GAUSS_GAUSS_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.GAUSS_LAGRANGE,BasisType.GAUSS_LAGRANGE)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_gauss_lagrange_expansion_hex():
    expansion_factory = nd.GaussLagrangeExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.HEX,num_modes)

    expected_modes = (5,5,5)
    expected_points = (5,5,5)
    expected_integr_type = (IntegrationPoint.GAUSS_GAUSS_LEGENDRE,IntegrationPoint.GAUSS_GAUSS_LEGENDRE,IntegrationPoint.GAUSS_GAUSS_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.GAUSS_LAGRANGE,BasisType.GAUSS_LAGRANGE,BasisType.GAUSS_LAGRANGE)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_gauss_lagrange_expansion_tet():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.GaussLagrangeExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TET,num_modes)

        msg = "TET should not have a Gauss Lagrange Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_gauss_lagrange_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.GaussLagrangeExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PYR,num_modes)

        msg = "PYR should not have a Gauss Lagrange Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_gauss_lagrange_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.GaussLagrangeExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PRISM,num_modes)

        msg = "PRISM should not have a Gauss Lagrange Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

########################################################################
# Orthogonal Expansion Factory
#
def test_orthogonal_expansion_seg():
    expansion_factory = nd.OrthogonalExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.SEG,num_modes)

    expected_modes = (5,)
    expected_points = (6,)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,)
    expected_field = ("")
    expected_basis = (BasisType.ORTHO_A,)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_orthogonal_expansion_tri():
    expansion_factory = nd.OrthogonalExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TRI,num_modes)

    expected_modes = (5,5)
    expected_points = (6,5)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.ORTHO_A,BasisType.ORTHO_B)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_orthogonal_expansion_quad():
    expansion_factory = nd.OrthogonalExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.QUAD,num_modes)

    expected_modes = (5,5)
    expected_points = (6,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.ORTHO_A,BasisType.ORTHO_A)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_orthogonal_expansion_hex():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.OrthogonalExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.HEX,num_modes)
        msg = "HEX should not have a Orthogonal Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_orthogonal_expansion_tet():
    expansion_factory = nd.OrthogonalExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TET,num_modes)

    expected_modes = (5,5,5)
    expected_points = (6,5,5)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0,IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.ORTHO_A,BasisType.ORTHO_B,BasisType.ORTHO_C)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_orthogonal_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.OrthogonalExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PYR,num_modes)

        msg = "PYR should not have a Orthogonal Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_orthogonal_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.OrthogonalExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PRISM,num_modes)

        msg = "PRISM should not have a Orthogonal Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

########################################################################
# GLL Lagrange SEM Expansion Factory
#
def test_GLL_lagrange_SEM_expansion_seg():
    expansion_Factory = nd.GLLLagrangeSEMExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_Factory.get_expansion(Elements.SEG,num_modes)

    expected_modes = (5,)
    expected_points = (5,)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,)
    expected_field = ("")
    expected_basis = (BasisType.GLL_LAGRANGE,)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_GLL_lagrange_SEM_expansion_tri():
    #no definition for this, expect correct rejection
    try:
        expansion_Factory = nd.GLLLagrangeSEMExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_Factory.get_expansion(Elements.TRI,num_modes)
        msg = "TRI should not have a GLL Lagrange SEM Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_GLL_lagrange_SEM_expansion_quad():
    expansion_Factory = nd.GLLLagrangeSEMExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_Factory.get_expansion(Elements.QUAD,num_modes)

    expected_modes = (5,5)
    expected_points = (5,5)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.GLL_LAGRANGE,BasisType.GLL_LAGRANGE)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_GLL_lagrange_SEM_expansion_hex():
    expansion_Factory = nd.GLLLagrangeSEMExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_Factory.get_expansion(Elements.HEX,num_modes)

    expected_modes = (5,5,5)
    expected_points = (5,5,5)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.GLL_LAGRANGE,BasisType.GLL_LAGRANGE,BasisType.GLL_LAGRANGE)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_GLL_lagrange_SEM_expansion_tet():
    #no definition for this, expect correct rejection
    try:
        expansion_Factory = nd.GLLLagrangeSEMExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_Factory.get_expansion(Elements.TET,num_modes)

        msg = "TET should not have a GLL Lagrange SEM Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_GLL_lagrange_SEM_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_Factory = nd.GLLLagrangeSEMExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_Factory.get_expansion(Elements.PYR,num_modes)
        
        msg = "PYR should not have a GLL Lagrange SEM Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_GLL_lagrange_SEM_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_Factory = nd.GLLLagrangeSEMExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_Factory.get_expansion(Elements.PRISM,num_modes)

        msg = "PRISM should not have a GLL Lagrange SEM Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

########################################################################
# Fourier Expansion Factory
#
def test_fourier_expansion_seg():
    expansion_factory = nd.FourierExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.SEG,num_modes)

    expected_modes = (5,)
    expected_points = (5,)
    expected_integr_type = (IntegrationPoint.FOURIER_EVENLY_SPACED,)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER,)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_fourier_expansion_tri():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.FourierExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TRI,num_modes)

        msg = "TRI should not have a Fourier Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_fourier_expansion_quad():
    expansion_factory = nd.FourierExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.QUAD,num_modes)

    expected_modes = (5,5)
    expected_points = (5,5)
    expected_integr_type = (IntegrationPoint.FOURIER_EVENLY_SPACED,IntegrationPoint.FOURIER_EVENLY_SPACED)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER,BasisType.FOURIER)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_fourier_expansion_hex():
    expansion_factory = nd.FourierExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.HEX,num_modes)

    expected_modes = (5,5,5)
    expected_points = (5,5,5)
    expected_integr_type = (IntegrationPoint.FOURIER_EVENLY_SPACED,IntegrationPoint.FOURIER_EVENLY_SPACED,IntegrationPoint.FOURIER_EVENLY_SPACED)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER,BasisType.FOURIER,BasisType.FOURIER)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_fourier_expansion_tet():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.FourierExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TET,num_modes)

        msg = "TET should not have a Fourier Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_fourier_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.FourierExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PYR,num_modes)

        msg = "PYR should not have a Fourier Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_fourier_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.FourierExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PRISM,num_modes)

        msg = "PRISM should not have a Fourier Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

########################################################################
# Fourier Single Mode Factory
#
def test_fourier_single_mode_expansion_seg():
    expansion_factory = nd.FourierSingleModeExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.SEG,num_modes)

    expected_modes = (5,)
    expected_points = (5,)
    expected_integr_type = (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER_SINGLE_MODE,)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_fourier_single_mode_expansion_tri():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.FourierSingleModeExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TRI,num_modes)

        msg = "TRI should not have a Fourier Single Mode Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_fourier_single_mode_expansion_quad():
    expansion_factory = nd.FourierSingleModeExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.QUAD,num_modes)

    expected_modes = (5,5)
    expected_points = (5,5)
    expected_integr_type = (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,IntegrationPoint.FOURIER_SINGLE_MODE_SPACED)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER_SINGLE_MODE,BasisType.FOURIER_SINGLE_MODE)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_fourier_single_mode_expansion_hex():
    expansion_factory = nd.FourierSingleModeExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.HEX,num_modes)

    expected_modes = (5,5,5)
    expected_points = (5,5,5)
    expected_integr_type = (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,IntegrationPoint.FOURIER_SINGLE_MODE_SPACED)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER_SINGLE_MODE,BasisType.FOURIER_SINGLE_MODE,BasisType.FOURIER_SINGLE_MODE)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_fourier_single_mode_expansion_tet():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.FourierSingleModeExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TET,num_modes)

        msg = "TET should not have a Fourier Single Mode Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_fourier_single_mode_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.FourierSingleModeExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PYR,num_modes)

        msg = "PYR should not have a Fourier Single Mode Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_fourier_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.FourierSingleModeExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PRISM,num_modes)

        msg = "PRISM should not have a Fourier Single Mode Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

########################################################################
# Fourier Half Mode Re Factory
#
def test_fourier_half_mode_re_expansion_seg():
    expansion_factory = nd.FourierHalfModeReExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.SEG,num_modes)

    expected_modes = (5,)
    expected_points = (5,)
    expected_integr_type = (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER_HALF_MODE_RE,)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_fourier_half_mode_re_expansion_tri():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.FourierHalfModeReExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TRI,num_modes)

        msg = "TRI should not have a Fourier Half Mode Real Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_fourier_half_mode_re_expansion_quad():
    expansion_factory = nd.FourierHalfModeReExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.QUAD,num_modes)

    expected_modes = (5,5)
    expected_points = (5,5)
    expected_integr_type = (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,IntegrationPoint.FOURIER_SINGLE_MODE_SPACED)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER_HALF_MODE_RE,BasisType.FOURIER_HALF_MODE_RE)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_fourier_half_mode_re_expansion_hex():
    expansion_factory = nd.FourierHalfModeReExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.HEX,num_modes)

    expected_modes = (5,5,5)
    expected_points = (5,5,5)
    expected_integr_type = (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,IntegrationPoint.FOURIER_SINGLE_MODE_SPACED)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER_HALF_MODE_RE,BasisType.FOURIER_HALF_MODE_RE,BasisType.FOURIER_HALF_MODE_RE)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_fourier_half_mode_re_expansion_tet():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.FourierHalfModeReExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TET,num_modes)

        msg = "TET should not have a Fourier Half Mode Real Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_fourier_half_mode_re_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.FourierHalfModeReExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PYR,num_modes)

        msg = "PYR should not have a Fourier Half Mode Real Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_fourier_half_mode_re_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.FourierHalfModeReExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PRISM,num_modes)

        msg = "PRISM should not have a Fourier Half Mode Real Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

########################################################################
# Fourier Half Mode Im Factory
#
def test_fourier_half_mode_im_expansion_seg():
    expansion_factory = nd.FourierHalfModeImExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.SEG,num_modes)

    expected_modes = (5,)
    expected_points = (5,)
    expected_integr_type = (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER_HALF_MODE_IM,)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_fourier_half_mode_im_expansion_tri():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.FourierHalfModeImExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TRI,num_modes)

        msg = "TRI should not have a Fourier Half Mode Imaginary Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_fourier_half_mode_im_expansion_quad():
    expansion_factory = nd.FourierHalfModeImExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.QUAD,num_modes)

    expected_modes = (5,5)
    expected_points = (5,5)
    expected_integr_type = (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,IntegrationPoint.FOURIER_SINGLE_MODE_SPACED)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER_HALF_MODE_IM,BasisType.FOURIER_HALF_MODE_IM)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_fourier_half_mode_im_expansion_hex():
    expansion_factory = nd.FourierHalfModeImExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.HEX,num_modes)

    expected_modes = (5,5,5)
    expected_points = (5,5,5)
    expected_integr_type = (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,IntegrationPoint.FOURIER_SINGLE_MODE_SPACED)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER_HALF_MODE_IM,BasisType.FOURIER_HALF_MODE_IM,BasisType.FOURIER_HALF_MODE_IM)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_fourier_half_mode_im_expansion_tet():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.FourierHalfModeImExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TET,num_modes)
        msg = "TET should not have a Fourier Half Mode Imaginary Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_fourier_half_mode_im_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.FourierHalfModeImExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PYR,num_modes)
        msg = "PYR should not have a Fourier Half Mode Imaginary Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_fourier_half_mode_im_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.FourierHalfModeImExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PRISM,num_modes)
        msg = "PRISM should not have a Fourier Half Mode Imaginary Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

########################################################################
# Chebyshev Factory
#
def test_chebyshev_expansion_seg():
    expansion_factory = nd.ChebyshevExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.SEG,num_modes)

    expected_modes = (5,)
    expected_points = (5,)
    expected_integr_type = (IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV,)
    expected_field = ("")
    expected_basis = (BasisType.CHEBYSHEV,)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_chebyshev_expansion_tri():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.ChebyshevExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TRI,num_modes)

        msg = "TRI should not have a Chebyshev definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_chebyshev_expansion_quad():
    expansion_factory = nd.ChebyshevExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.QUAD,num_modes)

    expected_modes = (5,5)
    expected_points = (5,5)
    expected_integr_type = (IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV,IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV)
    expected_field = ("")
    expected_basis = (BasisType.CHEBYSHEV,BasisType.CHEBYSHEV)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_chebyshev_expansion_hex():
    expansion_factory = nd.ChebyshevExpansionFactory()

    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.HEX,num_modes)

    expected_modes = (5,5,5)
    expected_points = (5,5,5)
    expected_integr_type = (IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV,IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV,IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV)
    expected_field = ("")
    expected_basis = (BasisType.CHEBYSHEV,BasisType.CHEBYSHEV,BasisType.CHEBYSHEV)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_chebyshev_expansion_tet():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.ChebyshevExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TET,num_modes)

        msg = "TET should not have a Chebyshev Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_chebyshev_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.ChebyshevExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PYR,num_modes)

        msg = "PYR should not have a Chebyshev Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_chebyshev_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.ChebyshevExpansionFactory()

        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PRISM,num_modes)

        msg = "PRISM should not have a Chebyshev Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

########################################################################
# Fourier Chebyshev Factory
#
def test_fourier_chebyshev_expansion_seg():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.FourierChebyshevExpansionFactory()
        num_modes=5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.SEG,num_modes)
        msg = "SEG should not have a Fourier Chebyshev definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass
    
def test_fourier_chebyshev_expansion_tri():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.FourierChebyshevExpansionFactory()
        num_modes=5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TRI,num_modes)
        msg = "TRI should not have a Fourier Chebyshev definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_fourier_chebyshev_expansion_quad():
    expansion_factory = nd.FourierChebyshevExpansionFactory()
    num_modes=5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.QUAD,num_modes)

    expected_modes = (5,5)
    expected_points = (5,5)
    expected_integr_type = (IntegrationPoint.FOURIER_EVENLY_SPACED,IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER,BasisType.CHEBYSHEV)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_fourier_chebyshev_expansion_hex():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.FourierChebyshevExpansionFactory()
        num_modes=5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.HEX,num_modes)
        msg = "HEX should not have a Fourier Chebyshev Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_fourier_chebyshev_expansion_tet():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.FourierChebyshevExpansionFactory()
        num_modes=5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TET,num_modes)
        msg = "TET should not have a Fourier Chebyshev Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_fourier_chebyshev_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.FourierChebyshevExpansionFactory()
        num_modes=5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PYR,num_modes)
        msg = "PYR should not have a Fourier Chebyshev Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_fourier_chebyshev_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.FourierChebyshevExpansionFactory()
        num_modes=5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PRISM,num_modes)
        msg = "PRISM should not have a Fourier Chebyshev Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

########################################################################
# Chebyshev Fourier Factory
#
def test_chebyshev_fourier_expansion_seg():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.ChebyshevFourierExpansionFactory()
        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.SEG,num_modes)
        msg = "SEG should not have a Chebyshev Fourier definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass
    
def test_chebyshev_fourier_expansion_tri():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.ChebyshevFourierExpansionFactory()
        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TRI,num_modes)
        msg = "TRI should not have a Chebyshev Fourier definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_chebyshev_fourier_expansion_quad():
    expansion_factory = nd.ChebyshevFourierExpansionFactory()
    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.QUAD,num_modes)

    expected_modes = (5,5)
    expected_points = (5,5)
    expected_integr_type = (IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV,IntegrationPoint.FOURIER_EVENLY_SPACED)
    expected_field = ("")
    expected_basis = (BasisType.CHEBYSHEV,BasisType.FOURIER)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_chebyshev_fourier_expansion_hex():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.ChebyshevFourierExpansionFactory()
        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.HEX,num_modes)
        msg = "HEX should not have a Chebyshev Fourier Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_chebyshev_fourier_expansion_tet():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.ChebyshevFourierExpansionFactory()
        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TET,num_modes)
        msg = "TET should not have a Chebyshev Fourier Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_chebyshev_fourier_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.ChebyshevFourierExpansionFactory()
        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PYR,num_modes)
        msg = "PYR should not have a Chebyshev Fourier Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_chebyshev_fourier_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.ChebyshevFourierExpansionFactory()
        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PRISM,num_modes)
        msg = "PRISM should not have a Chebyshev Fourier Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

########################################################################
# Fourier Modified Factory
#
def test_fourier_modified_expansion_seg():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.ModifiedFourierExpansionFactory()
        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.SEG,num_modes)

        msg = "SEG should not have a Fourier Modified definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass
    
def test_fourier_modified_expansion_tri():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.ModifiedFourierExpansionFactory()
        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TRI,num_modes)
        msg = "TRI should not have a Fourier Modified definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_fourier_modified_expansion_quad():
    expansion_factory = nd.ModifiedFourierExpansionFactory()
    num_modes = 5
    expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.QUAD,num_modes)

    expected_modes = (5,5)
    expected_points = (5,6)
    expected_integr_type = (IntegrationPoint.FOURIER_EVENLY_SPACED,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER,BasisType.MODIFIED_A)

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_fourier_modified_expansion_hex():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.ModifiedFourierExpansionFactory()
        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.HEX,num_modes)
        msg = "HEX should not have a Fourier Modified Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_fourier_modified_expansion_tet():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.ModifiedFourierExpansionFactory()
        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.TET,num_modes)
        msg = "TET should not have a Fourier Modified Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_fourier_modified_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.ModifiedFourierExpansionFactory()
        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PYR,num_modes)
        msg = "PYR should not have a Fourier Modified Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass

def test_fourier_modified_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_factory = nd.ModifiedFourierExpansionFactory()
        num_modes = 5
        expansion: nd.ExpansionDefinition = expansion_factory.get_expansion(Elements.PRISM,num_modes)
        msg = "PRISM should not have a Fourier Modified Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except nd.ExpansionValidationException:
        pass