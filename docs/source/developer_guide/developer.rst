.. _developer_guide:

NekUpload is currently designed to be compatible with any online repository built with InvenioRDM (Zenodo, AE Datastore etc.) NekUpload is built with the following design:



Developer Guide
===============

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   installation

Overview
--------

This is the overview of the code

utils subpackage
----------------

.. autoclass:: NekUpload.utils.hdf5_reader::HDF5Reader
    :members:

.. autoclass:: NekUpload.utils.xml_reader::XMLReader
    :members:

uploadModule subpackage
-----------------------

.. autoclass:: NekUpload.uploadModule.db::db
    :members:
    :show-inheritance:

.. autoclass:: NekUpload.uploadModule.invenio_db::invenioRDM
    :members:
    :show-inheritance:

.. automodule:: NekUpload.uploadModule.invenio_rdm_api
    :members:

metadataModule subpackage
-------------------------
