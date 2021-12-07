from artemis_client.session import ArtemisSession


class ArtemisManager():

    _session: ArtemisSession

    def __init__(self, artemis_session: ArtemisSession) -> None:
        self._session = artemis_session
