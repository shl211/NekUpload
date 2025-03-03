from NekUpload.NekData.data_type import Elements,BasisType,IntegrationPoint
import NekUpload.NekData.expansions as nd
import pytest

########################################################################
# Modified Expansion Builder
#
def test_modified_expansion_seg():
    expansion_builder = nd.ModifiedExpansionBuilder(Elements.SEG)

    num_modes = 5

    expected_modes = (5,)
    expected_points = (6,)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_modified_expansion_tri():
    expansion_builder = nd.ModifiedExpansionBuilder(Elements.TRI)

    num_modes = 5

    expected_modes = (5,5)
    expected_points = (6,5)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_B)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_expansion_quad():
    expansion_builder = nd.ModifiedExpansionBuilder(Elements.QUAD)

    num_modes = 5

    expected_modes = (5,5)
    expected_points = (6,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_expansion_hex():
    expansion_builder = nd.ModifiedExpansionBuilder(Elements.HEX)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (6,6,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_A)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_expansion_tet():
    expansion_builder = nd.ModifiedExpansionBuilder(Elements.TET)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (6,5,5)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0,IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_B,BasisType.MODIFIED_C)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_expansion_pyr():
    expansion_builder = nd.ModifiedExpansionBuilder(Elements.PYR)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (6,6,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_PYR_C)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_expansion_prism():
    expansion_builder = nd.ModifiedExpansionBuilder(Elements.PRISM)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (6,6,5)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_B)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

########################################################################
# Modified Quad Plus One Expansion Builder
#
def test_modified_plus_1_expansion_seg():
    expansion_builder = nd.ModifiedQuadPlus1ExpansionBuilder(Elements.SEG)

    num_modes = 5

    expected_modes = (5,)
    expected_points = (7,)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_modified_plus_1_expansion_tri():
    expansion_builder = nd.ModifiedQuadPlus1ExpansionBuilder(Elements.TRI)

    num_modes = 5

    expected_modes = (5,5)
    expected_points = (7,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_B)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_plus_1_expansion_quad():
    expansion_builder = nd.ModifiedQuadPlus1ExpansionBuilder(Elements.QUAD)

    num_modes = 5

    expected_modes = (5,5)
    expected_points = (7,7)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_plus_1_expansion_hex():
    expansion_builder = nd.ModifiedQuadPlus1ExpansionBuilder(Elements.HEX)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (7,7,7)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_A)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_plus_1_expansion_tet():
    expansion_builder = nd.ModifiedQuadPlus1ExpansionBuilder(Elements.TET)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (7,6,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0,IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_B,BasisType.MODIFIED_C)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_plus_1_expansion_pyr():
    expansion_builder = nd.ModifiedQuadPlus1ExpansionBuilder(Elements.PYR)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (7,7,7)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_PYR_C)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_plus_1_expansion_prism():
    expansion_builder = nd.ModifiedQuadPlus1ExpansionBuilder(Elements.PRISM)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (7,7,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_B)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

########################################################################
# Modified Quad Plus Two Expansion Builder
#
def test_modified_plus_2_expansion_seg():
    expansion_builder = nd.ModifiedQuadPlus2ExpansionBuilder(Elements.SEG)

    num_modes = 5

    expected_modes = (5,)
    expected_points = (8,)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_modified_plus_2_expansion_tri():
    expansion_builder = nd.ModifiedQuadPlus2ExpansionBuilder(Elements.TRI)

    num_modes = 5

    expected_modes = (5,5)
    expected_points = (8,7)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_B)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_plus_2_expansion_quad():
    expansion_builder = nd.ModifiedQuadPlus2ExpansionBuilder(Elements.QUAD)

    num_modes = 5

    expected_modes = (5,5)
    expected_points = (8,8)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_plus_2_expansion_hex():
    expansion_builder = nd.ModifiedQuadPlus2ExpansionBuilder(Elements.HEX)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (8,8,8)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_A)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_plus_2_expansion_tet():
    expansion_builder = nd.ModifiedQuadPlus2ExpansionBuilder(Elements.TET)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (8,7,7)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0,IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_B,BasisType.MODIFIED_C)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_plus_2_expansion_pyr():
    expansion_builder = nd.ModifiedQuadPlus2ExpansionBuilder(Elements.PYR)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (8,8,8)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_PYR_C)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_plus_2_expansion_prism():
    expansion_builder = nd.ModifiedQuadPlus2ExpansionBuilder(Elements.PRISM)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (8,8,7)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_B)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

########################################################################
# Modified GLL Expansion Builder
#
def test_modified_GLL_radau_expansion_seg():
    expansion_builder = nd.ModifiedGLLRadau10ExpansionBuilder(Elements.SEG)

    num_modes = 5

    expected_modes = (5,)
    expected_points = (6,)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_modified_GLL_radau_expansion_tri():
    expansion_builder = nd.ModifiedGLLRadau10ExpansionBuilder(Elements.TRI)

    num_modes = 5

    expected_modes = (5,5)
    expected_points = (6,5)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_B)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_GLL_radau_expansion_quad():
    expansion_builder = nd.ModifiedGLLRadau10ExpansionBuilder(Elements.QUAD)

    num_modes = 5

    expected_modes = (5,5)
    expected_points = (6,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_GLL_radau_expansion_hex():
    expansion_builder = nd.ModifiedGLLRadau10ExpansionBuilder(Elements.HEX)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (6,6,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_A)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_GLL_radau_expansion_tet():
    expansion_builder = nd.ModifiedGLLRadau10ExpansionBuilder(Elements.TET)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (6,5,5)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_B,BasisType.MODIFIED_C)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_GLL_radau_expansion_pyr():
    expansion_builder = nd.ModifiedGLLRadau10ExpansionBuilder(Elements.PYR)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (6,6,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_PYR_C)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_modified_GLL_radau_expansion_prism():
    expansion_builder = nd.ModifiedGLLRadau10ExpansionBuilder(Elements.PRISM)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (6,6,5)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.MODIFIED_A,BasisType.MODIFIED_A,BasisType.MODIFIED_B)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

########################################################################
# GLL Lagrange Expansion Builder
#
def test_GLL_lagrange_expansion_seg():
    expansion_builder = nd.GLLLagranageExpansionBuilder(Elements.SEG)

    num_modes = 5

    expected_modes = (5,)
    expected_points = (6,)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,)
    expected_field = ("")
    expected_basis = (BasisType.GLL_LAGRANGE,)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_GLL_lagrange_expansion_tri():
    expansion_builder = nd.GLLLagranageExpansionBuilder(Elements.TRI)

    num_modes = 5

    expected_modes = (5,5)
    expected_points = (6,5)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.GLL_LAGRANGE,BasisType.ORTHO_B)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_GLL_lagrange_expansion_quad():
    expansion_builder = nd.GLLLagranageExpansionBuilder(Elements.QUAD)

    num_modes = 5

    expected_modes = (5,5)
    expected_points = (6,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.GLL_LAGRANGE,BasisType.GLL_LAGRANGE)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_GLL_lagrange_expansion_hex():
    expansion_builder = nd.GLLLagranageExpansionBuilder(Elements.HEX)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (6,6,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.GLL_LAGRANGE,BasisType.GLL_LAGRANGE,BasisType.GLL_LAGRANGE)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_GLL_lagrange_expansion_tet():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.GLLLagranageExpansionBuilder(Elements.TET)
        msg = "TET should not have a GLL Lagrange Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_GLL_lagrange_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.GLLLagranageExpansionBuilder(Elements.PYR)
        msg = "PYR should not have a GLL Lagrange Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_GLL_lagrange_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.GLLLagranageExpansionBuilder(Elements.PRISM)
        msg = "PRISM should not have a GLL Lagrange Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

########################################################################
# Gauss Lagrange Expansion Builder
#
def test_gauss_lagrange_expansion_seg():
    expansion_builder = nd.GaussLagrangeExpansionBuilder(Elements.SEG)

    num_modes = 5

    expected_modes = (5,)
    expected_points = (5,)
    expected_integr_type = (IntegrationPoint.GAUSS_GAUSS_LEGENDRE,)
    expected_field = ("")
    expected_basis = (BasisType.GAUSS_LAGRANGE,)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_gauss_lagrange_expansion_tri():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.GaussLagrangeExpansionBuilder(Elements.TRI)
        msg = "TRI should not have a Gauss Lagrange Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_gauss_lagrange_expansion_quad():
    expansion_builder = nd.GaussLagrangeExpansionBuilder(Elements.QUAD)

    num_modes = 5

    expected_modes = (5,5)
    expected_points = (5,5)
    expected_integr_type = (IntegrationPoint.GAUSS_GAUSS_LEGENDRE,IntegrationPoint.GAUSS_GAUSS_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.GAUSS_LAGRANGE,BasisType.GAUSS_LAGRANGE)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_gauss_lagrange_expansion_hex():
    expansion_builder = nd.GaussLagrangeExpansionBuilder(Elements.HEX)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (5,5,5)
    expected_integr_type = (IntegrationPoint.GAUSS_GAUSS_LEGENDRE,IntegrationPoint.GAUSS_GAUSS_LEGENDRE,IntegrationPoint.GAUSS_GAUSS_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.GAUSS_LAGRANGE,BasisType.GAUSS_LAGRANGE,BasisType.GAUSS_LAGRANGE)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_gauss_lagrange_expansion_tet():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.GaussLagrangeExpansionBuilder(Elements.TET)
        msg = "TET should not have a Gauss Lagrange Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_gauss_lagrange_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.GaussLagrangeExpansionBuilder(Elements.PYR)
        msg = "PYR should not have a Gauss Lagrange Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_gauss_lagrange_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.GaussLagrangeExpansionBuilder(Elements.PRISM)
        msg = "PRISM should not have a Gauss Lagrange Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

########################################################################
# Orthogonal Expansion Builder
#
def test_orthogonal_expansion_seg():
    expansion_builder = nd.OrthogonalExpansionBuilder(Elements.SEG)

    num_modes = 5

    expected_modes = (5,)
    expected_points = (6,)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,)
    expected_field = ("")
    expected_basis = (BasisType.ORTHO_A,)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_orthogonal_expansion_tri():
    expansion_builder = nd.OrthogonalExpansionBuilder(Elements.TRI)

    num_modes = 5

    expected_modes = (5,5)
    expected_points = (6,5)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.ORTHO_A,BasisType.ORTHO_B)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_orthogonal_expansion_quad():
    expansion_builder = nd.OrthogonalExpansionBuilder(Elements.QUAD)

    num_modes = 5

    expected_modes = (5,5)
    expected_points = (6,6)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.ORTHO_A,BasisType.ORTHO_A)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_orthogonal_expansion_hex():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.OrthogonalExpansionBuilder(Elements.HEX)
        msg = "HEX should not have a Orthogonal Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass


def test_orthogonal_expansion_tet():
    expansion_builder = nd.OrthogonalExpansionBuilder(Elements.TET)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (6,5,5)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_RADAU_M_ALPHA1_BETA0,IntegrationPoint.GAUSS_RADAU_M_ALPHA2_BETA0)
    expected_field = ("")
    expected_basis = (BasisType.ORTHO_A,BasisType.ORTHO_B,BasisType.ORTHO_C)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_gauss_lagrange_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.OrthogonalExpansionBuilder(Elements.PYR)
        msg = "PYR should not have a Orthogonal Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_gauss_lagrange_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.GaussLagrangeExpansionBuilder(Elements.PRISM)
        msg = "PRISM should not have a Orthogonal Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

########################################################################
# GLL Lagrange SEM Expansion Builder
#
def test_GLL_lagrange_SEM_expansion_seg():
    expansion_builder = nd.GLLLagrangeSEMExpansionBuilder(Elements.SEG)

    num_modes = 5

    expected_modes = (5,)
    expected_points = (5,)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,)
    expected_field = ("")
    expected_basis = (BasisType.GLL_LAGRANGE,)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_GLL_lagrange_SEM_expansion_tri():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.GLLLagrangeSEMExpansionBuilder(Elements.TRI)
        msg = "TRI should not have a GLL Lagrange SEM Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_GLL_lagrange_SEM_expansion_quad():
    expansion_builder = nd.GLLLagrangeSEMExpansionBuilder(Elements.QUAD)

    num_modes = 5

    expected_modes = (5,5)
    expected_points = (5,5)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.GLL_LAGRANGE,BasisType.GLL_LAGRANGE)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_GLL_lagrange_SEM_expansion_hex():
    expansion_builder = nd.GLLLagrangeSEMExpansionBuilder(Elements.HEX)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (5,5,5)
    expected_integr_type = (IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.GLL_LAGRANGE,BasisType.GLL_LAGRANGE,BasisType.GLL_LAGRANGE)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_GLL_lagrange_SEM_expansion_tet():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.GLLLagrangeSEMExpansionBuilder(Elements.TET)
        msg = "TET should not have a GLL Lagrange SEM Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_GLL_lagrange_SEM_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.GLLLagrangeSEMExpansionBuilder(Elements.PYR)
        msg = "PYR should not have a GLL Lagrange SEM Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_GLL_lagrange_SEM_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.GLLLagrangeSEMExpansionBuilder(Elements.PRISM)
        msg = "PRISM should not have a GLL Lagrange SEM Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

########################################################################
# Fourier Expansion Builder
#
def test_fourier_expansion_seg():
    expansion_builder = nd.FourierExpansionBuilder(Elements.SEG)

    num_modes = 5

    expected_modes = (5,)
    expected_points = (5,)
    expected_integr_type = (IntegrationPoint.FOURIER_EVENLY_SPACED,)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER,)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_fourier_expansion_tri():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.FourierExpansionBuilder(Elements.TRI)
        msg = "TRI should not have a Fourier Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_fourier_expansion_quad():
    expansion_builder = nd.FourierExpansionBuilder(Elements.QUAD)

    num_modes = 5

    expected_modes = (5,5)
    expected_points = (5,5)
    expected_integr_type = (IntegrationPoint.FOURIER_EVENLY_SPACED,IntegrationPoint.FOURIER_EVENLY_SPACED)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER,BasisType.FOURIER)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_fourier_expansion_hex():
    expansion_builder = nd.FourierExpansionBuilder(Elements.HEX)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (5,5,5)
    expected_integr_type = (IntegrationPoint.FOURIER_EVENLY_SPACED,IntegrationPoint.FOURIER_EVENLY_SPACED,IntegrationPoint.FOURIER_EVENLY_SPACED)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER,BasisType.FOURIER,BasisType.FOURIER)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_fourier_expansion_tet():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.FourierExpansionBuilder(Elements.TET)
        msg = "TET should not have a Fourier Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_fourier_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.FourierExpansionBuilder(Elements.PYR)
        msg = "PYR should not have a Fourier Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_fourier_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.FourierExpansionBuilder(Elements.PRISM)
        msg = "PRISM should not have a Fourier Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

########################################################################
# Fourier Single Mode Builder
#
def test_fourier_single_mode_expansion_seg():
    expansion_builder = nd.FourierSingleModeExpansionBuilder(Elements.SEG)

    num_modes = 5

    expected_modes = (5,)
    expected_points = (5,)
    expected_integr_type = (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER_SINGLE_MODE,)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_fourier_single_mode_expansion_tri():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.FourierSingleModeExpansionBuilder(Elements.TRI)
        msg = "TRI should not have a Fourier Single Mode Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_fourier_single_mode_expansion_quad():
    expansion_builder = nd.FourierSingleModeExpansionBuilder(Elements.QUAD)

    num_modes = 5

    expected_modes = (5,5)
    expected_points = (5,5)
    expected_integr_type = (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,IntegrationPoint.FOURIER_SINGLE_MODE_SPACED)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER_SINGLE_MODE,BasisType.FOURIER_SINGLE_MODE)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_fourier_single_mode_expansion_hex():
    expansion_builder = nd.FourierSingleModeExpansionBuilder(Elements.HEX)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (5,5,5)
    expected_integr_type = (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,IntegrationPoint.FOURIER_SINGLE_MODE_SPACED)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER_SINGLE_MODE,BasisType.FOURIER_SINGLE_MODE,BasisType.FOURIER_SINGLE_MODE)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_fourier_single_mode_expansion_tet():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.FourierSingleModeExpansionBuilder(Elements.TET)
        msg = "TET should not have a Fourier Single Mode Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_fourier_single_mode_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.FourierSingleModeExpansionBuilder(Elements.PYR)
        msg = "PYR should not have a Fourier Single Mode Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_fourier_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.FourierSingleModeExpansionBuilder(Elements.PRISM)
        msg = "PRISM should not have a Fourier Single Mode Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

########################################################################
# Fourier Half Mode Re Builder
#
def test_fourier_half_mode_re_expansion_seg():
    expansion_builder = nd.FourierHalfModeReExpansionBuilder(Elements.SEG)

    num_modes = 5

    expected_modes = (5,)
    expected_points = (5,)
    expected_integr_type = (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER_HALF_MODE_RE,)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_fourier_half_mode_re_expansion_tri():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.FourierHalfModeReExpansionBuilder(Elements.TRI)
        msg = "TRI should not have a Fourier Half Mode Real Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_fourier_half_mode_re_expansion_quad():
    expansion_builder = nd.FourierHalfModeReExpansionBuilder(Elements.QUAD)

    num_modes = 5

    expected_modes = (5,5)
    expected_points = (5,5)
    expected_integr_type = (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,IntegrationPoint.FOURIER_SINGLE_MODE_SPACED)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER_HALF_MODE_RE,BasisType.FOURIER_HALF_MODE_RE)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_fourier_half_mode_re_expansion_hex():
    expansion_builder = nd.FourierHalfModeReExpansionBuilder(Elements.HEX)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (5,5,5)
    expected_integr_type = (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,IntegrationPoint.FOURIER_SINGLE_MODE_SPACED)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER_HALF_MODE_RE,BasisType.FOURIER_HALF_MODE_RE,BasisType.FOURIER_HALF_MODE_RE)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_fourier_half_mode_re_expansion_tet():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.FourierHalfModeReExpansionBuilder(Elements.TET)
        msg = "TET should not have a Fourier Half Mode Real Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_fourier_half_mode_re_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.FourierHalfModeReExpansionBuilder(Elements.PYR)
        msg = "PYR should not have a Fourier Half Mode Real Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_fourier_half_mode_re_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.FourierHalfModeReExpansionBuilder(Elements.PRISM)
        msg = "PRISM should not have a Fourier Half Mode Real Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

########################################################################
# Fourier Half Mode Im Builder
#
def test_fourier_half_mode_im_expansion_seg():
    expansion_builder = nd.FourierHalfModeImExpansionBuilder(Elements.SEG)

    num_modes = 5

    expected_modes = (5,)
    expected_points = (5,)
    expected_integr_type = (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER_HALF_MODE_IM,)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_fourier_half_mode_im_expansion_tri():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.FourierHalfModeReExpansionBuilder(Elements.TRI)
        msg = "TRI should not have a Fourier Half Mode Imaginary Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_fourier_half_mode_im_expansion_quad():
    expansion_builder = nd.FourierHalfModeImExpansionBuilder(Elements.QUAD)

    num_modes = 5

    expected_modes = (5,5)
    expected_points = (5,5)
    expected_integr_type = (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,IntegrationPoint.FOURIER_SINGLE_MODE_SPACED)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER_HALF_MODE_IM,BasisType.FOURIER_HALF_MODE_IM)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_fourier_half_mode_im_expansion_hex():
    expansion_builder = nd.FourierHalfModeImExpansionBuilder(Elements.HEX)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (5,5,5)
    expected_integr_type = (IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,IntegrationPoint.FOURIER_SINGLE_MODE_SPACED,IntegrationPoint.FOURIER_SINGLE_MODE_SPACED)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER_HALF_MODE_IM,BasisType.FOURIER_HALF_MODE_IM,BasisType.FOURIER_HALF_MODE_IM)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_fourier_half_mode_im_expansion_tet():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.FourierHalfModeImExpansionBuilder(Elements.TET)
        msg = "TET should not have a Fourier Half Mode Imaginary Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_fourier_half_mode_im_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.FourierHalfModeImExpansionBuilder(Elements.PYR)
        msg = "PYR should not have a Fourier Half Mode Imaginary Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_fourier_half_mode_im_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.FourierHalfModeImExpansionBuilder(Elements.PRISM)
        msg = "PRISM should not have a Fourier Half Mode Imaginary Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

########################################################################
# Chebyshev Builder
#
def test_chebyshev_expansion_seg():
    expansion_builder = nd.ChebyshevExpansionBuilder(Elements.SEG)

    num_modes = 5

    expected_modes = (5,)
    expected_points = (5,)
    expected_integr_type = (IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV,)
    expected_field = ("")
    expected_basis = (BasisType.CHEBYSHEV,)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)
    
def test_chebyshev_expansion_tri():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.ChebyshevExpansionBuilder(Elements.TRI)
        msg = "TRI should not have a Chebyshev definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_chebyshev_expansion_quad():
    expansion_builder = nd.ChebyshevExpansionBuilder(Elements.QUAD)

    num_modes = 5

    expected_modes = (5,5)
    expected_points = (5,5)
    expected_integr_type = (IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV,IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV)
    expected_field = ("")
    expected_basis = (BasisType.CHEBYSHEV,BasisType.CHEBYSHEV)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_chebyshev_expansion_hex():
    expansion_builder = nd.ChebyshevExpansionBuilder(Elements.HEX)

    num_modes = 5

    expected_modes = (5,5,5)
    expected_points = (5,5,5)
    expected_integr_type = (IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV,IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV,IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV)
    expected_field = ("")
    expected_basis = (BasisType.CHEBYSHEV,BasisType.CHEBYSHEV,BasisType.CHEBYSHEV)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_chebyshev_expansion_tet():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.ChebyshevExpansionBuilder(Elements.TET)
        msg = "TET should not have a Chebyshev Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_chebyshev_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.ChebyshevExpansionBuilder(Elements.PYR)
        msg = "PYR should not have a Chebyshev Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_chebyshev_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.ChebyshevExpansionBuilder(Elements.PRISM)
        msg = "PRISM should not have a Chebyshev Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

########################################################################
# Fourier Chebyshev Builder
#
def test_fourier_chebyshev_expansion_seg():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.FourierChebyshevExpansionBuilder(Elements.SEG)
        msg = "SEG should not have a Fourier Chebyshev definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass
    
def test_fourier_chebyshev_expansion_tri():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.FourierChebyshevExpansionBuilder(Elements.TRI)
        msg = "TRI should not have a Fourier Chebyshev definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_fourier_chebyshev_expansion_quad():
    expansion_builder = nd.FourierChebyshevExpansionBuilder(Elements.QUAD)

    num_modes = 5

    expected_modes = (5,5)
    expected_points = (5,5)
    expected_integr_type = (IntegrationPoint.FOURIER_EVENLY_SPACED,IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER,BasisType.CHEBYSHEV)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_fourier_chebyshev_expansion_hex():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.FourierChebyshevExpansionBuilder(Elements.HEX)
        msg = "HEX should not have a Fourier Chebyshev Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_fourier_chebyshev_expansion_tet():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.FourierChebyshevExpansionBuilder(Elements.TET)
        msg = "TET should not have a Fourier Chebyshev Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_fourier_chebyshev_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.FourierChebyshevExpansionBuilder(Elements.PYR)
        msg = "PYR should not have a Fourier Chebyshev Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_fourier_chebyshev_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.FourierChebyshevExpansionBuilder(Elements.PRISM)
        msg = "PRISM should not have a Fourier Chebyshev Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

########################################################################
# Chebyshev Fourier Builder
#
def test_chebyshev_fourier_expansion_seg():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.ChebyshevFourierExpansionBuilder(Elements.SEG)
        msg = "SEG should not have a Chebyshev Fourier definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass
    
def test_chebyshev_fourier_expansion_tri():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.ChebyshevFourierExpansionBuilder(Elements.TRI)
        msg = "TRI should not have a Chebyshev Fourier definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_chebyshev_fourier_expansion_quad():
    expansion_builder = nd.ChebyshevFourierExpansionBuilder(Elements.QUAD)

    num_modes = 5

    expected_modes = (5,5)
    expected_points = (5,5)
    expected_integr_type = (IntegrationPoint.GAUSS_GAUSS_CHEBYSHEV,IntegrationPoint.FOURIER_EVENLY_SPACED)
    expected_field = ("")
    expected_basis = (BasisType.CHEBYSHEV,BasisType.FOURIER)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_chebyshev_fourier_expansion_hex():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.ChebyshevFourierExpansionBuilder(Elements.HEX)
        msg = "HEX should not have a Chebyshev Fourier Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_chebyshev_fourier_expansion_tet():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.ChebyshevFourierExpansionBuilder(Elements.TET)
        msg = "TET should not have a Chebyshev Fourier Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_chebyshev_fourier_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.ChebyshevFourierExpansionBuilder(Elements.PYR)
        msg = "PYR should not have a Chebyshev Fourier Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_chebyshev_fourier_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.ChebyshevFourierExpansionBuilder(Elements.PRISM)
        msg = "PRISM should not have a Chebyshev Fourier Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

########################################################################
# Fourier Modified Builder
#
def test_fourier_modified_expansion_seg():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.ModifiedFourierExpansionBuilder(Elements.SEG)
        msg = "SEG should not have a Fourier Modified definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass
    
def test_fourier_modified_expansion_tri():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.ModifiedFourierExpansionBuilder(Elements.TRI)
        msg = "TRI should not have a Fourier Modified definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_fourier_modified_expansion_quad():
    expansion_builder = nd.ModifiedFourierExpansionBuilder(Elements.QUAD)

    num_modes = 5

    expected_modes = (5,5)
    expected_points = (5,6)
    expected_integr_type = (IntegrationPoint.FOURIER_EVENLY_SPACED,IntegrationPoint.GAUSS_LOBATTO_LEGENDRE)
    expected_field = ("")
    expected_basis = (BasisType.FOURIER,BasisType.MODIFIED_A)

    expansion_builder.add_basis()
    expansion_builder.add_num_modes(num_modes)
    expansion_builder.add_points()

    expansion = expansion_builder.getExpansion()

    assert(expected_basis == expansion.basis)
    assert(expected_modes == expansion.num_modes)
    assert(expected_integr_type == expansion.integration_point_type)
    assert(expected_points == expansion.num_points)
    #assert(expected_field == expansion.field)

def test_fourier_modified_expansion_hex():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.ModifiedFourierExpansionBuilder(Elements.HEX)
        msg = "HEX should not have a Fourier Modified Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_fourier_modified_expansion_tet():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.ModifiedFourierExpansionBuilder(Elements.TET)
        msg = "TET should not have a Fourier Modified Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_fourier_modified_expansion_pyr():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.ModifiedFourierExpansionBuilder(Elements.PYR)
        msg = "PYR should not have a Fourier Modified Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass

def test_fourier_modified_expansion_prism():
    #no definition for this, expect correct rejection
    try:
        expansion_builder = nd.ModifiedFourierExpansionBuilder(Elements.PRISM)
        msg = "PRISM should not have a Fourier Modified Expansion definition"
        pytest.fail(msg)#if no exception thrown, fails
    except ValueError:
        pass