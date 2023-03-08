from typing import AsyncGenerator, List
from aiohttp.client_reqrep import ClientResponse
from artemis_client.api import ManagedUserVM, Role, SearchUserDTO, SortingOrder, UserDTO, UserPageableSearchDTO
from artemis_client.managers.manager import ArtemisManager
from artemis_client.utils.paginate import paginate_json
from artemis_client.utils.serialize import loads


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

        return await self._session.post_api_endpoint("/admin/users", json=user)

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

        return await self._session.put_api_endpoint("/admin/users", json=user)

    async def get_authorities(self) -> List[Role]:
        resp = await self._session.get_api_endpoint("/admin/users/authorities")
        roles = await resp.json(loads=loads)
        return roles

    async def get_user(self, login: str) -> UserDTO:
        resp = await self._session.get_api_endpoint("/users/" + login)
        user = await resp.json(loads=loads)
        return user

    async def delete_user(self, login: str) -> ClientResponse:
        resp = await self._session.delete_api_endpoint("/admin/users/" + login)
        return resp

    async def get_users(
        self,
        search_term: str = "",
        page_size: int = 50,
        sorting_order: SortingOrder = "ASCENDING",
        sorted_column: str = "id",
    ) -> AsyncGenerator[UserDTO, None]:
        """Generates the users."""
        params: UserPageableSearchDTO = {
            "page": 0,
            "pageSize": page_size,
            "searchTerm": search_term,
            "sortingOrder": sorting_order,
            "sortedColumn": sorted_column,
            "authorities": "",
            "origins": "",
            "status": "",
            "courseIds": "",
            "registrationNumbers": ""
        }

        async for obj in paginate_json(
            self._session.get_api_endpoint, "/admin/users", params, page_size=page_size
        ):
            yield obj

    async def search_users(
        self, login_or_name: str
    ) -> AsyncGenerator[SearchUserDTO, None]:
        """Nearly the same as get_users.

        The API endpoint removes information from the object. Only INSTRUCTOR role is needed.
        """
        params = {
            "loginOrName": login_or_name,
        }

        # Artemis does not return a empty list, when querying for more pages
        async for obj in paginate_json(
            self._session.get_api_endpoint,
            "/users/search",
            params,
            page_size=25,
            max_pages=1,
        ):
            yield obj
