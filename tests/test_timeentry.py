import pytest

from salesforce_timecard.core import TimecardEntry


@pytest.mark.vcr
@pytest.mark.block_network
def test_list_timecard(mock_datetime_date_today_2020_09_18):
    te = TimecardEntry("tests/fixtures/cfg_user_password.json")

    rs = te.list_timecard(False, "2020-09-14", "2020-09-20")

    assert rs[0]["pse__Project_Name__c"] == "PX2143 - Company something"
