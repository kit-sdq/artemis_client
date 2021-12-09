from artemis_client.managers import submission_managers
from artemis_client.managers.manager import ArtemisManager


class SubmissionManager(ArtemisManager):
    def __init__(self):
        self.programming = submission_managers.ProgrammingSubmissionManager(
            self._session
        )
        """See :class:`~artemis_client.managers.submission_managers.ProgrammingSubmissionManager`"""
