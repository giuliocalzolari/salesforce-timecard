from freezegun import freeze_time
from salesforce_timecard.core import TimecardEntry
import pytest
import json


@freeze_time("2020-9-18")
@pytest.mark.vcr()
@pytest.mark.block_network
def test_delete_timecard():
    te = TimecardEntry("tests/fixtures/cfg_user_password.json")
    rs = te.list_timecard(False, "2020-09-14", "2020-09-20")
    assert rs[0]["Id"] ==  "a8D5I000000GtOMUA0"

    rs_del = te.delete_time_entry(rs[0]["Id"])
    assert rs_del ==  204
