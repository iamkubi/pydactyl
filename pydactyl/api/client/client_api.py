# Client Account APIs
from pydactyl.api.client.account.base import Account

# Client Server APIs
from pydactyl.api.client.servers.backups import Backups
from pydactyl.api.client.servers.base import ServersBase
from pydactyl.api.client.servers.databases import Databases
from pydactyl.api.client.servers.files import Files
from pydactyl.api.client.servers.network import Network
from pydactyl.api.client.servers.schedules import Schedules
from pydactyl.api.client.servers.settings import Settings
from pydactyl.api.client.servers.startup import Startup
from pydactyl.api.client.servers.users import Users

from pydactyl.api.base import PterodactylAPI


class ClientAPI(PterodactylAPI):
    """Provides a simplified interface to the Pterodactyl Panel API.

    This class is only used by PterodactylClient.  It provides an interface
    for the Client API endpoints.
    """

    def __init__(self, *args, **kwargs):
        """Initialize a Pterodactyl class instance."""
        self._account = None
        self._servers = None
        super().__init__(*args, **kwargs)

    @property
    def account(self):
        self._account = Account(self._url, self._api_key)
        return self._account

    @property
    def servers(self):
        self._servers = ClientServersAPI(self._url, self._api_key)
        return self._servers


class ClientServersAPI(ServersBase, ClientAPI):
    """Provides a simplified interface to the Pterodactyl Panel API.

    This class is only used by PterodactylClient.  It provides an interface
    for the Client API endpoints.
    """

    def __init__(self, *args, **kwargs):
        """Initialize a Pterodactyl class instance."""
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
        self._backups = Backups(self._url, self._api_key)
        return self._backups

    @property
    def databases(self):
        self._databases = Databases(self._url, self._api_key)
        return self._databases

    @property
    def files(self):
        self._files = Files(self._url, self._api_key)
        return self._files

    @property
    def network(self):
        self._network = Network(self._url, self._api_key)
        return self._network

    @property
    def schedules(self):
        self._schedules = Schedules(self._url, self._api_key)
        return self._schedules

    @property
    def settings(self):
        self._settings = Settings(self._url, self._api_key)
        return self._settings

    @property
    def startup(self):
        self._startup = Startup(self._url, self._api_key)
        return self._startup

    @property
    def users(self):
        self._users = Users(self._url, self._api_key)
        return self._users
