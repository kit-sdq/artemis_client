from typing import AsyncGenerator
import aiohttp
from aiohttp import JsonPayload, MultipartWriter

from aiohttp.client_reqrep import ClientResponse
from multidict import CIMultiDict
from artemis_client.api import Course, CourseWithExercises, CourseWithStats, Exercise, User
from artemis_client.managers.manager import ArtemisManager
from artemis_client.utils.serialize import dumps, loads


class CourseManager(ArtemisManager):

    async def create_course(self, course: Course) -> Course:
        new_course = course
        new_course["id"] = None  # type: ignore
        with MultipartWriter("form-data") as mpwriter:
            part = mpwriter.append_payload(JsonPayload(course, headers=CIMultiDict(), dumps=dumps))
            part.set_content_disposition("form-data", name="course", filename="blob")
            part.headers.pop(aiohttp.hdrs.CONTENT_LENGTH, None)
            resp = await self._session.post_api_endpoint("/admin/courses", data=mpwriter)
            return await resp.json(loads=loads)

    async def update_course(self, course: Course) -> ClientResponse:
        return await self._session.put_api_endpoint("/courses", json=course)

    async def get_courses(self, only_active=False) -> AsyncGenerator[Course, None]:
        params = {
            "onlyActive": "true" if only_active else "false"
        }
        resp = await self._session.get_api_endpoint("/courses", params=params)
        courses = await resp.json(loads=loads)

        for course in courses:
            yield course

    async def get_courses_with_stats(self, only_active=False) -> AsyncGenerator[CourseWithStats, None]:
        params = {
            "onlyActive": "true" if only_active else "false"
        }
        resp = await self._session.get_api_endpoint("/courses/with-user-stats", params=params)
        courses = await resp.json(loads=loads)

        for course in courses:
            yield course

    async def get_course(self, id: int) -> CourseWithStats:
        resp = await self._session.get_api_endpoint("/courses/" + str(id))
        return await resp.json(loads=loads)

    async def get_course_with_exercises(self, id: int) -> CourseWithExercises:
        resp = await self._session.get_api_endpoint("/courses/" + str(id) + "/with-exercises")
        return await resp.json(loads=loads)

    async def get_exercises_for_course(self, course_id: int) -> AsyncGenerator[Exercise, None]:
        course = await self.get_course_with_exercises(course_id)
        if course and "exercises" in course:
            for exercise in course["exercises"]:
                yield exercise

    async def delete_course(self, course_id: int) -> ClientResponse:
        return await self._session.delete_api_endpoint(f"/admin/courses/{course_id}")

    async def archive_course(self, course_id: int) -> ClientResponse:
        return await self._session.put_api_endpoint(f"/courses/{course_id}/archive")

    async def _get_users_in_course(self, id: int, api_user_type: str):
        resp = await self._session.get_api_endpoint("/courses/" + str(id) + "/" + api_user_type)
        users = await resp.json(loads=loads)
        for user in users:
            yield user

    async def get_students_in_course(self, id: int) -> AsyncGenerator[User, None]:
        async for u in self._get_users_in_course(id, "students"):
            yield u

    async def get_tutors_in_course(self, id: int) -> AsyncGenerator[User, None]:
        async for u in self._get_users_in_course(id, "tutors"):
            yield u

    async def get_editors_in_course(self, id: int) -> AsyncGenerator[User, None]:
        async for u in self._get_users_in_course(id, "editors"):
            yield u

    async def get_instructors_in_course(self, id: int) -> AsyncGenerator[User, None]:
        async for u in self._get_users_in_course(id, "instructors"):
            yield u
