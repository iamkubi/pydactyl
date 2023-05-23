import logging
import requests

from pydactyl.api.client.client_api import ClientAPI
from pydactyl.api.locations import Locations
from pydactyl.api.nests import Nests
from pydactyl.api.nodes import Nodes
from pydactyl.api.servers import Servers
from pydactyl.api.user import User
from pydactyl.exceptions import ClientConfigError


def http_adapter(backoff_factor, retries, extra_retry_codes):
    """Configures an HTTP adapter with retries and backoff."""
    retry_codes = [429] + extra_retry_codes
    retries = requests.adapters.Retry(
        total=retries, status_forcelist=retry_codes,
        backoff_factor=backoff_factor,
        allowed_methods=['DELETE', 'GET', 'HEAD', 'OPTIONS', 'POST', 'PUT'])
    adapter = requests.adapters.HTTPAdapter(max_retries=retries)
    return adapter


def set_logger(debug):
    """Configure debug logging if requested."""
    if debug:
        level = logging.DEBUG
    else:
        level = logging.NOTSET

    logging.basicConfig()
    logging.getLogger().setLevel(level)
    requests_log = logging.getLogger('requests.packages.urllib3')
    requests_log.setLevel(level)
    requests_log.propagate = True


class PterodactylClient(object):
    """Provides a simplified interface to the Pterodactyl Panel API.

    Instances of this class allow interaction with the Pterodactyl Panel API.
    """

    def __init__(self, url=None, api_key=None, backoff_factor=1, retries=3,
                 extra_retry_codes=[], debug=False):
        """Initialize a Pterodactyl class instance.

        Args:
            url(str): The base URL of the panel to connect to.
            api_key(str): Pterodactyl Panel API key.
            backoff_factor(int): urllib3 retry backoff_factor
            retries(int): maximum number of retries per call
            extra_retry_codes(iter): list of additional integer HTTP status
                    codes to retry on, e.g. [502, 504]
            debug(bool): enable debug logging for requests
        """
        if not url:
            raise ClientConfigError(
                'You must specify the hostname of a Pterodactyl instance.')

        if not api_key:
            raise ClientConfigError(
                'You must specify a Pterodactyl API key to authenticate.')

        self._api_key = api_key
        self._url = url

        self._session = requests.Session()
        adapter = http_adapter(backoff_factor=backoff_factor,
                               retries=retries,
                               extra_retry_codes=extra_retry_codes)
        self._session.mount('https://', adapter)
        self._session.mount('http://', adapter)

        set_logger(debug)

        self._client = None
        self._locations = None
        self._nests = None
        self._nodes = None
        self._servers = None
        self._user = None

    @property
    def client(self):
        self._client = ClientAPI(self._url, self._api_key, self._session)
        return self._client

    @property
    def locations(self):
        self._locations = Locations(self._url, self._api_key, self._session)
        return self._locations

    @property
    def nests(self):
        self._nests = Nests(self._url, self._api_key, self._session)
        return self._nests

    @property
    def nodes(self):
        self._nodes = Nodes(self._url, self._api_key, self._session)
        return self._nodes

    @property
    def servers(self):
        self._servers = Servers(self._url, self._api_key, self._session)
        return self._servers

    @property
    def user(self):
        self._user = User(self._url, self._api_key, self._session)
        return self._user
