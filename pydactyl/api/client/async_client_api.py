from pydactyl.api.async_base import AsyncPterodactylAPI
from pydactyl.api.client.account.async_base import AsyncAccount
from pydactyl.api.client.servers.async_base import AsyncServersBase
from pydactyl.api.client.servers.async_backups import AsyncBackups
from pydactyl.api.client.servers.async_databases import AsyncDatabases
from pydactyl.api.client.servers.async_files import AsyncFiles
from pydactyl.api.client.servers.async_network import AsyncNetwork
from pydactyl.api.client.servers.async_schedules import AsyncSchedules
from pydactyl.api.client.servers.async_settings import AsyncSettings
from pydactyl.api.client.servers.async_startup import AsyncStartup
from pydactyl.api.client.servers.async_users import AsyncUsers


class AsyncClientAPI(AsyncPterodactylAPI):
    """Provides a simplified interface to the Pterodactyl Panel API."""

    def __init__(self, *args, **kwargs):
        self._servers = None
        self._account = None
        super().__init__(*args, **kwargs)

    @property
    def account(self):
        self._account = AsyncAccount(self._url, self._api_key, self._session)
        return self._account

    @property
    def servers(self):
        self._servers = AsyncClientServersAPI(self._url, self._api_key, self._session)
        return self._servers


class AsyncClientServersAPI(AsyncServersBase, AsyncClientAPI):
    """Async Client Servers API."""

    def __init__(self, *args, **kwargs):
        self._backups = None
        self._databases = None
        self._files = None
        self._network = None
        self._schedules = None
        self._settings = None
        self._startup = None
        self._users = None
        super().__init__(*args, **kwargs)

    @property
    def backups(self):
        self._backups = AsyncBackups(self._url, self._api_key, self._session)
        return self._backups

    @property
    def databases(self):
        self._databases = AsyncDatabases(self._url, self._api_key, self._session)
        return self._databases

    @property
    def files(self):
        self._files = AsyncFiles(self._url, self._api_key, self._session)
        return self._files

    @property
    def network(self):
        self._network = AsyncNetwork(self._url, self._api_key, self._session)
        return self._network

    @property
    def schedules(self):
        self._schedules = AsyncSchedules(self._url, self._api_key, self._session)
        return self._schedules

    @property
    def settings(self):
        self._settings = AsyncSettings(self._url, self._api_key, self._session)
        return self._settings

    @property
    def startup(self):
        self._startup = AsyncStartup(self._url, self._api_key, self._session)
        return self._startup

    @property
    def users(self):
        self._users = AsyncUsers(self._url, self._api_key, self._session)
        return self._users
