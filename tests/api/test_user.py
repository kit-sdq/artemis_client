import pytest

from typeguard import check_type
from artemis_client.api import (
    SearchUserDTO,
    UserDTO,
)

from artemis_client.session import ArtemisSession


@pytest.mark.asyncio
async def test_get_users(artemis_session: ArtemisSession):
    found = False
    async for user in artemis_session.user.get_users():
        check_type("user", user, UserDTO)
        if user["login"] == artemis_session.get_username():
            found = True
    assert found


@pytest.mark.asyncio
async def test_search_users(artemis_session: ArtemisSession):
    found = False
    async for user in artemis_session.user.search_users(artemis_session.get_username()):
        check_type("user", user, SearchUserDTO)
        if user["login"] == artemis_session.get_username():
            found = True
    assert found


@pytest.mark.asyncio
async def test_search_users_missing(artemis_session: ArtemisSession):
    found = False
    async for _ in artemis_session.user.search_users("someRandomStringThatIsNotAUser"):
        found = True
    assert not found
