from artemis_client.managers.manager import ArtemisManager

from artemis_client.api import Feedback, Result
from artemis_client.utils.serialize import loads

from typing import List


class ResultManager(ArtemisManager):

    async def latest_result_with_feedback(self, participation_id: int) -> Result:
        resp = await self._session.get_api_endpoint(f"/participations/{participation_id}/latest-result")
        return await resp.json(loads=loads)

    async def result_details(self, result: Result, participation_id: int) -> List[Feedback]:
        resp = await self._session.get_api_endpoint(f"participations/{participation_id}/results/{result['id']}/details")
        return await resp.json(loads=loads)
