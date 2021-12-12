from artemis_client.utils.serialize import deserialize_datetime
from .manager import ArtemisManager


class TimeManager(ArtemisManager):
    """ This manager queries the /time endpoint of Artemis.
    """
    async def time(self):
        resp = await self._session.get_endpoint("/time")
        text: str = await resp.text()
        return deserialize_datetime(text[1:-1])
