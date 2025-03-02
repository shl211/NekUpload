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

    git clone https://github.com/shl211/NekUpload
    pip install -e .

Note that this requires Python version >=3.11.


Checking Installation
---------------------

Run pytest to check all tests are working. You may notice that some tests are skipped. This is intentional and just means that you have not obtained and stored the necessary API keys yet.

Setup
-----

API keys must be acquired. For testing, we utilise the InvenioRDM demo instance hosted at https://inveniordm.web.cern.ch. You will need to make an account and acquire an API key.

Acquiring an API key
~~~~~~~~~~~~~~~~~~~~

An API key is required to utilise this application. To access an API key, go to the online repository host. Login to your account and select your profile. You will see an option: *Applications*, as shown in the following image:

.. image:: ../_static/quickstart1.png
    :alt: Image showing where to find *Applications*
    :align: center

Under *Personal access tokens*, click *new token* to generate an API key. Provide it with a name, and under *scopes* you should select **deposit:write**. Then create the API key.

.. tip::

    If you do not see the option to select **deposit:write** under scopes, then you already have those permissions. Continue and create the API key.

Community
~~~~~~~~~

A test community has been set up: TEST_NEKTAR_UPLOAD. Join this if possible, otherwise, create your own test community.

Environment variables
~~~~~~~~~~~~~~~~~~~~~

Store the following in a *.env* file in the project root:

.. code::

    INVENIO_RDM_DEMO_URL=https://inveniordm.web.cern.ch
    INVENIO_RDM_DEMO_TOKEN=<YOUR_API_KEY_HERE>
    INVENIO_RDM_TEST_COMMUNITY_SLUG=test_nekupload #or the slug for your own test community

.. warning::

    API keys should be securely managed. They should never be committed to version control and minimum privileges should be granted to accomplish the required task. As part of best practice, generate a new API token every week.