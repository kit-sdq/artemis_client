from artemis_client.managers import assessment_managers
from artemis_client.managers.manager import ArtemisManager
from artemis_client.session import ArtemisSession
from artemis_client.managers.assessment_managers import ProgrammingAssessmentManager


class AssessmentManager(ArtemisManager):
    def __init__(self, session: ArtemisSession):
        super().__init__(session)
        self.programming = assessment_managers.ProgrammingAssessmentManager(
            self._session
        )
        """See :class:`~artemis_client.managers.assessment_managers.ProgrammingAssesmentManager`"""
