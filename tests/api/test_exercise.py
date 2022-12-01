import pytest
from typeguard import check_type
from artemis_client.api import (
    Participation,
    ProgrammingExerciseStudentParticipation,
    Result,
    SolutionProgrammingExerciseParticipation,
    StudentParticipation,
    TemplateProgrammingExerciseParticipation,
)

from artemis_client.session import ArtemisSession


@pytest.mark.asyncio
async def test_get_results(artemis_session: ArtemisSession):
    async for c in artemis_session.course.get_courses_with_stats():
        async for e in artemis_session.course.get_exercises_for_course(c["id"]):
            results = await artemis_session.exercise.get_results(e["id"])
            for result in results:
                check_type("Result", result, Result)
                return
    pytest.skip("Result not found")


@pytest.mark.dependency()
@pytest.mark.asyncio
async def test_get_participations(artemis_session: ArtemisSession):
    # If this fails a new participation type may be added.
    async for c in artemis_session.course.get_courses_with_stats():
        async for e in artemis_session.course.get_exercises_for_course(c["id"]):
            async for p in artemis_session.exercise.get_participations(e["id"]):
                check_type("Participation", p, Participation)
                return
    pytest.skip("Result not found")


@pytest.mark.dependency(
    [
        "test_get_participations_ProgrammingExerciseStudentParticipation",
        "test_get_participations_TemplateProgrammingExerciseParticipation",
        "test_get_participations_TemplateProgrammingExerciseParticipation",
        "test_get_participations_SolutionProgrammingExerciseParticipation",
    ]
)
@pytest.mark.asyncio
async def test_get_participations_StudentParticipation(artemis_session: ArtemisSession):
    async for c in artemis_session.course.get_courses_with_stats():
        async for e in artemis_session.course.get_exercises_for_course(c["id"]):
            async for p in artemis_session.exercise.get_participations(e["id"]):
                if p["type"] == "student":
                    check_type("StudentParticipation", p, StudentParticipation)
                    return
    pytest.skip("Result not found")


@pytest.mark.dependency()
@pytest.mark.asyncio
async def test_get_participations_ProgrammingExerciseStudentParticipation(
    artemis_session: ArtemisSession,
):
    async for c in artemis_session.course.get_courses_with_stats():
        async for e in artemis_session.course.get_exercises_for_course(c["id"]):
            async for p in artemis_session.exercise.get_participations(e["id"]):
                if p["type"] == "programming":
                    check_type(
                        "ProgrammingExerciseStudentParticipation",
                        p,
                        ProgrammingExerciseStudentParticipation,
                    )
                    return
    pytest.skip("Result not found")


@pytest.mark.dependency()
@pytest.mark.asyncio
async def test_get_participations_TemplateProgrammingExerciseParticipation(
    artemis_session: ArtemisSession,
):
    async for c in artemis_session.course.get_courses_with_stats():
        async for e in artemis_session.course.get_exercises_for_course(c["id"]):
            async for p in artemis_session.exercise.get_participations(e["id"]):
                if p["type"] == "template":
                    check_type(
                        "TemplateProgrammingExerciseParticipation",
                        p,
                        TemplateProgrammingExerciseParticipation,
                    )
                    return
    pytest.skip("Result not found")


@pytest.mark.dependency()
@pytest.mark.asyncio
async def test_get_participations_SolutionProgrammingExerciseParticipation(
    artemis_session: ArtemisSession,
):
    async for c in artemis_session.course.get_courses_with_stats():
        async for e in artemis_session.course.get_exercises_for_course(c["id"]):
            async for p in artemis_session.exercise.get_participations(e["id"]):
                if p["type"] == "solution":
                    check_type(
                        "SolutionProgrammingExerciseParticipation",
                        p,
                        SolutionProgrammingExerciseParticipation,
                    )
                    return
    pytest.skip("Result not found")
