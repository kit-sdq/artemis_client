from typing import AsyncGenerator

from aiohttp.client_reqrep import ClientResponse
from artemis_client.api import Course, CourseWithExercises, CourseWithStats, Exercise, User
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

    async def get_course(self, id: int) -> CourseWithStats:
        resp = await self._session.get_api_endpoint("/courses/" + str(id))
        return await resp.json()

    async def get_course_with_exercises(self, id: int) -> CourseWithExercises:
        resp = await self._session.get_api_endpoint("/courses/" + str(id) + "/with-exercises")
        return await resp.json()

    async def get_exercises_for_course(self, course_id: int) -> AsyncGenerator[Exercise, None]:
        course = await self.get_course_with_exercises(course_id)
        if not course or "exercises" not in course:
            raise StopAsyncIteration
        for exercise in course["exercises"]:
            yield exercise

    async def delete_course(self, id: int) -> ClientResponse:
        return await self._session.delete_api_endpoint("/courses/" + str(id))

    async def archive_course(self, id: int) -> ClientResponse:
        return await self._session.put_api_endpoint("/courses/" + str(id) + "/archive")

    async def _get_users_in_course(self, id: int, api_user_type: str):
        resp = await self._session.get_api_endpoint("/courses/" + str(id) + "/" + api_user_type)
        users = await resp.json()
        for user in users:
            yield user

    async def get_students_in_course(self, id: int) -> AsyncGenerator[User, None]:
        return self._get_users_in_course(id, "students")

    async def get_tutors_in_course(self, id: int) -> AsyncGenerator[User, None]:
        return self._get_users_in_course(id, "tutors")

    async def get_editors_in_course(self, id: int) -> AsyncGenerator[User, None]:
        return self._get_users_in_course(id, "editors")

    async def get_instructors_in_course(self, id: int) -> AsyncGenerator[User, None]:
        return self._get_users_in_course(id, "instructors")
