from freezegun import freeze_time
from salesforce_timecard.core import TimecardEntry
import pytest


@pytest.fixture(scope="module")
def vcr_config():
    return {"decode_compressed_response": True}



@freeze_time("2020-9-18")
@pytest.mark.vcr()
@pytest.mark.block_network
def test_list_timecard():
    te = TimecardEntry("tests/fixtures/cfg_user_password.json")

    rs = te.list_timecard(False, "2020-09-14", "2020-09-20")
    print(rs[0])
    assert rs[0]["pse__Project_Name__c"] == "PX2143 - Company something"