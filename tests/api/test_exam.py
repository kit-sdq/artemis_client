import pytest
from typeguard import check_type
from artemis_client.api import Exam, ExerciseGroup, StudentExam

from artemis_client.session import ArtemisSession


@pytest.mark.asyncio
async def test_get_exams(artemis_session: ArtemisSession):
    async for c in artemis_session.course.get_courses():
        async for exam in artemis_session.exam.get_exams(c["id"]):
            check_type("Exam", exam, Exam)
            return
    pytest.skip("No exam found")


@pytest.mark.asyncio
async def test_get_exercise_groups(artemis_session: ArtemisSession):
    async for c in artemis_session.course.get_courses():
        async for exam in artemis_session.exam.get_exams(c["id"]):
            async for exercise_group in artemis_session.exam.get_exercise_groups(c["id"], exam["id"]):
                check_type("Exam", exercise_group, ExerciseGroup)
                return
    pytest.skip("No exercise group found")


@pytest.mark.asyncio
async def test_get_student_exams(artemis_session: ArtemisSession):
    async for c in artemis_session.course.get_courses():
        async for exam in artemis_session.exam.get_exams(c["id"]):
            async for student_exam in artemis_session.exam.get_student_exams(c["id"], exam["id"]):
                check_type("StudentExam", student_exam, StudentExam)
                return
    pytest.skip("No student exam found")
