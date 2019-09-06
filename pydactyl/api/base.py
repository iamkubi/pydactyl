import requests
from requests.compat import urljoin


class PterodactylAPI(object):
    """Pterodactyl API client."""

    def __init__(self, hostname, api_key):
        super(PterodactylAPI, self).__init__()
        self._api_key = api_key
        self._hostname = urljoin(hostname, 'api/')

    def _get_headers(self):
        """Headers to use for API calls."""
        headers = {
            'Accept': 'Application/vnd.pterodactyl.v1+json',
            'Authorization': 'Bearer {0}'.format(self._api_key),
            'Content-Type': 'application/js',
        }

        return headers

    def _request_get(self, endpoint, params=None):
        """Make a GET request to the Pterodactyl API.

        Args:
            endpoint(str): URI for the API
            params(dict): Extra parameters to pass to the endpoint, e.g. a query string

        Returns:
            response(obj): A HTTP response object
        """
        url = urljoin(self._hostname, endpoint)
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
        url = urljoin(self._hostname, endpoint)
        headers = self._get_headers()

        response = requests.post(url, params=params, headers=headers, data=data)
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
        url = urljoin(self._hostname, endpoint)
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
        url = urljoin(self._hostname, endpoint)
        headers = self._get_headers()

        response = requests.delete(url, params=params, headers=headers)
        response.raise_for_status()

        return response
