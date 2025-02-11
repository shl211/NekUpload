from NekUpload.metadataModule.identifier import Identifier,IdentifierType
import pytest

def test_valid_ORCID():
    #taken from 
    #https://support.orcid.org/hc/en-us/articles/360053289173-Why-does-my-ORCID-iD-have-an-X#:~:text=ORCID%20iD%27s%20that%20end%20with%20an%20X%20are,digits%20of%20your%20identifier%20form%20a%20coherent%20iD.
    valid_ids = {
        "test_case_1": "0000-0001-5109-3700",
        "test_case_2": "0000-0002-1825-0097",
        "test_case_3": "0000-0002-1694-233X",
    }

    for test_case, id in valid_ids.items():
        try:
            identifier = Identifier(id, IdentifierType.ORCID)

            assert(identifier.get_id() == id)
            assert(identifier.get_id_type() == IdentifierType.ORCID)
        except ValueError:
            assert False, f"{test_case} was incorrectly rejected"

def test_invalid_ORCID():
    invalid_ids = {
        "too_short_length": "0000-0002-1825-009",
        "too_long_length": "0000-0002-1825-00971",
        "invalid_char": "0000-0002-182A-0097",
        "wrong_checksum": "0000-0002-1825-0098",
        "missing_hyphens": "0000000218250097",
        "misplaced_hyphens": "0000000-21825-0097"
    }

    for test_case,id in invalid_ids.items():
        try:
            Identifier(id,IdentifierType.ORCID)
            
            #constructor should throw error, so should never reach this point
            assert False, f"{test_case} was not correctly rejected"
        except ValueError:
            pass

@pytest.mark.skip
def test_valid_ISNI():
    valid_ids = {
        "test_case_1": "000000012146438X"
        }

    for test_case, id in valid_ids.items():
        try:
            identifier = Identifier(id, IdentifierType.ISNI)

            assert(identifier.get_id() == id)
            assert(identifier.get_id_type() == IdentifierType.ISNI)
        except ValueError:
            assert False, f"{test_case} was incorrectly rejected"