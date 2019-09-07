import requests
from requests.compat import urljoin

from pydactyl.constants import REQUEST_TYPES
from pydactyl.exceptions import BadRequestError


class PterodactylAPI(object):
    """Pterodactyl API client."""

    def __init__(self, url, api_key):
        super(PterodactylAPI, self).__init__()
        self._api_key = api_key
        self._url = urljoin(url, 'api/')

    def _get_headers(self):
        """Headers to use for API calls."""
        headers = {
            'Authorization': 'Bearer {0}'.format(self._api_key),
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        return headers

    def _api_request(self, endpoint, mode='GET', params=None, data=None, json=True):
        """Make a request to the Pterodactyl API.

        Args:
            endpoint(str): URI for the API
            params(dict): Extra parameters to pass to the endpoint, e.g. a query string
            data(dict): POST data
            json(bool): Set to False to return the response object, True for just JSON

        Returns:
            response: A HTTP response object or the JSON response depending on the value of the json parameter.
        """
        if not endpoint:
            raise BadRequestError('No API endpoint was specified.')

        url = urljoin(self._url, endpoint)
        headers = self._get_headers()

        if mode == 'GET':
            response = requests.get(url, params=params, headers=headers)
        elif mode == 'POST':
            response = requests.post(url, params=params, headers=headers, json=data)
        elif mode == 'PATCH':
            response = requests.patch(url, params=params, headers=headers, json=data)
        elif mode == 'DELETE':
            response = requests.delete(url, params=params, headers=headers)
        else:
            raise BadRequestError('Invalid request type specified(%s).  Must be one of %r.' % (mode, REQUEST_TYPES))

        response.raise_for_status()

        if json:
            return response.json()
        else:
            return response

    def _request_get(self, endpoint, params=None):
        # too much duplication here, just make one api function
        """Make a GET request to the Pterodactyl API.

        Args:
            endpoint(str): URI for the API
            params(dict): Extra parameters to pass to the endpoint, e.g. a query string

        Returns:
            response(obj): A HTTP response object
        """
        url = urljoin(self._url, endpoint)
        headers = self._get_headers()

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        return response

    def _request_post(self, endpoint, params=None, data=None):
        """Make a POST request to the Pterodactyl API.

        Args:
            endpoint(str): URI for the API
            params(dict): Extra parameters to pass to the endpoint, e.g. a query string
            data(dict): POST data

        Returns:
            response(obj): A HTTP response object
        """
        url = urljoin(self._url, endpoint)
        headers = self._get_headers()

        response = requests.post(url, params=params, headers=headers, json=data)
        response.raise_for_status()

        return response

    def _request_patch(self, endpoint, params=None, data=None):
        """Make a PATCH request to the Pterodactyl API.

        Args:
            endpoint(str): URI for the API
            params(dict): Extra parameters to pass to the endpoint, e.g. a query string
            data(dict): PATCH data
        Returns:
            response(obj): A HTTP response object
        """
        url = urljoin(self._url, endpoint)
        headers = self._get_headers()

        response = requests.patch(url, params=params, headers=headers, data=data)
        response.raise_for_status()

        return response

    def _request_delete(self, endpoint, params=None):
        """Make a DELETE request to the Pterodactyl API.

        Args:
            endpoint(str): URI for the API
            params(dict): Extra parameters to pass to the endpoint, e.g. a query string

        Returns:
            response(obj): A HTTP response object
        """
        url = urljoin(self._url, endpoint)
        headers = self._get_headers()

        response = requests.delete(url, params=params, headers=headers)
        response.raise_for_status()

        return response
