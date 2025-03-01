import h5py
import numpy as np
import pytest
import os

@pytest.fixture
def create_missing_mesh_pair():
    """This has a HEX Maps but no corresponding HEX Mesh
    """
    filename = create_geometry_template("missing_map_pair.h5")

    with h5py.File(filename,"a") as f:
        maps_group = f.require_group("NEKTAR/GEOMETRY/MAPS")  # Ensure group exists
        
        # If dataset already exists, delete it
        if "HEX" in maps_group:
            del maps_group["HEX"]  # Remove old dataset
        
        # Create the dataset
        maps_group.create_dataset("HEX", data=np.arange(30, dtype=np.int32))
    
    yield filename
    os.remove(filename)

@pytest.fixture
def create_missing_maps_pair():
    """This has a HEX Mesh but no corresponding HEX Maps
    """
    filename = create_geometry_template("missing_mesh_pair.h5")

    with h5py.File(filename,"a") as f:
        mesh_group = f.require_group("NEKTAR/GEOMETRY/MESH")  # Ensure group exists
        
        # If dataset already exists, delete it
        if "HEX" in mesh_group:
            del mesh_group["HEX"]  # Remove old dataset
        
        # Create the dataset
        mesh_group.create_dataset("HEX", data=np.arange(120, dtype=np.int32).reshape(20, 6))
    
    yield filename
    os.remove(filename)

@pytest.fixture
def create_missing_inconsistent_pair():
    """This has a HEX Mesh and Maps but with different lengths
    """
    filename = create_geometry_template("inconsistent_pairs.h5")

    with h5py.File(filename,"a") as f:
        mesh_group = f.require_group("NEKTAR/GEOMETRY/MESH")  # Ensure group exists
        maps_group = f.require_group("NEKTAR/GEOMETRY/MAPS")
        
        if "HEX" in mesh_group:
            del mesh_group["HEX"]
        if "HEX" in maps_group:
            del maps_group["HEX"]
        
        mesh_group.create_dataset("HEX", data=np.arange(120, dtype=np.int32).reshape(20, 6))
        maps_group.create_dataset("HEX", data=np.arange(30, dtype=np.int32))
        
    yield filename
    os.remove(filename)

@pytest.fixture
def create_hex_with_missing_2d():
    """This has a HEX but no quads
    """
    filename = create_geometry_template("missing_quads_for_hexes.h5")

    with h5py.File(filename,"a") as f:
        mesh_group = f.require_group("NEKTAR/GEOMETRY/MESH")  # Ensure group exists
        maps_group = f.require_group("NEKTAR/GEOMETRY/MAPS")
        
        if "QUAD" in mesh_group:
            del mesh_group["QUAD"]
        if "HEX" in mesh_group:
            del mesh_group["HEX"]

        if "QUAD" in maps_group:
            del maps_group["QUAD"]
        if "HEX" in maps_group:
            del maps_group["HEX"]
        
        mesh_group.create_dataset("HEX", data=np.arange(180, dtype=np.int32).reshape(30, 6))
        maps_group.create_dataset("HEX", data=np.arange(30, dtype=np.int32))
        
    yield filename
    os.remove(filename)

@pytest.fixture
def create_tet_with_missing_2d():
    """This has a TET but no tris
    """
    filename = create_geometry_template("missing_tris_for_tets.h5")

    with h5py.File(filename,"a") as f:
        mesh_group = f.require_group("NEKTAR/GEOMETRY/MESH")  # Ensure group exists
        maps_group = f.require_group("NEKTAR/GEOMETRY/MAPS")
        
        if "TRI" in mesh_group:
            del mesh_group["TRI"]
        if "TET" in mesh_group:
            del mesh_group["TET"]

        if "TRI" in maps_group:
            del maps_group["TRI"]
        if "TET" in maps_group:
            del maps_group["TET"]
        
        mesh_group.create_dataset("TET", data=np.arange(120, dtype=np.int32).reshape(30, 4))
        maps_group.create_dataset("TET", data=np.arange(30, dtype=np.int32))
        
    yield filename
    os.remove(filename)

@pytest.fixture
def create_pyr_with_missing_2d_quad():
    """This has a PYR but no quads
    """
    filename = create_geometry_template("missing_quads_for_pyr.h5")

    with h5py.File(filename,"a") as f:
        mesh_group = f.require_group("NEKTAR/GEOMETRY/MESH")  # Ensure group exists
        maps_group = f.require_group("NEKTAR/GEOMETRY/MAPS")
        
        if "QUAD" in mesh_group:
            del mesh_group["QUAD"]
        if "PYR" in mesh_group:
            del mesh_group["PYR"]

        if "QUAD" in maps_group:
            del maps_group["QUAD"]
        if "PYR" in maps_group:
            del maps_group["PYR"]
        
        mesh_group.create_dataset("PYR", data=np.arange(150, dtype=np.int32).reshape(30, 5))
        maps_group.create_dataset("PYR", data=np.arange(30, dtype=np.int32))
        
    yield filename
    os.remove(filename)

@pytest.fixture
def create_pyr_with_missing_2d_tri():
    """This has a PYR but no tris
    """
    filename = create_geometry_template("missing_tris_for_pyr.h5")

    with h5py.File(filename,"a") as f:
        mesh_group = f.require_group("NEKTAR/GEOMETRY/MESH")  # Ensure group exists
        maps_group = f.require_group("NEKTAR/GEOMETRY/MAPS")
        
        if "TRI" in mesh_group:
            del mesh_group["TRI"]
        if "PYR" in mesh_group:
            del mesh_group["PYR"]

        if "TRI" in maps_group:
            del maps_group["TRI"]
        if "PYR" in maps_group:
            del maps_group["PYR"]
        
        mesh_group.create_dataset("PYR", data=np.arange(150, dtype=np.int32).reshape(30, 5))
        maps_group.create_dataset("PYR", data=np.arange(30, dtype=np.int32))
        
    yield filename
    os.remove(filename)

@pytest.fixture
def create_prism_with_missing_2d_quad():
    """This has a PRISM but no quads
    """
    filename = create_geometry_template("missing_quads_for_prism.h5")

    with h5py.File(filename,"a") as f:
        mesh_group = f.require_group("NEKTAR/GEOMETRY/MESH")  # Ensure group exists
        maps_group = f.require_group("NEKTAR/GEOMETRY/MAPS")
        
        if "QUAD" in mesh_group:
            del mesh_group["QUAD"]
        if "PRISM" in mesh_group:
            del mesh_group["PRISM"]

        if "QUAD" in maps_group:
            del maps_group["QUAD"]
        if "PRISM" in maps_group:
            del maps_group["PRISM"]
        
        mesh_group.create_dataset("PRISM", data=np.arange(150, dtype=np.int32).reshape(30, 5))
        maps_group.create_dataset("PRISM", data=np.arange(30, dtype=np.int32))
        
    yield filename
    os.remove(filename)

@pytest.fixture
def create_prism_with_missing_2d_tri():
    """This has a PRISM but no tris
    """
    filename = create_geometry_template("missing_tris_for_prism.h5")

    with h5py.File(filename,"a") as f:
        mesh_group = f.require_group("NEKTAR/GEOMETRY/MESH")  # Ensure group exists
        maps_group = f.require_group("NEKTAR/GEOMETRY/MAPS")
        
        if "TRI" in mesh_group:
            del mesh_group["TRI"]
        if "PRISM" in mesh_group:
            del mesh_group["PRISM"]

        if "TRI" in maps_group:
            del maps_group["TRI"]
        if "PRISM" in maps_group:
            del maps_group["PRISM"]
        
        mesh_group.create_dataset("PRISM", data=np.arange(150, dtype=np.int32).reshape(30, 5))
        maps_group.create_dataset("PRISM", data=np.arange(30, dtype=np.int32))
        
    yield filename
    os.remove(filename)

def create_geometry_template(filename: str) -> str:
    """This generates the same file as ADR_2D_TriQuad.nekg

    Args:
        filename (str): Name of file
    """
    # Create an HDF5 file
    with h5py.File(filename, "w") as f:
        nektar = f.create_group("NEKTAR")
        geometry = nektar.create_group("GEOMETRY")
        maps = geometry.create_group("MAPS")
        mesh = geometry.create_group("MESH")
        
        # Attributes
        geometry.attrs["FORMAT_VERSION"] = 2
        
        # MAPS datasets
        maps.create_dataset("COMPOSITE", data=np.arange(11, dtype=np.int32))
        maps.create_dataset("CURVE_EDGE", data=np.array([], dtype=np.int32))
        maps.create_dataset("CURVE_FACE", data=np.array([], dtype=np.int32))
        maps.create_dataset("DOMAIN", data=np.array([0, 1], dtype=np.int32))
        maps.create_dataset("QUAD", data=np.arange(22, 48, dtype=np.int32))
        maps.create_dataset("SEG", data=np.arange(96, dtype=np.int32))
        maps.create_dataset("TRI", data=np.arange(22, dtype=np.int32))
        maps.create_dataset("VERT", data=np.arange(49, dtype=np.int32))
        
        # MESH datasets
        composite_data = [b' Q[22-47] ', b' T[0-21] ', b' E[0-1] ', b' E[2-5] ', b' E[45] ',
                        b' E[56] ', b' E[67] ', b' E[79] ', b' E[88] ', b' E[94-95] ',
                        b' E[84,75,69,62,51,40,30,20,6] ']
        mesh.create_dataset("COMPOSITE", data=np.array(composite_data, dtype='S'))
        mesh.create_dataset("CURVE_EDGE", data=np.empty((0, 3), dtype=np.int32))
        mesh.create_dataset("CURVE_FACE", data=np.empty((0, 3), dtype=np.int32))
        mesh.create_dataset("CURVE_NODES", data=np.empty((0, 3), dtype=np.float64))
        mesh.create_dataset("DOMAIN", data=np.array([b'0', b'1'], dtype='S'))
        mesh.create_dataset("QUAD", data=np.array([
            [35, 41, 46, 40], [36, 42, 47, 41], [37, 43, 48, 42], [38, 44, 49, 43],
            [39, 45, 50, 44], [46, 52, 57, 51], [47, 53, 58, 52], [48, 54, 59, 53],
            [49, 55, 60, 54], [50, 56, 61, 55], [57, 63, 68, 62], [58, 64, 70, 63],
            [59, 65, 72, 64], [60, 66, 73, 65], [61, 67, 74, 66], [68, 70, 71, 69],
            [71, 76, 80, 75], [72, 77, 81, 76], [73, 78, 82, 77], [74, 79, 83, 78],
            [80, 85, 89, 84], [81, 86, 90, 85], [82, 87, 91, 86], [83, 88, 92, 87],
            [89, 90, 93, 94], [91, 92, 95, 93]
        ], dtype=np.int32))
        mesh.create_dataset("SEG", data=np.empty((96, 2), dtype=np.int32))
        mesh.create_dataset("TRI", data=np.empty((22, 3), dtype=np.int32))
        mesh.create_dataset("VERT", data=np.empty((49, 3), dtype=np.float64))

    return filename