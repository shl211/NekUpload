Installation
============

Virtual Environment
-------------------

A virtual environment is highly recommended to isolate your project's dependencies and prevent conflicts with other Python projects you may have. This ensures a clean and consistent environment for NekUpload.

Creating a Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before installing the package, create a python environment with your desired Python version. Python versions from 3.11 onwards are required. 

For **pyenv**:

.. code-block:: console
    
    pyenv virtualenv 3.11.0 nekupload-env
    pyenv activate nekupload-env

For **venv**:

.. code-block:: console

    python3 -m venv nekupload-env
    source nekupload-env/bin/activate

For **conda**:

.. code-block:: console

    conda create --name nekupload-env python=3.11
    conda activate nekupload-env

NekUpload can be located on PyPI, and can be installed using:

Installing the Package
----------------------

.. code::

    pip install NekUpload

Note that this requires Python version >=3.11.

Next Steps
----------

There are currently two entry points for executing the upload and validation pipeline. An app with GUI interface is provided for local file uploads. This is designed for small file uploads. For larger datasets it is recommended to utilise shell scripting and submit to a HPC system.