Common Issues
=============

Installation Issues
-------------------

.. rubric:: Error regarding Tkinter


NekUpload requires Tkinter >=v8.5, which is packaged with Python installations. Try reinstalling Python with Tkinter selected and try again.

Incorrect File Formats
----------------------

.. rubric:: Error regarding incorrect geometry file format

NekUpload enforces HDF5 format for geometry files. You are likely uploading a XML formatted geometry file. See :ref:`converting-geometry-file` for more details.

.. rubric:: Error regarding incorrect output, checkpoint or filter file format

NekUpload enforces HDF5 format for output files. You are likely uploading a XML format file. See :ref:`converting-output-files` for more details.