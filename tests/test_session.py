import pytest
from artemis_client.artemis_session import ArtemisSession


@pytest.mark.asyncio
async def test_wrong_usage():
    with pytest.raises(RuntimeError):
        session = ArtemisSession()
        await session.get_api_endpoint("/test")


@pytest.mark.asyncio
async def test_correct_usage():
    async with ArtemisSession() as session:
        resp = await session.get_endpoint("/time")
        assert resp.ok
