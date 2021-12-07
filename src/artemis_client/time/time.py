from datetime import datetime
from artemis_client.artemis_session import ArtemisSession


async def time(session: ArtemisSession):
    resp = await session.get_endpoint("/time")
    text: str = await resp.text()
    text = text[1:text.rindex(".")]

    return datetime.strptime(text, "%Y-%m-%dT%H:%M:%S")
