from aiohttp.client_reqrep import ClientResponse
from artemis_client.managers.manager import ArtemisManager
from artemis_client.api import Result


class ProgrammingAssessmentManager(ArtemisManager):
    async def save_assessment(
        self, participation_id: int, result: Result, submit: bool = False
    ) -> ClientResponse:
        params = {"submit": submit}
        return await self._session.put_api_endpoint(
            f"/participations/{participation_id}/manual-results",
            json=result,
            params=params,
        )
