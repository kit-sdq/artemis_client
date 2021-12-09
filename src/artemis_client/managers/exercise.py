from typing import AsyncGenerator
from artemis_client.api import StudentParticipation
from artemis_client.managers.manager import ArtemisManager


class ExerciseManager(ArtemisManager):

    async def get_participations(self, exercise_id: int, with_latest_results: bool = True) -> AsyncGenerator[StudentParticipation, None]:
        params = {
            "withLatestResult": with_latest_results
        }
        resp = await self._session.get_api_endpoint(f"/exercises/{exercise_id}/participations", params=params)
        participations = await resp.json()
        for participation in participations:
            yield participation
