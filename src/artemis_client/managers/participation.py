from artemis_client.managers import participation_managers
from artemis_client.managers.manager import ArtemisManager
from artemis_client.session import ArtemisSession


class ParticipationManager(ArtemisManager):
    def __init__(self, session: ArtemisSession):
        super().__init__(session)
        self.programming = participation_managers.ProgrammingExerciseParticipationManager(self._session)
        """See :class:`~artemis_client.managers.participation_managers.ProgrammingExerciseParticipationManager`"""
