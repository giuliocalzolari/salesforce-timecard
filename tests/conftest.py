import datetime
from unittest.mock import MagicMock

import pytest


@pytest.fixture()
def mock_datetime_date_today_2020_09_18(monkeypatch):
    """Mock this datetime.date.today()."""
    datetime_mock = MagicMock(wraps=datetime.date)
    datetime_mock.today.return_value = datetime.datetime(2020, 9, 18)
    monkeypatch.setattr(datetime, "datetime", datetime_mock)


@pytest.fixture(scope="module")
def vcr_config():
    return {"decode_compressed_response": True}
