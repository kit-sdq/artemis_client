from typing import AsyncGenerator
from artemis_client.api import Exam, ExerciseGroup
from artemis_client.managers.manager import ArtemisManager


class ExamManager(ArtemisManager):

    async def get_exams(self, course_id: int) -> AsyncGenerator[Exam, None]:
        resp = await self._session.get_api_endpoint(f"/courses/{course_id}/exams")
        exams = await resp.json()
        for exam in exams:
            yield exam

    async def get_exam_with_exercise_groups_and_exercises(self, course_id: int, exam_id: int) -> Exam:
        resp = await self._session.get_api_endpoint(f"/courses/{course_id}/exams/{exam_id}/exam-for-assessment-dashboard")
        return await resp.json()

    async def get_exercise_groups(self, course_id: int, exam_id: int) -> AsyncGenerator[ExerciseGroup, None]:

        pass
