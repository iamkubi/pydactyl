"""Provide the Pterodactyl class."""

import requests


class Error(Exception):
    """Base class for excpetions."""
    pass


class BadRequestError(Error):
    """Raised when there is a problem with the API request."""
    pass


class Pytdactyl(object):
    """Provides a simplified interface to the Pterodactyl Panel API.

    Instances of this class allow you to interact with the Pterodactyl Panel API.
    An example
    """

    def __init__(
            self,
            hostname=None,
            api_key=None):
        """Initialize a Pterodactyl class instance.

        Args:
            hostname(str): The base URL of the panel to connect to.
            api_key(str): Pterodactyl Panel API key.
        """
        self.__hostname = hostname
        self.__api_key = api_key

        self.client = client

    def _api_call(self, endpoint, mode='GET', params={}, data={}):
        """Makes an API call to the Pterodactyl Panel.

        Args:
            endpoint(str): Name of the API endpoint to connect to
            mode(str): Request mode: GET, POST, PATCH, or DELETE
            params(dict): Extra parameters to pass to the endpoint, e.g. a query string
            data(dict): POST data
        """
        request_url = requests.urljoin(self.__hostname, endpoint)
        headers = {
            'Accept': 'Application/vnd.pterodactyl.v1+json',
            'Authorization': 'Bearer {0}'.format(self.__api_key),
            'Content-Type': 'application/js',
        }

        if mode == 'GET':
            response = requests.get(request_url, params=params, headers=headers)
        elif mode == 'POST':
            response = requests.post(request_url, data=data, headers=headers)
        elif mode == 'PATCH':
            response = requests.patch(request_url, data=data, headers=headers)
        elif mode == 'DELETE':
            response = requests.delete(request_url, headers=headers)
        else:
            raise BadRequestError('Invalid mode specified for request: %s' % mode)

        response.raise_for_status()
        return response
