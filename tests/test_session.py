import pytest
from artemis_client.artemis_session import ArtemisSession


@pytest.mark.asyncio
async def test_session():
    session = ArtemisSession()
    async with session:
        pass

    async with session:
        pass
