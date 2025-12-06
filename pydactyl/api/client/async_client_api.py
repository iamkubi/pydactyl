from pydactyl.api.async_base import AsyncPterodactylAPI
from pydactyl.api.client.servers.async_backups import AsyncBackups

class AsyncClientAPI(AsyncPterodactylAPI):
    """Async Client API."""

    def __init__(self, *args, **kwargs):
        self._servers = None
        super().__init__(*args, **kwargs)

    @property
    def servers(self):
        self._servers = AsyncClientServersAPI(self._url, self._api_key, self._session)
        return self._servers


class AsyncClientServersAPI(AsyncPterodactylAPI):
    """Async Client Servers API."""

    def __init__(self, *args, **kwargs):
        self._backups = None
        super().__init__(*args, **kwargs)

    @property
    def backups(self):
        self._backups = AsyncBackups(self._url, self._api_key, self._session)
        return self._backups
