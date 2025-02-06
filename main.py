from NekUpload.utils.hdf5_reader import HDF5Reader

with HDF5Reader("tests/datasets/ADRSolver/ADR_3D_AllElmt.nekg") as reader:
    reader.get_keys()
    print(reader.summary())