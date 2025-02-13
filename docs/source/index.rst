.. NekUpload documentation master file, created by
   sphinx-quickstart on Wed Feb 12 15:10:52 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

NekUpload Documentation
=======================

**NekUpload** is a Python package for uploading `Nektar++ <https://nektar.info>`_ datasets to a specified database. Automated validation and metadata extraction will occur, and the datasets will be submitted to the database admin for review. There are multiple ways to utilise the program. Users can utilise this with an interactive GUI for local file uploads. For larger file uploads, it is recommended that shell scripting be used for submission to HPC systems. Check out the :doc:`usage` section for more information to get started. 

Motivation
----------

Why use this package when there are other ways to upload?

This package provides an extra layer of verification to make both Nektar++ users and database administrators life easier. It also extracts relevant information from the datasets to reduce the amount of metadata input the user must provide. This pipeline also ensures that Nektar++ users submit all the relevant files and do not accidentally miss out or include non-relevant files. This will also automate the upload process, allowing for large dataset uploads to be transferred more efficiently from a non-interactive environment (such as an HPC environment). The database admin, knowing that the datasets are self-consistent and verified, can speed up the verification process, allowing for datasets to be made publicly available faster. 

.. note::
   This project is under active development.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   developer
   api
