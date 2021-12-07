""" Artemis Session to store credentials and reuse TCP connections.
"""
from aiohttp import ClientSession
from typing import Optional
import logging

from artemis_client.artemis_api import LoginVM
from .configuration import get_url, get_value

AUTHORIZATION_HEADER = "authorization"


class ArtemisSession:

    _session: Optional[ClientSession] = None
    _token: Optional[str] = None

    def __init__(self) -> None:
        pass

    async def __aenter__(self, *_):
        self._session = ClientSession()
        if self._token is None:
            self._token = await self._login()
        self._session.headers[AUTHORIZATION_HEADER] = self._token
        return self

    async def __aexit__(self, *_):
        await self._get_session().close()

    async def _login(self) -> str:
        login_vm: LoginVM = {
            "username": get_value("ARTEMIS", "USERNAME"),
            "password": get_value("ARTEMIS", "PASSWORD"),
            "rememberMe": False,
        }
        resp = await self.post_api_endpoint("/authenticate", json=login_vm)
        if resp.ok:
            logging.debug(f"logged in to {get_url('ARTEMIS', 'URL')}")
            return resp.headers[AUTHORIZATION_HEADER]
        else:
            raise ConnectionError(f"could not login to {get_url('ARTEMIS', 'URL')}")

    async def post_api_endpoint(self, endpoint, **data):
        return await self._get_session().post(
            self._get_api_endpoint_url(endpoint), **data
        )

    def _get_api_endpoint_url(self, endpoint=""):
        return get_url("ARTEMIS", "URL") + "/api" + endpoint

    def _get_session(self):
        if self._session is None:
            raise RuntimeError(
                "Use ArtemisSession only in a 'async with' statement (Context Manager)"
            )

        return self._session
