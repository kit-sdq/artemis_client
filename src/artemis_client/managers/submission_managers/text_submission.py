from typing import AsyncGenerator
from artemis_client.api import TextSubmission
from artemis_client.managers import ArtemisManager
from artemis_client.utils.serialize import loads

class TextSubmissionManager(ArtemisManager):
    async def get_submissions(
        self,
        exercise_id: int,
        filter_submitted_only: bool = False,
        filter_assessed_by_tutor: bool = False,
        correction_round: int = 0,
    ) -> AsyncGenerator[TextSubmission, None]:
        """
        Returns all text submissions of that exercise id.

        :param      exercise_id:                The exercise identifier
        :type       exercise_id:                int
        :param      filter_submitted_only:      Only return submitted submissions, defaults to False
        :type       filter_submitted_only:      bool
        :param      filter_assessed_by_tutor:   Only return submissions assessed by the tutor making the request, defaults to 0
        :type       filter_assessed_by_tutor:   bool
        :param      correction_round:           The correction round, defaults to 0
        :type       correction_round:           int
        """
        params = {
            "submittedOnly": str(filter_submitted_only).lower(),
            "assessedByTutor": str(filter_assessed_by_tutor).lower(),
            "correction-round": str(correction_round),
        }
        resp = await self._session.get_api_endpoint(
            f"/exercises/{exercise_id}/text-submissions",
            params=params
        )
        jdict: list[TextSubmission] = await resp.json(loads=loads)
        for submission in jdict:
            yield submission

    async def lock_and_get_submission(
        self, submission_id: int, correction_round: int = 0
    ) -> TextSubmission:
        """
        Locks the submission for assessment and gets the submission.
        :param      submission_id:     The submission identifier
        :type       submission_id:     int
        :param      correction_round:  The correction round, defaults to 0
        :type       correction_round:  int
        """
        params = {"correction-round": str(correction_round)}
        resp = await self._session.get_api_endpoint(
            f"/text-submissions/{submission_id}/lock", params=params
        )
        jdict = await resp.json(loads=loads)
        return jdict