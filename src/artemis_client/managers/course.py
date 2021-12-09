from typing import AsyncGenerator, Optional
from artemis_client.api import Course, CourseWithStats
from artemis_client.managers.manager import ArtemisManager


class CourseManager(ArtemisManager):

    async def get_courses(self, only_active=False) -> AsyncGenerator[Course, None]:
        params = {
            "onlyActive": "true" if only_active else "false"
        }
        resp = await self._session.get_api_endpoint("/courses", params=params)
        courses = await resp.json()

        for course in courses:
            yield course

    async def get_courses_with_stats(self, only_active=False) -> AsyncGenerator[CourseWithStats, None]:
        params = {
            "onlyActive": "true" if only_active else "false"
        }
        resp = await self._session.get_api_endpoint("/courses/with-user-stats", params=params)
        courses = await resp.json()

        for course in courses:
            yield course

    async def get_course(self, id: int) -> Optional[CourseWithStats]:
        resp = await self._session.get_api_endpoint("/courses/" + str(id))
        if not resp.ok:
            return None
        return await resp.json()
