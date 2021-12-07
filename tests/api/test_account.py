import pytest
from typeguard import check_type

from artemis_client.api.account import get_account, is_authenticated
from artemis_client.artemis_api import UserDTO, UserDTORequired


@pytest.mark.asyncio
async def test_is_authenticated(artemis_session):
    assert await is_authenticated(artemis_session)


@pytest.mark.asyncio
async def test_account(artemis_session):
    account: UserDTO = await get_account(artemis_session)
    check_type("account", account, UserDTORequired)
    check_type("account", account, UserDTO)
    assert account["activated"] == True
    assert "ROLE_ADMIN" in account["authorities"]
