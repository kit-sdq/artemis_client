from artemis_client.managers.manager import ArtemisManager
from artemis_client.api import TextSubmission, Participation, TextBlock, TextFeedback
from artemis_client.utils.serialize import loads

class TextAssessmentManager(ArtemisManager):
    async def next(self, exercise_id: int, head: bool = True) -> TextSubmission:
        """
        Returns the next submission without an assessment.

        :param      exercise_id:  The exercise identifier
        :type       exercise_id:  int
        :param      head:         defaults to True
        :type       head:         bool
        """
        params = {
            "head": str(head).lower()
        }

        resp = await self._session.get_api_endpoint(
            f"/exercises/{exercise_id}/text-submission-without-assessment",
            params=params
        )

        jdict = await resp.json(loads=loads)
        return jdict

    async def start(self, participation_id: int, submission_id: int, correction_round: int = 0) -> Participation:
        """
        Locks the submission for assessment.

        :param      participation_id:   The participation identifier
        :type       participation_id:   int
        :param      submission_id:      The submission identifier
        :type       submission_id:      int
        :param      correction_round:   The correction round, defaults to 0
        :type       correction_round:   int
        """

        params = {
            "correction-round": str(correction_round),
        }
        resp = await self._session.get_api_endpoint(
            f"/participations/{participation_id}/submissions/{submission_id}/for-text-assessment",
            params=params
        )
        jdict: Participation = await resp.json(loads=loads)
        return jdict

    async def cancel(self, participation_id: int, submission_id: int) -> None:
        """
        Remove the lock from the submission.

        :param      participation_id:   The participation identifier
        :type       participation_id:   int
        :param      submission_id:      The submission identifier
        :type       submission_id:      int
        """
        await self._session.post_api_endpoint(
            f"/participations/{participation_id}/submissions/{submission_id}/cancel-assessment"
        )

        # no response body

    async def submit(self, participation_id: int, result_id: int, feedbacks: list[TextFeedback], text_blocks: list[TextBlock]) -> None:
        """
        Submits an assessment with the provided feedbacks for the text blocks.

        :param      participation_id:   The participation identifier
        :type       participation_id:   int
        :param      result_id:          The result identifier
        :type       result_id:          int
        """

        await self._session.post_api_endpoint(
            f"/participations/{participation_id}/results/{result_id}/submit-text-assessment",
            json = {
                "feedbacks": feedbacks,
                "textBlocks": [i.to_dict() for i in text_blocks]
            }
        )
