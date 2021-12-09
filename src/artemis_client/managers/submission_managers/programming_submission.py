from aiohttp.client_reqrep import ClientResponse
from artemis_client.api import Participation, SubmissionType
from artemis_client.managers import ArtemisManager


class ProgrammingSubmissionManager(ArtemisManager):
    async def trigger_build(
        self, participation: Participation, submission_type: SubmissionType
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
