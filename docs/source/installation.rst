Installation
============

To use NekUpload, first clone the repository:

.. code-block:: console
    
    git clone ..

Virtual Environment
-------------------

A virtual environment is highly recommended to isolate your project's dependencies and prevent conflicts with other Python projects you may have. This ensures a clean and consistent environment for NekUpload.

Creating a Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before installing the package, create a python environment with your desired Python version. Python versions from 3.8 onwards are recommended. 

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

Installing the Package
----------------------

To install the NekUpload package, run:

.. code-block:: console

   pip install -r requirements.txt .

To test whether the installation is successful, run the test suite with

.. code-block:: console

    pytest

.. note::

    After running the test, you may notice that some tests were skipped over. This is because demo API keys have not been set up for testing purposes. As a user, you can safely ignore this. If you are a developer, refer to the :ref:`developer_guide` for more information.

Next Steps
----------

There are currently two entry points for executing the upload and validation pipeline. An app with GUI interface is provided for local file uploads. This is designed for small file uploads. For larger datasets it is recommended to utilise shell scripting and submit to a HPC system.

