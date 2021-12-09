import pytest

from typeguard import check_type
from artemis_client.api import Course, CourseWithStats

from artemis_client.session import ArtemisSession


@pytest.mark.asyncio
async def test_get_courses(artemis_session: ArtemisSession):
    async for c in artemis_session.course.get_courses():
        check_type("c", c, Course)


@pytest.mark.asyncio
async def test_get_courses_with_stats(artemis_session: ArtemisSession):
    async for c in artemis_session.course.get_courses_with_stats():
        check_type("c", c, CourseWithStats)
