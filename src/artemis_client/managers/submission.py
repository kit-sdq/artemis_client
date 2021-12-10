from artemis_client.managers import submission_managers
from artemis_client.managers.manager import ArtemisManager
from artemis_client.session import ArtemisSession


class SubmissionManager(ArtemisManager):
    def __init__(self, session: ArtemisSession):
        super().__init__(session)
        self.programming = submission_managers.ProgrammingSubmissionManager(
            self._session
        )
        """See :class:`~artemis_client.managers.submission_managers.ProgrammingSubmissionManager`"""
