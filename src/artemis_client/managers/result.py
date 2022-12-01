from artemis_client.managers.manager import ArtemisManager

from artemis_client.api import Feedback
from artemis_client.utils.serialize import loads

from typing import List


class ResultManager(ArtemisManager):

    async def result_details(self, result_id: int, participation_id: int) -> List[Feedback]:
        resp = await self._session.get_api_endpoint(f"/participations/{participation_id}/results/{result_id}/details")
        return await resp.json(loads=loads)
