from dotenv import load_dotenv
import os
from NekUpload.uploadModule import InvenioRDM

#integration test for uploading files
#this one should fail, and draft deleted
#on test instance, no record should be shown
if __name__ == "__main__":
    load_dotenv()
    #currently use Invenio RDM demo instance
    URL = os.getenv("INVENIO_RDM_DEMO_URL",None)
    TOKEN = os.getenv("INVENIO_RDM_DEMO_TOKEN",None)
    COMMUNITY_SLUG = os.getenv("INVENIO_RDM_TEST_COMMUNITY_SLUG",None)

    #only run this test if environment variables exist
    if URL is not None and TOKEN is not None and COMMUNITY_SLUG is not None:
        metadata = {
            "metadata": {
                "title": "NEKTAR TEST UPLOAD AND PUBLISH TO COMMUNITY",
                "creators": [
                    {
                        "person_or_org": {
                            "given_name": "Stephen",
                            "family_name": "Liu",
                            "type": "personal",
                            "identifiers": [{"identifier": "0000-0002-1825-0097"}]
                        },
                        "affiliations": [{"name": "Imperial College London"}]
                    }
                ],
                "publisher": "InvenioRDM",
                "publication_date": "2024-05-14",
                "resource_type": {"id": "dataset"}
            }
        }

        database = InvenioRDM()
        #take tests/ as the root directory
        #error is these files do not exist in the specified paths
        #record will be created succesfully, and should then be deleted
        files = ["no_exist/ADRSolver/ADR_2D_TriQuad.nekg",
                "no_exist/ADRSolver/ADR_2D_TriQuad.xml",
                "no_exist/ADRSolver/ADR_2D_TriQuad.fld",
                "no_exist/ADRSolver/ADR_2D_TriQuad_0.chk"]

        community_slug_id = "test_nekupload"
        try:
            database.upload_files(URL,TOKEN,files,metadata,community_slug_id)
            assert False, "The upload should have failed, but it succeeded."
        except Exception as e:
            pass