from typing import AsyncGenerator
from aiohttp.client_reqrep import ClientResponse
from artemis_client.api import ManagedUserVM, UserDTO
from artemis_client.managers.manager import ArtemisManager
from artemis_client.utils.paginate import paginate_json


class UserManager(ArtemisManager):
    """This manager allows creating, updating, deleting users.
    Admin role is required in the current session.
    """

    async def create_user(self, user: ManagedUserVM) -> ClientResponse:
        """Creates an user.

        Parameters
        ----------
        user : ManagedUserVM
            The user

        Returns
        -------
        ClientResponse
            201 if the user was created
            400 if login or mail exist already
        """
        if not 8 <= len(user["password"]) <= 50:
            raise ValueError("Password has invalid length")

        return await self._session.post_api_endpoint("/users", json=user)

    async def update_user(self, user: ManagedUserVM):
        """Creates an user.

        Parameters
        ----------
        user : ManagedUserVM
            The user

        Returns
        -------
        ClientResponse
            201 if the user was created
            400 if login or mail exist already
        """
        if not 8 <= len(user["password"]) <= 50:
            raise ValueError("Password has invalid length")

        return await self._session.put_api_endpoint("/users", json=user)

    async def get_users(
        self, search_term: str = "", page_size: int = 50, sorting_order="ASCENDING", sorted_column: str = "id"
    ) -> AsyncGenerator[UserDTO, None]:
        params = {
            "searchTerm": search_term,
            "sortingOrder": sorting_order,
            "sortedColumn": sorted_column
        }

        async for obj in paginate_json(self._session.get_api_endpoint, "/users", params, page_size=page_size):
            yield obj
