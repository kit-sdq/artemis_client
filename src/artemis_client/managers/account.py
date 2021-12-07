from artemis_client.api import UserDTO

from .manager import ArtemisManager


class AccountManager(ArtemisManager):

    async def is_authenticated(self) -> bool:
        resp = await self._session.get_api_endpoint("/authenticate")
        return resp.ok

    async def get_account(self) -> UserDTO:
        resp = await self._session.get_api_endpoint("/account")
        jdict = await resp.json()
        return jdict
