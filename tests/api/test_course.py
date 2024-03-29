from aiohttp.client_exceptions import ClientResponseError
import pytest
from typeguard import check_type
from artemis_client.api import (
    Course,
    CourseWithExercises,
    CourseWithStats,
    Exercise,
    FileUploadExercise,
    ModelingExercise,
    ProgrammingExercise,
    QuizExercise,
    TextExercise,
    User,
)

from artemis_client.session import ArtemisSession


@pytest.mark.asyncio
async def test_get_courses(artemis_session: ArtemisSession):
    async for c in artemis_session.course.get_courses():
        check_type("Course", c, Course)
        break
    else:
        pytest.skip("No course found")


@pytest.mark.asyncio
async def test_get_courses_with_stats(artemis_session: ArtemisSession):
    async for c in artemis_session.course.get_courses_with_stats():
        check_type("CourseWithStats", c, CourseWithStats)
        break
    else:
        pytest.skip("No course found")


@pytest.mark.asyncio
async def test_get_course(artemis_session: ArtemisSession):
    async for c in artemis_session.course.get_courses_with_stats():
        course = await artemis_session.course.get_course(c["id"])
        check_type("CourseWithStats", course, CourseWithStats)
        break
    else:
        pytest.skip("No course found")


@pytest.mark.asyncio
async def test_get_course_with_exercises(artemis_session: ArtemisSession):
    async for c in artemis_session.course.get_courses_with_stats():
        course = await artemis_session.course.get_course_with_exercises(c["id"])
        check_type("CourseWithExercises", course, CourseWithExercises)
        break
    else:
        pytest.skip("No course found")


@pytest.mark.dependency()
@pytest.mark.asyncio
async def test_programming_exercise_type(artemis_session: ArtemisSession):
    found = False
    async for c in artemis_session.course.get_courses_with_stats():
        async for e in artemis_session.course.get_exercises_for_course(c["id"]):
            if "type" in e:
                if e["type"] == "programming":
                    check_type("ProgrammingExercise", e, ProgrammingExercise)
                    found = True
    if not found:
        pytest.skip("No course with programming exercises found")


@pytest.mark.dependency()
@pytest.mark.asyncio
async def test_modeling_exercise_type(artemis_session: ArtemisSession):
    async for c in artemis_session.course.get_courses_with_stats():
        async for e in artemis_session.course.get_exercises_for_course(c["id"]):
            if "type" in e:
                if e["type"] == "modeling":
                    check_type("ModelingExercise", e, ModelingExercise)
                    return
    pytest.skip("No course with modeling exercises found")


@pytest.mark.dependency()
@pytest.mark.asyncio
async def test_quiz_exercise_type(artemis_session: ArtemisSession):
    async for c in artemis_session.course.get_courses_with_stats():
        async for e in artemis_session.course.get_exercises_for_course(c["id"]):
            if "type" in e:
                if e["type"] == "quiz":
                    check_type("QuizExercise", e, QuizExercise)
                    return
    pytest.skip("No course with quiz exercises found")


@pytest.mark.dependency()
@pytest.mark.asyncio
async def test_text_exercise_type(artemis_session: ArtemisSession):
    async for c in artemis_session.course.get_courses_with_stats():
        async for e in artemis_session.course.get_exercises_for_course(c["id"]):
            if "type" in e:
                if e["type"] == "text":
                    check_type("TextExercise", e, TextExercise)
                    return
    pytest.skip("No course with text exercises found")


@pytest.mark.dependency()
@pytest.mark.asyncio
async def test_file_upload_exercise_type(artemis_session: ArtemisSession):
    async for c in artemis_session.course.get_courses_with_stats():
        async for e in artemis_session.course.get_exercises_for_course(c["id"]):
            if "type" in e:
                if e["type"] == "file-upload":
                    check_type("FileUploadExercise", e, FileUploadExercise)
                    return
    pytest.skip("No course with file-upload exercises found")


@pytest.mark.dependency(
    depends=[
        "test_programming_exercise_type",
        "test_modeling_exercise_type",
        "test_quiz_exercise_type",
        "test_text_exercise_type",
        "test_file_upload_exercise_type",
    ]
)
@pytest.mark.asyncio
async def test_get_exercises_for_course(artemis_session: ArtemisSession):
    found = False
    async for c in artemis_session.course.get_courses_with_stats():
        async for e in artemis_session.course.get_exercises_for_course(c["id"]):
            check_type("Exercise", e, Exercise)
            # If this test failes, check if a new ExerciseType was added and update the API
            # entities and add test_*_exercise_type
            found = True
    if not found:
        pytest.skip("No course with exercises found")


@pytest.mark.asyncio
async def test_delete_course(artemis_session: ArtemisSession, test_course_generator):
    new_course = await test_course_generator()
    assert await artemis_session.course.get_course(new_course["id"])
    resp = await artemis_session.course.delete_course(new_course["id"])
    assert resp.ok
    with pytest.raises(ClientResponseError):
        await artemis_session.course.get_course(new_course["id"])
    with pytest.raises(ClientResponseError):
        await artemis_session.course.delete_course(new_course["id"])


@pytest.mark.asyncio
async def test_create_course(artemis_session: ArtemisSession, test_course_generator):
    new_course = await test_course_generator()
    assert await artemis_session.course.get_course(new_course["id"])


@pytest.mark.asyncio
async def test_get_students_in_course(artemis_session: ArtemisSession):
    async for c in artemis_session.course.get_courses_with_stats():
        async for user in artemis_session.course.get_students_in_course(c["id"]):
            check_type("User", user, User)
            if "authorities" in user:
                assert "ROLE_USER" in user["authorities"]
            return
    pytest.skip("No course with students found")


@pytest.mark.asyncio
async def test_get_tutors_in_course(artemis_session: ArtemisSession):
    async for c in artemis_session.course.get_courses_with_stats():
        async for user in artemis_session.course.get_tutors_in_course(c["id"]):
            check_type("User", user, User)
            if "authorities" in user:
                assert "ROLE_TUTOR" in user["authorities"]
            return
    pytest.skip("No course with tutors found")


@pytest.mark.asyncio
async def test_get_editors_in_course(artemis_session: ArtemisSession):
    async for c in artemis_session.course.get_courses_with_stats():
        async for user in artemis_session.course.get_editors_in_course(c["id"]):
            check_type("User", user, User)
            if "authorities" in user:
                assert "ROLE_EDITOR" in user["authorities"]
            return
    pytest.skip("No course with editors found")


@pytest.mark.asyncio
async def test_get_instructors_in_course(artemis_session: ArtemisSession):
    async for c in artemis_session.course.get_courses_with_stats():
        async for user in artemis_session.course.get_instructors_in_course(c["id"]):
            check_type("User", user, User)
            if "authorities" in user:
                assert "ROLE_INSTRUCTOR" in user["authorities"]
            return
    pytest.skip("No course with instructors found")
