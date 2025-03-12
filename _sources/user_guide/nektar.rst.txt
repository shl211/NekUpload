Nektar++
========

Users of this software are expected to have generated datasets using Nektar++.

Nektar++ Best Practices
-----------------------

A Nektar++ simulation dataset following best practices must consist of at least:

* session.xml - Session file in XML format
* geometry.nekg - Geometry file in HDF5 format
* output.fld - Output file in HDF5 format

It can optionally have:

* checkpoint.chk - Checkpoint files in HDF5 format
* filter.fce - Filter files in HDF5 format

Supporting items to the dataset can include:

* Images (\*jpg,\*png)
* Research Papers (\*.pdf)

Since Nektar++ v5.0.0, there has been full HDF5 support for geometry and output files. HDF5 files provide many benefits over the traditional XML format for geometry and output. XML files are inefficient to load into memory. The entire file is often loaded into the program's memory before it can be parsed and used. With HDF5, many readers support memory mapping, which allows for faster read access. Moreover, range loading is supported, so only relevant sections of the file have to be loaded in. Parallel I/O is also supported.

Therefore, there is a shift towards XML file formats towards HDF5 where applicable, and this software will enforce these best practices.

Converting files
----------------

For older simulation datasets that are follow the old Nektar++ best practices, where all files are in plain XML format with the geometry encoded as an Endian, conversion is necessary. NekUpload currently does not provide tools to automate the conversion process, so users must convert files themselves. 

Nektar++ provides the **NekMesh** and **FieldConvert** commands that can be used to convert files from XML format to HDF5 format. **FieldConvert** is part of the `Nektar++ installation <https://www.nektar.info/getting-started/installation/>`_. HDF5 support and MPI support must be enabled if building Nektar++ from source.

.. _converting-geometry-file:

Obtaining geometry.nekg
^^^^^^^^^^^^^^^^^^^^^^^

In XML format, the geometry is sometimes nested inside session.xml, or can be in a separate geometry.xml file. To obtain a geometry.nekg file utilise the following command:

.. code::
    
    #if geometry is within session file 
    NekMesh session.xml HDF5geometry.nekg

    #if geometry is separate to session file
    nekupload mergexml session.xml geometry.xml merged_session.xml
    NekMesh merged_session.xml HDF5geometry.nekg

This will generate two files: HDF5geometry.xml (the new session file) and HDF5geometry.nekg (the new geometry file). An additional flag in the session file is required, ensuring it is placed before the expansion list being: 

.. code::

    1    <GEOMETRY DIM="3" SPACE="3" HDF5FILE="HDF5Mesh.nekg" />

For more info, see `Section 4.5.2.1 of the Nektar User Guide <https://doc.nektar.info/userguide/latest/user-guidese19.html#x28-1230004.5>`_

.. note::

    **NekMesh** only accepts one input file for converting xml to nekg. To workaround this, this package provides a CLI **nekupload**. *nekupload mergexml file1 file2 output* will merge the two stated files, and any repeated first level elements are replaced with the one specified in file2. This is the standard Nektar++ behaviour when multiple input files are detected for a solver e.g. *ADRSolver file1.xml file2.xml* file1 and file2 are merged as per the previously stated rule. The new merged XML file can then be used with **NekMesh** as usual.

.. warning::

    Order of files specified is important in **nekupload**. First-level elements, such as <EXPANSIONS>, in first file will be replaced by the one defined in second file if present. Otherwise, appended. Formatting may be screwed up a little, so always double check files afterwards. 

.. _converting-output-files:

Obtaining HDF5 Filter, Checkpoint & Output files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Convert files using:

.. code::

    FieldConvert in.fld out.fld:fld:format=Hdf5

TBC for chk and fce

For more info see `Section 5.3 of the Nektar User Guide <https://doc.nektar.info/userguide/latest/user-guidese23.html#x36-1640005.3>`_