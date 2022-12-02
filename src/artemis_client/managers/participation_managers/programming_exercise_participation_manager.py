from artemis_client.api import Result
from artemis_client.managers.manager import ArtemisManager
from artemis_client.utils.serialize import loads


class ProgrammingExerciseParticipationManager(ArtemisManager):

    async def get_latest_result_with_feedback(self, participation_id: int) -> Result:
        resp = await self._session.get_api_endpoint(f"/programming-exercise-participations/{participation_id}/latest-result-with-feedbacks")
        return await resp.json(loads=loads)
