import aiohttp
import logging
from pydactyl.api.client.async_client_api import AsyncClientAPI
from pydactyl.api.application.async_locations import AsyncLocations
from pydactyl.api.application.async_nests import AsyncNests
from pydactyl.api.application.async_nodes import AsyncNodes
from pydactyl.api.application.async_servers import AsyncServers
from pydactyl.api.application.async_user import AsyncUser
from pydactyl.exceptions import ClientConfigError

def get_logger() -> logging.Logger:
    """Get the default logger."""
    logger = logging.getLogger(__name__)
    return logger

class AsyncPterodactylClient(object):
    """Async Pterodactyl Client."""

    def __init__(self, url=None, api_key=None, logger: logging.Logger = get_logger()):
        if not url:
            raise ClientConfigError(
                'You must specify the hostname of a Pterodactyl instance.')

        if not api_key:
            raise ClientConfigError(
                'You must specify a Pterodactyl API key to authenticate.')

        self._api_key = api_key
        self._url = url
        self._logger = logger
        self._session = None
        self._client = None
        self._locations = None
        self._nests = None
        self._nodes = None
        self._servers = None
        self._user = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()

    async def close(self):
        if self._session:
            await self._session.close()

    @property
    def client(self):
        self._client = AsyncClientAPI(self._url, self._api_key, self._session)
        return self._client

    @property
    def locations(self):
        self._locations = AsyncLocations(self._url, self._api_key, self._session)
        return self._locations

    @property
    def nests(self):
        self._nests = AsyncNests(self._url, self._api_key, self._session)
        return self._nests

    @property
    def nodes(self):
        self._nodes = AsyncNodes(self._url, self._api_key, self._session)
        return self._nodes

    @property
    def servers(self):
        self._servers = AsyncServers(self._url, self._api_key, self._session)
        return self._servers

    @property
    def user(self):
        self._user = AsyncUser(self._url, self._api_key, self._session)
        return self._user
