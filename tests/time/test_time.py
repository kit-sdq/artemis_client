import pytest
from datetime import datetime

from artemis_client.session import ArtemisSession


@pytest.mark.asyncio
async def test_time(artemis_session: ArtemisSession):
    date = await artemis_session.time.time()
    assert (date - datetime.now()).total_seconds() < 60


@pytest.mark.asyncio
async def test_time_type(artemis_session: ArtemisSession):
    date = await artemis_session.time.time()
    assert isinstance(date, datetime)
