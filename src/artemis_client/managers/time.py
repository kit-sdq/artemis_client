from datetime import datetime
from .manager import ArtemisManager


class TimeManager(ArtemisManager):
    """ This manager queries the /time endpoint of Artemis.
    """
    async def time(self):
        resp = await self._session.get_endpoint("/time")
        text: str = await resp.text()
        text = text[1:text.rindex(".")]

        return datetime.strptime(text, "%Y-%m-%dT%H:%M:%S")
