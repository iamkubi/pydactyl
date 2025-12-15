from pydactyl.api import base
from pydactyl.api.async_base import AsyncPterodactylAPI
from pydactyl.api.client.servers.async_websocket_client import AsyncWebsocketClient
from pydactyl.constants import POWER_SIGNALS
from pydactyl.exceptions import BadRequestError
from pydactyl.responses import PaginatedResponse


class AsyncServersBase(AsyncPterodactylAPI):
    """Async Pterodactyl Client Server Base API.

    Methods in this class appear in the base **client.servers** namespace
    when using AsyncPterodactylClient.
    """

    async def list_servers(self, includes=None, params=None):
        """List all servers the client has access to.

        Args:
            includes(iter): List of includes, e.g. ('egg', 'subusers')
            params(dict): Extra parameters to pass, e.g. {'per_page': 300}
        """
        endpoint = 'client'
        response = await self._api_request(endpoint=endpoint, includes=includes,
                                     params=params)
        return PaginatedResponse(self, endpoint, response)

    async def list_permissions(self):
        """Retries all available permissions.

        This is used by the frontend.  I have no idea what this does.
        """
        endpoint = 'client/permissions'
        response = await self._api_request(endpoint=endpoint)
        return response

    async def get_server(self, server_id, detail=False, includes=None, params=None):
        """Get information for the specified server.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            detail(bool): If True includes the object type and a nested data
                    structure.  This is not particularly useful.
            includes(iter): List of includes, e.g. ('egg', 'subusers')
            params(dict): Extra parameters to pass, e.g. {'per_page': 300}
        """
        response = await self._api_request(
            endpoint='client/servers/{}'.format(server_id),
            includes=includes, params=params)
        return base.parse_response(response, detail)

    async def get_server_utilization(self, server_id, detail=False):
        """Get resource utilization information for the specified server.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            detail(bool): If True includes the object type and a nested data
                    structure.  This is not particularly useful.
        """
        response = await self._api_request(
            endpoint='client/servers/{}/resources'.format(server_id))
        return base.parse_response(response, detail)

    async def send_console_command(self, server_id, cmd):
        """Sends a console command to the specified server.

        The server must be online, otherwise API will return a HTTP 412 error.
        If successful, there will be an empty response body.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            cmd(str): Console command to send to the server
        """
        data = {'command': cmd}
        endpoint = 'client/servers/{}/command'.format(server_id)
        response = await self._api_request(endpoint=endpoint, mode='POST',
                                     data=data, json=False)
        return response

    async def send_power_action(self, server_id, signal):
        """Sends a console command to the specified server.

        The server must be online, otherwise API will return a HTTP 412 error.
        If successful, there will be an empty response body.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            signal(str): Power signal to send to the server.
                Valid options:
                start - Sends the startup command to the server.
                stop - Sends the stop command to the server.
                restart - Stops the server then immediately starts it.
                kill - Instantly ends all processes and marks the server as
                       stopped.  The kill signal can corrupt server files
                       and should only be used as a last resort.
        """
        if signal not in POWER_SIGNALS:
            raise BadRequestError(
                'Invalid power signal sent({}), must be one of: {}'.format(
                    signal, POWER_SIGNALS))

        data = {'signal': signal}
        endpoint = 'client/servers/{}/power'.format(server_id)
        response = await self._api_request(endpoint=endpoint, mode='POST',
                                     data=data, json=False)
        return response

    async def get_websocket(self, server_id):
        """Generates credentials to connect to the server's websocket.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
        Returns:
            response(dict): Response with token and websocket address
        """
        endpoint = 'client/servers/{}/websocket'.format(server_id)
        response = await self._api_request(endpoint=endpoint, mode='GET')
        return response

    async def get_websocket_client(self, server_id):
        """Get an authenticated websocket client for the server.

        Args:
            server_id(str): Server identifier (abbreviated UUID)

        Returns:
            WebsocketClient: An instantiated and ready-to-connect websocket client.
        """
        response = await self.get_websocket(server_id)
        data = response['data']

        async def refresh_token():
            return await self.get_websocket(server_id)

        return AsyncWebsocketClient(url=data['socket'], token=data['token'],
                                    session=self._session,
                                    token_refresher=refresh_token)
