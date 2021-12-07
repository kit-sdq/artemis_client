""" This file configures pytest.
"""
import asyncio
import pytest

from artemis_client.artemis_session import ArtemisSession


# Make sure the event loop is reused: Allow reusing artemis session
@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session", autouse=True)
async def artemis_session():
    async with ArtemisSession() as session:
        yield session
