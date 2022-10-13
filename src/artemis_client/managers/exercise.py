from typing import AsyncGenerator, List
from artemis_client.api import ProgrammingExercise, StudentParticipation
from artemis_client.managers.manager import ArtemisManager
from artemis_client.utils.serialize import loads


class ExerciseManager(ArtemisManager):

    async def get_participations(self, exercise_id: int, with_latest_results: bool = True) -> AsyncGenerator[StudentParticipation, None]:
        params = {
            "withLatestResult": "true" if with_latest_results else "false"
        }
        resp = await self._session.get_api_endpoint(f"/exercises/{exercise_id}/participations", params=params)
        participations: List[StudentParticipation] = await resp.json(loads=loads)
        for participation in participations:
            yield participation

    async def get_with_template_and_solution(self, exercise_id: int, with_submission_results: bool = False) -> ProgrammingExercise:
        """
        Returns the exercise including the template and solution participation.

        :param      exercise_id:  The exercise id.
        :type       exercise_id:  int
        """
        params = {
            "withSubmissionResults": str(with_submission_results).lower()
        }
        resp = await self._session.get_api_endpoint(f"/programming-exercises/{exercise_id}/with-template-and-solution-participation", params=params)
        return await resp.json(loads=loads)
