from typing import List, AsyncGenerator
from aiohttp.client_reqrep import ClientResponse
from artemis_client.api import Participation, ProgrammingSubmission, SubmissionType
from artemis_client.managers import ArtemisManager
from artemis_client.utils.serialize import loads


class ProgrammingSubmissionManager(ArtemisManager):
    async def trigger_build(
        self, participation: Participation, submission_type: SubmissionType = "MANUAL"
    ) -> ClientResponse:
        if "id" not in participation:
            raise ValueError("id is missing in participation!")
        if "type" not in participation:
            raise ValueError("type is missing in participation!")
        if participation["type"] != "programming":
            raise ValueError("only programming participations are supported!")

        params = {"submissionType": submission_type}

        return await self._session.post_api_endpoint(
            f"/programming-submissions/{participation['id']}/trigger-build",
            params=params,
        )

    async def get_submissions(
        self,
        exercise_id: int,
        filter_submitted_only: bool = False,
        filter_assessed_by_tutor: bool = False,
        correction_round: int = 0,
    ) -> AsyncGenerator[ProgrammingSubmission, None]:
        params = {
            "submittedOnly": str(filter_submitted_only).lower(),
            "assessedByTutor": str(filter_assessed_by_tutor).lower(),
            "correction-round": str(correction_round),
        }
        resp = await self._session.get_api_endpoint(
            f"/exercises/{exercise_id}/programming-submissions",
            params=params
        )
        jdict: List[ProgrammingSubmission] = await resp.json(loads=loads)
        for submission in jdict:
            yield submission

    async def lock_and_get_submission(
        self, submission_id: int, correction_round: int = 0
    ) -> ProgrammingSubmission:
        """
        Locks the submission for assessment and gets the submission.

        :param      submission_id:     The submission identifier
        :type       submission_id:     int
        :param      correction_round:  The correction round, defaults to 0
        :type       correction_round:  int
        """
        params = {"correction-round": str(correction_round)}
        resp = await self._session.get_api_endpoint(
            f"/programming-submissions/{submission_id}/lock", params=params
        )
        jdict = await resp.json(loads=loads)
        return jdict
