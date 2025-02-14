from dotenv import load_dotenv
import os
from NekUpload.uploadModule import invenioRDM
from NekUpload.metadataModule import *
from memory_profiler import profile

#integration test for uploading files
#this one should fail, and draft deleted
#@profile #uncomment for memory profiler
def demo():
    load_dotenv()
    #currently use Invenio RDM demo instance
    URL = os.getenv("INVENIO_RDM_DEMO_URL",None)
    TOKEN = os.getenv("INVENIO_RDM_DEMO_TOKEN",None)
    COMMUNITY_SLUG = os.getenv("INVENIO_RDM_TEST_COMMUNITY_SLUG",None)

    #only run this test if environment variables exist
    if URL is not None and TOKEN is not None and COMMUNITY_SLUG is not None:
        
        title = "NEKTAR TEST METADATA INTEGRATION UPLOAD"
        publisher = "InvenioRDM"
        version = "v1.2.3"
        resource_type = "dataset"
        publication_date = "2025"

        author = InvenioPersonInfo("Vladimir","Putin")
        author.add_identifier(Identifier("0000-0002-1825-0097",IdentifierType.ORCID))

        metadata_obj = InvenioMetadata(title,publication_date,[author],resource_type)
        metadata_obj.add_publisher(publisher)
        metadata_obj.add_version(version)
        metadata_obj.add_description("This is a test integration of metadata module with upload module")

        metadata_payload = metadata_obj.get_metadata_payload()

        metadata = {"metadata" : metadata_payload}

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