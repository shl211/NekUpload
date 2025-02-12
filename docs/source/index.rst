.. NekUpload documentation master file, created by
   sphinx-quickstart on Wed Feb 12 15:10:52 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

NekUpload Documentation
=======================

**NekUpload** is a Python package for uploading `Nektar++ <https://nektar.info>`_ datasets to a specified database. Automated validation and metadata extraction will occur, and the datasets will be submitted to the database admin for review. There are multiple ways to utilise the program. Users can utilise this with an interactive GUI for local file uploads. For larger file uploads, it is recommended that shell scripting be used for submission to HPC systems. Check out the :doc:`usage` section for more information to get started. 



.. note::
   This project is under active development.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage
   developer
   api
