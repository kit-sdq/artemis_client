import pytest
from aiohttp.client_exceptions import ClientResponseError
from artemis_client.api import UserDTO
from artemis_client.session import ArtemisSession
from typeguard import check_type


@pytest.mark.asyncio
async def test_account(artemis_session: ArtemisSession):
    account: UserDTO = await artemis_session.account.get_account()
    check_type("UserDTO", account, UserDTO)
    assert "activated" in account and account["activated"] is True
    assert "authorities" in account and "ROLE_ADMIN" in account["authorities"]


@pytest.mark.asyncio
async def test_update_account(artemis_session: ArtemisSession):
    account: UserDTO = await artemis_session.account.get_account()
    assert("firstName" in account)
    old_name = account["firstName"]
    account["firstName"] = "test"
    try:
        await artemis_session.account.update_account(account)
        # exception may occur here
        updated_account: UserDTO = await artemis_session.account.get_account()
        assert updated_account["firstName"] == account["firstName"]

        account["firstName"] = old_name
        updated_account: UserDTO = await artemis_session.account.get_account()
        assert updated_account["firstName"] == old_name
    except ClientResponseError as e:
        assert e.status == 403
        pytest.skip("User Registration is disabled")
