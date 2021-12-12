from aiohttp.client_reqrep import ClientResponse
from artemis_client.api import UserDTO
from aiohttp.client_exceptions import ClientResponseError

from artemis_client.utils.serialize import loads

from .manager import ArtemisManager


class AccountManager(ArtemisManager):
    """ This class describes an account manager for the current session's account.
    """
    async def is_authenticated(self) -> bool:
        try:
            resp = await self._session.get_api_endpoint("/authenticate")
            return resp.ok
        except ClientResponseError:
            return False

    async def get_account(self) -> UserDTO:
        resp = await self._session.get_api_endpoint("/account")
        jdict = await resp.json(loads=loads)
        return jdict

    async def update_account(self, user: UserDTO) -> ClientResponse:
        return await self._session.put_api_endpoint("/account", json=user)
