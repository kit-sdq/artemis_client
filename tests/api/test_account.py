import pytest
from typeguard import check_type

from artemis_client.api import UserDTO, UserDTORequired
from artemis_client.session import ArtemisSession


@pytest.mark.asyncio
async def test_is_authenticated(artemis_session: ArtemisSession):
    assert await artemis_session.account.is_authenticated()


@pytest.mark.asyncio
async def test_account(artemis_session: ArtemisSession):
    account: UserDTO = await artemis_session.account.get_account()
    check_type("account", account, UserDTORequired)
    check_type("account", account, UserDTO)
    assert account["activated"] is True
    assert "ROLE_ADMIN" in account["authorities"]


@pytest.mark.asyncio
async def test_update_account(artemis_session: ArtemisSession):
    account: UserDTO = await artemis_session.account.get_account()
    old_name = account["firstName"]
    account["firstName"] = "test"

    resp = await artemis_session.account.update_account(account)
    assert resp.ok or "User Registration is disabled" in (await resp.text())

    if resp.ok:
        updated_account: UserDTO = await artemis_session.account.get_account()
        assert updated_account["firstName"] == account["firstName"]

        account["firstName"] = old_name
        updated_account: UserDTO = await artemis_session.account.get_account()
        assert updated_account["firstName"] == old_name
