from dotenv import load_dotenv
import os
from NekUpload.db import invenioRDM
from memory_profiler import profile

#integration test for uploading files
#this one should fail, and draft deleted
#on test instance, no record should be shown
#@profile #uncomment for memory profiler
def demo():
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

        database = invenioRDM()
        files = ["../tests/datasets/ADRSolver/ADR_2D_TriQuad.nekg",
                "../tests/datasets/ADRSolver/ADR_2D_TriQuad.xml",
                "../tests/datasets/ADRSolver/ADR_2D_TriQuad.fld",
                "../tests/datasets/ADRSolver/ADR_2D_TriQuad_0.chk"]

        #get absolute path from wherever this is run
        files_abs_paths = [os.path.join(os.path.dirname(__file__),f) for f in files]

        try:
            database.upload_files(URL,TOKEN,files_abs_paths,metadata,COMMUNITY_SLUG)
        except Exception as e:
            assert False, "The upload should have succeeded, but it failed."

if __name__ == "__main__":
    demo()