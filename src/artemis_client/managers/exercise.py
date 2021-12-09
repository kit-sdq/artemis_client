from typing import AsyncGenerator
from artemis_client.api import Exercise
from artemis_client.managers.manager import ArtemisManager


class ExerciseManager(ArtemisManager):

    async def get_exercises_for_course(self, course_id: int) -> AsyncGenerator[Exercise, None]:
        course = await self._session.course.get_course_with_exercises(course_id)
        if not course or "exercises" not in course:
            raise StopAsyncIteration
        for exercise in course["exercises"]:
            yield exercise
