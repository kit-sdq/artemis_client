""" This file configures pytest.
"""
import asyncio
from typing import List
from aiohttp.client_exceptions import ClientResponseError
import pytest
import random
import string
from datetime import datetime, timedelta
from artemis_client.api import Course

from artemis_client.session import ArtemisSession


# Make sure the event loop is reused: Allow reusing artemis session
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def artemis_session():
    async with ArtemisSession() as session:
        yield session


@pytest.fixture(scope="function", autouse=True)
async def test_course_generator(artemis_session: ArtemisSession):
    _temp_courses: List[Course] = []
    counter = 1
    random_string = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=5))

    async def make_course():
        nonlocal _temp_courses
        nonlocal counter

        course: Course = {
                "accuracyOfScores": 2,
                "color": None,
                "complaintsEnabled": True,
                "courseIcon": None,
                "customizeGroupNames": False,
                "description": "test api",
                "editorGroupName": None,
                "endDate": datetime.now() + timedelta(1),
                "startDate": datetime.now(),
                "id": 0,
                "instructorGroupName": None,
                "maxComplaintTimeDays": 7,
                "maxComplaints": 3,
                "maxPoints": 10,
                "maxRequestMoreFeedbackTimeDays": 7,
                "maxTeamComplaints": 3,
                "onlineCourse": False,
                "postsEnabled": False,
                "presentationScore": 0,
                "registrationConfirmationMessage": None,
                "registrationEnabled": False,
                "requestMoreFeedbackEnabled": True,
                "semester": "SS22",
                "shortName": f"test{random_string}{counter}",
                "studentGroupName": None,
                "teachingAssistantGroupName": None,
                "testCourse": True,
                "title": f"test-{random_string}-{counter}",
        }

        counter += 1

        new_course = await artemis_session.course.create_course(course)
        if "shortName" in new_course:
            assert new_course["shortName"] == course["shortName"]
        _temp_courses += [new_course]
        return new_course

    yield make_course

    for course in _temp_courses:
        try:
            await artemis_session.course.delete_course(course["id"])
        except ClientResponseError as e:
            assert e.status == 404  # course was deleted by test
