from aiohttp import ClientSession
from typing import Optional
import logging

from aiohttp.client_reqrep import ClientResponse

from artemis_client.api import LoginVM
from artemis_client.utils.url import sanitize_url
from .configuration import get_value

AUTHORIZATION_HEADER = "authorization"


class ArtemisSession:
    """This class describes an session with the Artemis REST API.

    Stores credentials and reuse TCP connections.

    This class is based of aiohttp.ClienSession().
    All API methods allow supplying kwargs controlling the underlaying
    ClientSession method. When an API call failes an exception is raised.
    """

    _session: Optional[ClientSession] = None
    _token: Optional[str] = None

    def __init__(self, url: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None) -> None:
        self._login_vm: LoginVM = {
            "username": username or get_value("ARTEMIS", "USERNAME"),
            "password": password or get_value("ARTEMIS", "PASSWORD"),
            "rememberMe": False,
        }
        self._url: str = sanitize_url(url or get_value("ARTEMIS", "URL"))

        # Must be imported here to prevent circular import error!
        import artemis_client.managers
        self.account = artemis_client.managers.AccountManager(self)
        """See :class:`~artemis_client.managers.AccountManager`"""
        self.time = artemis_client.managers.TimeManager(self)
        """See :class:`~artemis_client.managers.TimeManager`"""
        self.user = artemis_client.managers.UserManager(self)
        """See :class:`~artemis_client.managers.UserManager`"""
        self.course = artemis_client.managers.CourseManager(self)
        """See :class:`~artemis_client.managers.CourseManager`"""
        self.exam = artemis_client.managers.ExamManager(self)
        """See :class:`~artemis_client.managers.ExamManager`"""
        self.exercise = artemis_client.managers.ExerciseManager(self)
        """See :class:`~artemis_client.managers.ExerciseManager`"""

    async def __aenter__(self, *_):
        self._session = ClientSession(self._url, raise_for_status=True)
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

    async def get_endpoint(self, endpoint: str, **kwargs) -> ClientResponse:
        return await self._get_session().get(
            self._get_endpoint_url(endpoint), **kwargs
        )

    async def post_endpoint(self, endpoint: str, **kwargs) -> ClientResponse:
        return await self._get_session().post(
            self._get_endpoint_url(endpoint), **kwargs
        )

    async def put_endpoint(self, endpoint: str, **kwargs) -> ClientResponse:
        return await self._get_session().put(
            self._get_endpoint_url(endpoint), **kwargs
        )

    async def delete_endpoint(self, endpoint: str, **kwargs) -> ClientResponse:
        return await self._get_session().delete(
            self._get_endpoint_url(endpoint), **kwargs
        )

    async def head_endpoint(self, endpoint: str, **kwargs) -> ClientResponse:
        return await self._get_session().head(
            self._get_endpoint_url(endpoint), **kwargs
        )

    async def options_endpoint(self, endpoint: str, **kwargs) -> ClientResponse:
        return await self._get_session().options(
            self._get_endpoint_url(endpoint), **kwargs
        )

    async def patch_endpoint(self, endpoint: str, **kwargs) -> ClientResponse:
        return await self._get_session().patch(
            self._get_endpoint_url(endpoint), **kwargs
        )

    # Query Artemis /api endpoints

    async def get_api_endpoint(self, api_endpoint: str, **kwargs) -> ClientResponse:
        return await self._get_session().get(
            self._get_api_endpoint_url(api_endpoint), **kwargs
        )

    async def post_api_endpoint(self, api_endpoint: str, **kwargs) -> ClientResponse:
        return await self._get_session().post(
            self._get_api_endpoint_url(api_endpoint), **kwargs
        )

    async def put_api_endpoint(self, api_endpoint: str, **kwargs) -> ClientResponse:
        return await self._get_session().put(
            self._get_api_endpoint_url(api_endpoint), **kwargs
        )

    async def delete_api_endpoint(self, api_endpoint: str, **kwargs) -> ClientResponse:
        return await self._get_session().delete(
            self._get_api_endpoint_url(api_endpoint), **kwargs
        )

    async def head_api_endpoint(self, api_endpoint: str, **kwargs) -> ClientResponse:
        return await self._get_session().head(
            self._get_api_endpoint_url(api_endpoint), **kwargs
        )

    async def options_api_endpoint(self, api_endpoint: str, **kwargs) -> ClientResponse:
        return await self._get_session().options(
            self._get_api_endpoint_url(api_endpoint), **kwargs
        )

    async def patch_api_endpoint(self, api_endpoint: str, **kwargs) -> ClientResponse:
        return await self._get_session().patch(
            self._get_api_endpoint_url(api_endpoint), **kwargs
        )

    ###################################

    def get_username(self) -> str:
        return self._login_vm["username"]

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
