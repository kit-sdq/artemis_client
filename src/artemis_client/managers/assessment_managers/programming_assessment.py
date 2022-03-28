from aiohttp.client_reqrep import ClientResponse
from artemis_client.managers.manager import ArtemisManager
from artemis_client.api import Result


class ProgrammingAssessmentManager(ArtemisManager):
    async def save_assessment(
        self, participation_id: int, result: Result, submit: bool = False
    ) -> ClientResponse:
        """
        Saves or submittes an assessment.

        :param      participation_id:  The participation identifier
        :type       participation_id:  int
        :param      result:            The result
        :type       result:            Result
        :param      submit:            Set to true to submit, false to save the assesment. Submit to remove the lock.
        :type       submit:            bool

        :returns:   The client response.
        :rtype:     ClientResponse
        """
        params = {"submit": submit}
        return await self._session.put_api_endpoint(
            f"/participations/{participation_id}/manual-results",
            json=result,
            params=params,
        )

    async def delete_assessment(
        self, participation_id: int, submission_id: int, result_id: int
    ) -> ClientResponse:
        """
        Delete an assessment of a given submission.

        :param      participation_id:  The participation identifier
        :type       participation_id:  int
        :param      submission_id:     The submission identifier
        :type       submission_id:     int
        :param      result_id:         The result identifier
        :type       result_id:         int

        :returns:   The client response.
        :rtype:     ClientResponse
        """
        return await self._session.delete_api_endpoint(
            f"/participations/{participation_id}/programming-submissions/{submission_id}/results/{result_id}"
        )

    async def cancel_assessment(self, submission_id: int) -> ClientResponse:
        """
        Cancel an assessment of a given submission for the current user, i.e. delete the corresponding result / release the lock. Then the submission is available for assessment again.

        :param      submission_id:  The submission identifier
        :type       submission_id:  int

        :returns:   The client response.
        :rtype:     ClientResponse
        """
        return await self._session.put_api_endpoint(
            f"/programming-submissions/{submission_id}/cancel-assessment"
        )
