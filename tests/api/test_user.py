from typing import List
import pytest

from typeguard import check_type
from artemis_client.api import (
    ManagedUserVM,
    Role,
    SearchUserDTO,
    UserDTO,
)

from artemis_client.session import ArtemisSession


@pytest.mark.asyncio
async def get_authorities(artemis_session: ArtemisSession):
    roles = await artemis_session.user.get_authorities()
    check_type("roles", roles, List[Role])
    assert "ROLE_ADMIN" in roles


@pytest.mark.asyncio
async def test_get_user(artemis_session: ArtemisSession):
    user = await artemis_session.user.get_user(artemis_session.get_username())
    assert user
    check_type("user", user, UserDTO)
    assert user["login"] == artemis_session.get_username()


@pytest.mark.asyncio
async def test_create_delete_user(artemis_session: ArtemisSession):
    assert not await artemis_session.user.get_user("testuser_hda783")

    test_user: ManagedUserVM = {
        "login": "testuser_hda783",
        "firstName": "Test",
        "lastName": "User",
        "authorities": ["ROLE_USER"],
        "email": "testuser@test.test",
        "password": "testpw123",
        "imageUrl": "",
        "visibleRegistrationNumber": ""
    }
    resp = await artemis_session.user.create_user(test_user)
    assert resp.ok

    assert await artemis_session.user.get_user("testuser_hda783")
    await artemis_session.user.delete_user("testuser_hda783")
    assert not await artemis_session.user.get_user("testuser_hda783")


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
