import timeit
import asyncio
import pytest

from artemis_client.session import ArtemisSession


@pytest.mark.asyncio
async def test_time_performance(artemis_session: ArtemisSession):
    start = timeit.default_timer()
    tasks = [artemis_session.time.time() for _ in range(100)]
    await asyncio.gather(*tasks)
    stop = timeit.default_timer()
    assert stop - start <= 10
