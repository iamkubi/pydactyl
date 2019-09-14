import requests

from pydactyl.constants import REQUEST_TYPES
from pydactyl.exceptions import BadRequestError


def parse_response(response, detail):
    """Parse the response data.

    Optionally includes additional data that specifies the object type
    and requires accessing the data through a nested dictionary.  The
    Client API doesn't include any additional information, but the
    Servers API includes created and updated timestamps in the detailed
    response.

    Args:
         response(dict): A request response object.
         detail(bool): Include additional data from the raw response.
    """
    if detail:
        data = response
    else:
        if response['object'] == 'list':
            data = [item.get('attributes') for item in response.get('data')]
        else:
            data = response.get('attributes')

    return data


def url_join(*args):
    """Join combine URL parts to get the full endpoint address."""
    return '/'.join(arg.strip('/') for arg in args)


class PterodactylAPI(object):
    """Pterodactyl API client."""

    def __init__(self, url, api_key):
        self._api_key = api_key
        self._url = url_join(url, 'api')

    def _get_headers(self):
        """Headers to use for API calls."""
        headers = {
            'Authorization': 'Bearer {0}'.format(self._api_key),
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        return headers

    def _api_request(self, endpoint, mode='GET', params=None, data=None,
                     json=True):
        """Make a request to the Pterodactyl API.

        Args:
            endpoint(str): URI for the API
            mode(str): Request type, one of ('GET', 'POST', 'PATCH', 'DELETE)
            params(dict): Extra parameters to pass to the endpoint,
                    e.g. a query string
            data(dict): POST data
            json(bool): Set to False to return the response object, True for
                    just JSON

        Returns:
            response: A HTTP response object or the JSON response depending on
                    the value of the json parameter.
        """
        if not endpoint:
            raise BadRequestError('No API endpoint was specified.')

        url = url_join(self._url, endpoint)
        headers = self._get_headers()

        if mode == 'GET':
            response = requests.get(url, params=params, headers=headers)
        elif mode == 'POST':
            response = requests.post(url, params=params, headers=headers,
                                     json=data)
        elif mode == 'PATCH':
            response = requests.patch(url, params=params, headers=headers,
                                      json=data)
        elif mode == 'DELETE':
            response = requests.delete(url, params=params, headers=headers)
        else:
            raise BadRequestError(
                'Invalid request type specified(%s).  Must be one of %r.' % (
                    mode, REQUEST_TYPES))

        response.raise_for_status()

        if json:
            return response.json()
        else:
            return response
