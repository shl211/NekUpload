#To run this file you must be in the examples directory
#Environment variables must be set as follows
#INVENIO_RDM_DEMO_URL is a host name for the demo instance
#INVENIO_RDM_DEMO_TOKEN is an API key
#INVENIO_RDM_TEST_COMMUNITY_SLUG is a community in InvenioRDM where drafts will be uploaded 

nekupload add-author-person "John" "Doe" --orcid "0000-0002-1825-0097"
nekupload add-info "TEST SHELL SUBCOMMANDS"
nekupload upload --host $INVENIO_RDM_DEMO_URL --api-key $INVENIO_RDM_DEMO_TOKEN --community-slug $INVENIO_RDM_TEST_COMMUNITY_SLUG -f valid_invenio_upload.py
