from artemis_client.artemis_session import ArtemisSession


async def isAuthenticated(session: ArtemisSession) -> bool:
    resp = await session.get_api_endpoint("/authenticate")
    return resp.ok
