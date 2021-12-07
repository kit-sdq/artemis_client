""" Artemis Session to store credentials and reuse TCP connections.
"""
from aiohttp import ClientSession
from typing import Optional
import logging

from aiohttp.client_reqrep import ClientResponse

from artemis_client.artemis_api import LoginVM
from .configuration import get_url, get_value

AUTHORIZATION_HEADER = "authorization"


class ArtemisSession:
    """This class describes an session with the Artemis REST API.

    Usage:
    async with ArtemisSession() as session:
        # do something with session

    This class is based of aiohttp.ClienSession().
    All API methods allow supplying kwargs controlling the underlaying
    ClientSession method.
    """

    _session: Optional[ClientSession] = None
    _token: Optional[str] = None
    _url: str
    _login_vm: LoginVM

    def __init__(self, url: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None) -> None:
        self._login_vm = {
            "username": username or get_value("ARTEMIS", "USERNAME"),
            "password": password or get_value("ARTEMIS", "PASSWORD"),
            "rememberMe": False,
        }
        self._url = url or get_url("ARTEMIS", "URL")

    async def __aenter__(self, *_):
        self._session = ClientSession(self._url)
        if self._token is None:
            self._token = await self._login()
        self._session.headers[AUTHORIZATION_HEADER] = self._token
        return self

    async def __aexit__(self, *_):
        await self._get_session().close()

    async def _login(self) -> str:
        resp = await self.post_api_endpoint("/authenticate", json=self._login_vm)
        if resp.ok:
            logging.debug(f"logged in to {self._url}")
            return resp.headers[AUTHORIZATION_HEADER]
        else:
            raise ConnectionError(f"could not login to {self._url}")

    ###################################

    # Query ARTEMIS endpoints

    async def get_endpoint(self, endpoint: str, **get_args) -> ClientResponse:
        return await self._get_session().get(
            self._get_endpoint_url(endpoint), **get_args
        )

    async def post_endpoint(self, endpoint: str, **post_args) -> ClientResponse:
        return await self._get_session().post(
            self._get_endpoint_url(endpoint), **post_args
        )

    async def put_endpoint(self, endpoint: str, **put_args) -> ClientResponse:
        return await self._get_session().put(
            self._get_endpoint_url(endpoint), **put_args
        )

    async def delete_endpoint(self, endpoint: str, **put_args) -> ClientResponse:
        return await self._get_session().delete(
            self._get_endpoint_url(endpoint), **put_args
        )

    async def head_endpoint(self, endpoint: str, **put_args) -> ClientResponse:
        return await self._get_session().head(
            self._get_endpoint_url(endpoint), **put_args
        )

    async def options_endpoint(self, endpoint: str, **put_args) -> ClientResponse:
        return await self._get_session().options(
            self._get_endpoint_url(endpoint), **put_args
        )

    async def patch_endpoint(self, endpoint: str, **put_args) -> ClientResponse:
        return await self._get_session().patch(
            self._get_endpoint_url(endpoint), **put_args
        )

    # Query Artemis /api endpoints

    async def get_api_endpoint(self, api_endpoint: str, **get_args) -> ClientResponse:
        return await self._get_session().get(
            self._get_api_endpoint_url(api_endpoint), **get_args
        )

    async def post_api_endpoint(self, api_endpoint: str, **post_args) -> ClientResponse:
        return await self._get_session().post(
            self._get_api_endpoint_url(api_endpoint), **post_args
        )

    async def put_api_endpoint(self, api_endpoint: str, **put_args) -> ClientResponse:
        return await self._get_session().put(
            self._get_api_endpoint_url(api_endpoint), **put_args
        )

    async def delete_api_endpoint(self, api_endpoint: str, **put_args) -> ClientResponse:
        return await self._get_session().delete(
            self._get_api_endpoint_url(api_endpoint), **put_args
        )

    async def head_api_endpoint(self, api_endpoint: str, **put_args) -> ClientResponse:
        return await self._get_session().head(
            self._get_api_endpoint_url(api_endpoint), **put_args
        )

    async def options_api_endpoint(self, api_endpoint: str, **put_args) -> ClientResponse:
        return await self._get_session().options(
            self._get_api_endpoint_url(api_endpoint), **put_args
        )

    async def patch_api_endpoint(self, api_endpoint: str, **put_args) -> ClientResponse:
        return await self._get_session().patch(
            self._get_api_endpoint_url(api_endpoint), **put_args
        )

    ###################################

    def _get_endpoint_url(self, endpoint: str) -> str:
        return endpoint

    def _get_api_endpoint_url(self, endpoint: str = "") -> str:
        return self._get_endpoint_url("/api" + endpoint)

    def _get_session(self) -> ClientSession:
        if self._session is None:
            raise RuntimeError(
                "Use ArtemisSession only in a 'async with' statement (Context Manager)"
            )

        return self._session
