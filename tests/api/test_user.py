from typing import List

import pytest
from aiohttp.client_exceptions import ClientResponseError
from artemis_client.api import (
    ManagedUserVM,
    Role,
    SearchUserDTO,
    UserDTO,
)
from artemis_client.session import ArtemisSession
from typeguard import check_type


@pytest.mark.asyncio
async def get_authorities(artemis_session: ArtemisSession):
    roles = await artemis_session.user.get_authorities()
    check_type("List[Role]", roles, List[Role])
    assert "ROLE_ADMIN" in roles


@pytest.mark.asyncio
async def test_get_user(artemis_session: ArtemisSession):
    user = await artemis_session.user.get_user(artemis_session.get_username())
    assert user
    check_type("UserDTO", user, UserDTO)
    assert "login" in user and user["login"] == artemis_session.get_username()


@pytest.mark.asyncio
async def test_create_delete_user(artemis_session: ArtemisSession):
    with pytest.raises(ClientResponseError):  # 404 not found
        await artemis_session.user.get_user("testuser_hda783")

    test_user: ManagedUserVM = {
        "login": "testuser_hda783",
        "firstName": "Test",
        "lastName": "User",
        "authorities": ["ROLE_USER"],
        "email": "testuser@test.test",
        "password": "testpw123",
        "imageUrl": "",
        "visibleRegistrationNumber": "",
        "groups": []
    }
    error = None
    try:
        await artemis_session.user.create_user(test_user)
    except ClientResponseError as e:
        error = e

    assert await artemis_session.user.get_user("testuser_hda783")

    await artemis_session.user.delete_user("testuser_hda783")

    with pytest.raises(ClientResponseError):
        await artemis_session.user.get_user("testuser_hda783")

    if error:
        pytest.fail(f"create_user returned {error.status} but user existed anyways")


@pytest.mark.asyncio
async def test_get_users(artemis_session: ArtemisSession):
    async for user in artemis_session.user.get_users():
        check_type("UserDTO", user, UserDTO)
        if "login" in user and user["login"] == artemis_session.get_username():
            break
    else:
        pytest.fail()


@pytest.mark.asyncio
async def test_search_users(artemis_session: ArtemisSession):
    async for user in artemis_session.user.search_users(artemis_session.get_username()):
        check_type("SearchUserDTO", user, SearchUserDTO)
        if user["login"] == artemis_session.get_username():
            break
    else:
        pytest.fail()


@pytest.mark.asyncio
async def test_search_users_missing(artemis_session: ArtemisSession):
    async for _ in artemis_session.user.search_users("someRandomStringThatIsNotAUser"):
        pytest.fail()
