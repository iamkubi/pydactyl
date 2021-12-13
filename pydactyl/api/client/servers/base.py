from pydactyl.api import base
from pydactyl.constants import POWER_SIGNALS
from pydactyl.exceptions import BadRequestError
from pydactyl.responses import PaginatedResponse


class ServersBase(base.PterodactylAPI):
    """Pterodactyl Client Server Base API."""

    def list_servers(self):
        """List all servers the client has access to."""
        endpoint = 'client'
        response = self._api_request(endpoint=endpoint)
        return PaginatedResponse(self, endpoint, response)

    def list_permissions(self):
        """Retries all available permissions.

        This is used by the frontend.  I have no idea what this does.
        """
        endpoint = 'client/permissions'
        response = self._api_request(endpoint=endpoint)
        return response

    def get_server(self, server_id, detail=False):
        """Get information for the specified server.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            detail(bool): If True includes the object type and a nested data
                    structure.  This is not particularly useful.
        """
        response = self._api_request(
            endpoint='client/servers/{}'.format(server_id))
        return base.parse_response(response, detail)

    def get_server_utilization(self, server_id, detail=False):
        """Get resource utilization information for the specified server.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            detail(bool): If True includes the object type and a nested data
                    structure.  This is not particularly useful.
        """
        response = self._api_request(
            endpoint='client/servers/{}/resources'.format(server_id))
        return base.parse_response(response, detail)

    def send_console_command(self, server_id, cmd):
        """Sends a console command to the specified server.

        The server must be online, otherwise API will return a HTTP 412 error.
        If successful, there will be an empty response body.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            cmd(str): Console command to send to the server
        """
        data = {'command': cmd}
        endpoint = 'client/servers/{}/command'.format(server_id)
        response = self._api_request(endpoint=endpoint, mode='POST',
                                     data=data, json=False)
        return response

    def send_power_action(self, server_id, signal):
        """Sends a console command to the specified server.

        The server must be online, otherwise API will return a HTTP 412 error.
        If successful, there will be an empty response body.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            signal(str): Power signal to send to the server.  Valid options:
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
        response = self._api_request(endpoint=endpoint, mode='POST',
                                     data=data, json=False)
        return response
