from aiohttp.client_exceptions import ClientResponseError
import pytest
from typeguard import check_type
from artemis_client.api import (
    TextExercise,
    TextSubmission,
    Participation
)
from typing import cast

from artemis_client.session import ArtemisSession


@pytest.mark.asyncio
async def test_text_assessment_next_and_cancel(artemis_session: ArtemisSession):
    found = False
    async for c in artemis_session.course.get_courses_with_stats():
        async for e in artemis_session.course.get_exercises_for_course(c["id"]):
            exercise = None
            if "type" in e:
                if e["type"] == "text":
                    exercise = cast(TextExercise, e)
            if exercise is None:
                continue

            submission = await artemis_session.assessment.text.next(exercise["id"])
            check_type("TextSubmission", submission, TextSubmission)

            if "participation" in submission:
                # cancel the started submission:
                await artemis_session.assessment.text.cancel(submission["participation"]["id"], submission["id"])

            # stop executing so it does not lock infinitely:
            return

    if not found:
        pytest.skip("No course with text exercises found")

@pytest.mark.asyncio
async def test_text_assessment_start_and_get_submissions(artemis_session: ArtemisSession):
    found = False
    async for c in artemis_session.course.get_courses():
        async for e in artemis_session.course.get_exercises_for_course(c["id"]):
            if "type" in e:
                if e["type"] != "text":
                    continue
            async for submission in artemis_session.submission.text.get_submissions(e["id"]):
                check_type("TextSubmission", submission, TextSubmission)
                if "participation" not in submission:
                    continue
                participation = await artemis_session.assessment.text.start(submission["participation"]["id"], submission["id"])
                check_type("Participation", participation, Participation)

                # cancel the started submission:
                await artemis_session.assessment.text.cancel(submission["participation"]["id"], submission["id"])
                # to reduce the load, only test one submission:
                return

    if not found:
        pytest.skip("No course with text exercises found")
