import pytest

from typeguard import check_type
from artemis_client.api import UserDTO

from artemis_client.session import ArtemisSession


@pytest.mark.asyncio
async def test_update_account(artemis_session: ArtemisSession):
    found = True
    async for user in artemis_session.user.get_users():
        check_type("user", user, UserDTO)
        if user["login"] == artemis_session.get_username():
            found = True
    assert found
