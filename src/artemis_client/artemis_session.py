""" Artemis Session to store credentials and reuse TCP connections.
"""
from aiohttp import ClientSession
from typing import Optional

CONFIG_FILENAME = "config.ini"


class ArtemisSession():

    session: Optional[ClientSession] = None

    def __init__(self) -> None:
        pass

    async def __aenter__(self, *_):
        self._session = ClientSession()
        return self

    async def __aexit__(self):
        await self._session.close()
