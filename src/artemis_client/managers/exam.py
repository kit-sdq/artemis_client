from typing import AsyncGenerator, List
from artemis_client.api import Exam, ExerciseGroup, StudentExam
from artemis_client.managers.manager import ArtemisManager
from artemis_client.utils.serialize import loads


class ExamManager(ArtemisManager):
    async def get_exams(self, course_id: int) -> AsyncGenerator[Exam, None]:
        """
        Returns all exams for a course.
        """
        resp = await self._session.get_api_endpoint(f"/courses/{course_id}/exams")
        exams: List[Exam] = await resp.json(loads=loads)
        for exam in exams:
            yield exam

    async def get_exam(
        self,
        course_id: int,
        exam_id: int,
        with_students=False,
        with_exercise_groups=False,
    ) -> Exam:
        """
        Returns an exams for a course and an exam id.
        """
        params = {
            "withStudents": str(with_students).lower(),
            "withExerciseGroups": str(with_exercise_groups).lower(),
        }
        resp = await self._session.get_api_endpoint(
            f"/courses/{course_id}/exams/{exam_id}", params=params
        )
        return await resp.json(loads=loads)

    async def get_exercise_groups(
        self, course_id: int, exam_id: int
    ) -> AsyncGenerator[ExerciseGroup, None]:
        """
        Returns exercise groups for a course and an exam id.
        """
        exam = await self.get_exam(course_id, exam_id, with_exercise_groups=True)
        if "exerciseGroups" not in exam:
            raise StopAsyncIteration
        for group in exam["exerciseGroups"]:
            yield group

    async def get_student_exams(
        self, course_id: int, exam_id: int
    ) -> AsyncGenerator[StudentExam, None]:
        """
        Returns the student exams for a exam.
        """
        resp = await self._session.get_api_endpoint(
            f"/courses/{course_id}/exams/{exam_id}/student-exams"
        )
        exams: List[StudentExam] = await resp.json(loads=loads)
        for exam in exams:
            yield exam

    async def toggle_to_submitted(
        self, course_id: int, exam_id: int, student_exam_id: int
    ) -> StudentExam:
        """
        Toggles a student exams to submitted. This is needed to assess a student exam that was not handed in explicitly.
        Returns the updated student exam with the submission date set.
        """
        resp = await self._session.put_api_endpoint(
            f"/courses/{course_id}/exams/{exam_id}/student-exams/{student_exam_id}/toggle-to-submitted"
        )
        return await resp.json(loads=loads)
