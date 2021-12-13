from pydactyl.api.client.client_api import ClientAPI
from pydactyl.api.locations import Locations
from pydactyl.api.nests import Nests
from pydactyl.api.nodes import Nodes
from pydactyl.api.servers import Servers
from pydactyl.api.user import User
from pydactyl.exceptions import ClientConfigError


class PterodactylClient(object):
    """Provides a simplified interface to the Pterodactyl Panel API.

    Instances of this class allow interaction with the Pterodactyl Panel API.
    """

    def __init__(self, url=None, api_key=None):
        """Initialize a Pterodactyl class instance.

        Args:
            url(str): The base URL of the panel to connect to.
            api_key(str): Pterodactyl Panel API key.
        """
        if not url:
            raise ClientConfigError(
                'You must specify the hostname of a Pterodactyl instance.')

        if not api_key:
            raise ClientConfigError(
                'You must specify a Pterodactyl API key to authenticate.')

        self._url = url
        self._api_key = api_key

        self._client = None
        self._locations = None
        self._nests = None
        self._nodes = None
        self._servers = None
        self._user = None

    @property
    def client(self):
        self._client = ClientAPI(self._url, self._api_key)
        return self._client

    @property
    def locations(self):
        self._locations = Locations(self._url, self._api_key)
        return self._locations

    @property
    def nests(self):
        self._nests = Nests(self._url, self._api_key)
        return self._nests

    @property
    def nodes(self):
        self._nodes = Nodes(self._url, self._api_key)
        return self._nodes

    @property
    def servers(self):
        self._servers = Servers(self._url, self._api_key)
        return self._servers

    @property
    def user(self):
        self._user = User(self._url, self._api_key)
        return self._user
