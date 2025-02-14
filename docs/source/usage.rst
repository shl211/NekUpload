User Guide
==========

NekUpload by default will attempt to upload provided Nektar++ datasets to a database within the Department of Aeronautics, Imperial College London. This database is built upon `InvenioRDM <https://invenio-software.org/products/rdm/>`_ online repository. 

.. note::

    Technically, as long as the user has access to a suitable host URL, API key and community slug or UUID, datasets can be uploaded to any database built with InvenioRDM, such as `Zenodo <https://zenodo.org/>`_.

Setup
-----

Users will have to first acquire an API key from their InvenioRDM account.

Acquiring API key
~~~~~~~~~~~~~~~~~

Login to your InvenioRDM account. This is located at **??**. Go to Account, and locate *Applications*. Generate a personal access token by clicking *new token*. Provide a name for the the key and select the relevant scope, which is **deposit:write**. Create the key and make a note of the API key.

.. note::

    There may be options for API key scope, and these vary depending on the InvenioRDM instance. Best practice dictates that the minimum privilege level should be selected to alleviate security concerns. At minimum, users must have **deposit:write** permissions. If you do not see an option for this, then that means the API key automatically has that configuration. 

Setting Up API key
~~~~~~~~~~~~~~~~~~

Create a **.env** file in your root directory. Add the following:

.. code-block::

    NEKTAR_DB_API_KEY=API_KEY

where API_KEY should be replaced with your API key. This is to help prevent your API key being leaked by being present within the computer memory. Obviously, this only minimises the security risk of an API key being exposed, as it will eventually be loaded into memory (but in a very small scope) for upload purposes. Therefore, once you are finished uploading all data and have received a receipt of upload, please delete your API key by logging back onto the online portal.

.. attention::

    API keys should be deleted after use by logging back into the online portal and deleting the key. Also, do not commit your API keys to version control systems.

GUI Application
---------------

To run the GUI application, execute the following command:

.. code-block::

    nekupload-app

.. note::
    If this fails, check that your **tkinter** version is greater than v8.5. Python installations are usually bundled with this version. To update your **tkinter** version, see `TkDocs <https://tkdocs.com/tutorial/install.html>`_ for upgrading.

The fields for the Nektar++ database uploads should be pre-loaded with the following fields

- Host Name: https://data.ae.ic.ac.uk
- Community Slug: nektar

The host name refers to where the database is located, and the community slug is the identification of which community/group the dataset will be submitted to for approval. If users wish to upload to somewhere else, they are free to configure the settings. Fill in the fields and submit. 

Observing Completion
~~~~~~~~~~~~~~~~~~~~

Currently, the only way to view whether the files have succeeded uploading is to view the Python terminal. This will be improved in the future

.. note::
    Better output logs will be provided in the future

Shell scripting
---------------

TBC