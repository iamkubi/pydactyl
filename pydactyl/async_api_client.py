import aiohttp
import logging
from pydactyl.api.client.async_client_api import AsyncClientAPI
from pydactyl.api.async_locations import AsyncLocations
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

