from NekUpload.db.invenio_db import invenioRDM
from dotenv import load_dotenv
import os

load_dotenv()
url = os.getenv("INVENIO_RDM_DEMO_URL")
token = os.getenv("INVENIO_RDM_DEMO_TOKEN")
print(url)
metadata = {
    "metadata": {
        "title": "NEKTAR TEST UPLOAD AND PUBLISH TO COMMUNITY",
        "creators": [
            {
                "person_or_org": {
                    "given_name": "Josiah",
                    "family_name": "Carberry",
                    "type": "personal",
                    "identifiers": [{"identifier": "0000-0002-1825-0097"}]
                },
                "affiliations": [{"name": "Brown University"}]
            }
        ],
        "publisher": "InvenioRDM",
        "publication_date": "2024-05-14",
        "resource_type": {"id": "dataset"}
    }
}

database = invenioRDM()
files = ["tests/datasets/ADRSolver/ADR_2D_TriQuad.nekg",
         "tests/datasets/ADRSolver/ADR_2D_TriQuad.xml",
         "tests/datasets/ADRSolver/ADR_2D_TriQuad.fld",
         "tests/datasets/ADRSolver/ADR_2D_TriQuad_0.chk"]

community_slug_id = "test_nekupload"
database.upload_files(url,token,files,metadata,community_slug_id)