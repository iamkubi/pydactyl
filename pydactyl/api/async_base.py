import aiohttp
from pydactyl.api import base
from pydactyl.exceptions import BadRequestError, PterodactylApiError
from pydactyl.constants import REQUEST_TYPES

class AsyncPterodactylAPI(object):
    """Async Pterodactyl API client."""

    def __init__(self, url, api_key, session=None):
        self._api_key = api_key
        self._url = url
        self._session = session

    def _get_headers(self):
        """Headers to use for API calls."""
        headers = {
            'Authorization': 'Bearer {0}'.format(self._api_key),
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        return headers

    async def _api_request(self, endpoint, mode='GET', params=None, data=None,
                           json=None, override_headers=None, data_as_json=True,
                           includes=None):
        """Make a request to the Pterodactyl API."""
        if not endpoint:
            raise BadRequestError('No API endpoint was specified.')

        url = base.url_join(self._url, 'api', endpoint)
        headers = self._get_headers()
        if override_headers:
            headers.update(override_headers)

        if includes:
            include_str = ','.join(includes)
            if params and params.get('include'):
                params['include'] += ',' + include_str
            elif params:
                params['include'] = include_str
            else:
                params = {'include': include_str}

        # Create a session if one wasn't provided or if it's closed
        local_session = False
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
            local_session = True

        try:
            if mode == 'GET':
                async with self._session.get(url, params=params, headers=headers) as response:
                    return await self._handle_response(response, json)
            elif mode == 'POST':
                if data_as_json:
                    async with self._session.post(url, params=params, headers=headers, json=data) as response:
                        return await self._handle_response(response, json)
                else:
                    async with self._session.post(url, params=params, headers=headers, data=data) as response:
                        return await self._handle_response(response, json)
            elif mode == 'PATCH':
                async with self._session.patch(url, params=params, headers=headers, json=data) as response:
                    return await self._handle_response(response, json)
            elif mode == 'DELETE':
                async with self._session.delete(url, params=params, headers=headers, json=data) as response:
                    return await self._handle_response(response, json)
            elif mode == 'PUT':
                async with self._session.put(url, params=params, headers=headers, json=data) as response:
                    return await self._handle_response(response, json)
            else:
                raise BadRequestError(
                    'Invalid request type specified(%s).  Must be one of %r.' % (
                        mode, REQUEST_TYPES))
        finally:
            if local_session:
                await self._session.close()

    async def _handle_response(self, response, json_output):
        try:
            response_json = await response.json()
        except Exception:
            response_json = {}

        if response.status in (400, 422):
            raise PterodactylApiError('API Request resulted in errors: %s' %
                                      response_json.get('errors'))
        else:
            response.raise_for_status()

        if json_output is True:
            return response_json
        elif json_output is False:
            return response
        else:
            return response_json or response

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
