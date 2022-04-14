from aiohttp import ClientSession
from typing import Optional
import logging

from aiohttp.client_reqrep import ClientResponse
from aiohttp.client_exceptions import ClientResponseError

from artemis_client.api import LoginVM
from artemis_client.utils.serialize import dumps
from artemis_client.utils.url import sanitize_url
from .configuration import get_value

AUTHORIZATION_HEADER = "authorization"
MAX_LOGIN_TRIES = 10


class ArtemisSession:
    """This class describes an session with the Artemis REST API.

    Stores credentials and reuses TCP connections.

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
        self.submission = artemis_client.managers.SubmissionManager(self)
        """See :class:`~artemis_client.managers.SubmissionManager`"""
        self.assessment = artemis_client.managers.AssessmentManager(self)
        """See :class:`~artemis_client.managers.AssessmentManager`"""
        self.result = artemis_client.managers.ResultManager(self)
        """See :class:`~artemis_client.managers.ResultManager`"""

    ###################################

    async def __aenter__(self, *_):
        self._session = ClientSession(self._url, raise_for_status=True, json_serialize=dumps)
        if self._token is not None:
            self._get_session().headers[AUTHORIZATION_HEADER] = self._token
        return self

    async def __aexit__(self, *_):
        await self._get_session().close()
        self._session = None

    ###################################

    # Query Artemis endpoints

    async def get_endpoint(self, endpoint: str, **kwargs) -> ClientResponse:
        return await self._request_endpoint("get", endpoint, **kwargs)

    async def post_endpoint(self, endpoint: str, **kwargs) -> ClientResponse:
        return await self._request_endpoint("post", endpoint, **kwargs)

    async def put_endpoint(self, endpoint: str, **kwargs) -> ClientResponse:
        return await self._request_endpoint("put", endpoint, **kwargs)

    async def delete_endpoint(self, endpoint: str, **kwargs) -> ClientResponse:
        return await self._request_endpoint("delete", endpoint, **kwargs)

    async def head_endpoint(self, endpoint: str, **kwargs) -> ClientResponse:
        return await self._request_endpoint("head", endpoint, **kwargs)

    async def options_endpoint(self, endpoint: str, **kwargs) -> ClientResponse:
        return await self._request_endpoint("options", endpoint, **kwargs)

    async def patch_endpoint(self, endpoint: str, **kwargs) -> ClientResponse:
        return await self._request_endpoint("patch", endpoint, **kwargs)

    # Query Artemis /api endpoints

    async def get_api_endpoint(self, api_endpoint: str, **kwargs) -> ClientResponse:
        return await self._request_api_endpoint("get", api_endpoint, **kwargs)

    async def post_api_endpoint(self, api_endpoint: str, **kwargs) -> ClientResponse:
        return await self._request_api_endpoint("post", api_endpoint, **kwargs)

    async def put_api_endpoint(self, api_endpoint: str, **kwargs) -> ClientResponse:
        return await self._request_api_endpoint("put", api_endpoint, **kwargs)

    async def delete_api_endpoint(self, api_endpoint: str, **kwargs) -> ClientResponse:
        return await self._request_api_endpoint("delete", api_endpoint, **kwargs)

    async def head_api_endpoint(self, api_endpoint: str, **kwargs) -> ClientResponse:
        return await self._request_api_endpoint("head", api_endpoint, **kwargs)

    async def options_api_endpoint(self, api_endpoint: str, **kwargs) -> ClientResponse:
        return await self._request_api_endpoint("options", api_endpoint, **kwargs)

    async def patch_api_endpoint(self, api_endpoint: str, **kwargs) -> ClientResponse:
        return await self._request_api_endpoint("patch", api_endpoint, **kwargs)

    ###################################

    def get_username(self) -> str:
        return self._login_vm["username"]

    ###################################

    def _get_endpoint_url(self, endpoint: str) -> str:
        return endpoint

    def _get_session(self) -> ClientSession:
        if self._session is None:
            raise RuntimeError(
                "Use ArtemisSession only in a 'async with' statement (Context Manager)"
            )

        return self._session

    async def _login(self) -> str:
        # Do not use _request_* to not catch 401 ClientResponseError
        resp = await self._get_session().post(self._get_endpoint_url("/api/authenticate"), json=self._login_vm)
        if resp.ok:
            logging.debug(f"logged in to {self._url}")
            return resp.headers[AUTHORIZATION_HEADER]
        else:
            raise ConnectionError(f"could not login to {self._url}")

    async def _request_endpoint(self, method: str, endpoint: str, tries=0, **kwargs) -> ClientResponse:
        try:
            return await self._get_session().request(method, self._get_endpoint_url(endpoint), **kwargs)
        except ClientResponseError as e:
            if e.status == 401 and tries < MAX_LOGIN_TRIES:
                # Attempt to log in
                self._token = await self._login()
                self._get_session().headers[AUTHORIZATION_HEADER] = self._token
                # Try again
                return await self._request_endpoint(method, endpoint, tries + 1, **kwargs)
            else:
                raise e

    async def _request_api_endpoint(self, method: str, api_endpoint: str, **kwargs) -> ClientResponse:
        return await self._request_endpoint(method, "/api" + api_endpoint, **kwargs)
