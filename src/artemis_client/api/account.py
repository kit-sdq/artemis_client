from artemis_client.artemis_api import UserDTO
from artemis_client.artemis_session import ArtemisSession


async def is_authenticated(session: ArtemisSession) -> bool:
    resp = await session.get_api_endpoint("/authenticate")
    return resp.ok


async def get_account(session: ArtemisSession) -> UserDTO:
    resp = await session.get_api_endpoint("/account")
    jdict = await resp.json()
    return jdict
