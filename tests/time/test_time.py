import pytest
from datetime import datetime
from artemis_client.time.time import time


@pytest.mark.asyncio
async def test_time(artemis_session):
    date = await time(artemis_session)
    assert (date - datetime.now()).total_seconds() < 60


@pytest.mark.asyncio
async def test_time_type(artemis_session):
    date = await time(artemis_session)
    assert isinstance(date, datetime)
