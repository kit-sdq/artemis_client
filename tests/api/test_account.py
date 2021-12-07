import pytest

from artemis_client.api.account import isAuthenticated


@pytest.mark.asyncio
async def test_isAuthenticated(artemis_session):
    assert isAuthenticated(artemis_session)
