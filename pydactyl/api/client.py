from pydactyl.api.base import PterodactylAPI
from pydactyl.constants import POWER_SIGNALS
from pydactyl.exceptions import BadRequestError


class Client(PterodactylAPI):
    """Class for interacting with the Pterdactyl Client API."""

    def list_servers(self):
        """List all servers the client has access to."""
        response = self._api_request('client')
        return response

    def get_server(self, server_id):
        """Get information for the specified server.

        Args:
            server_id(str): UUID of a server
        """
        response = self._api_request('client/servers/%s' % server_id)
        return response

    def get_server_utilization(self, server_id):
        """Get resource utilization information for the specified server.

        Args:
            id(str): UUID of a server
        """
        response = self._api_request('client/servers/%s/utilization' % server_id)
        return response

    def send_console_command(self, server_id, cmd):
        """Sends a console command to the specified server.

        The server must be online, otherwise API will return a HTTP 412 error.
        If successful, there will be an empty response body.

        Args:
            id(str): UUID of a server
            cmd(str): Console command to send to the server
        """
        data = {'command': cmd}
        response = self._api_request('client/servers/%s/command' % server_id, mode='POST', data=data)
        return response

    def send_power_action(self, server_id, signal):
        """Sends a console command to the specified server.

        The server must be online, otherwise API will return a HTTP 412 error.
        If successful, there will be an empty response body.

        Args:
            id(str): UUID of a server
            signal(str): Power signal to send to the server.  Possible options include:
                start - Sends the startup command to the server.
                stop - Sends the stop command to the server.
                restart - Stops the server then immediately starts it.
                kill - Instantly ends all processes and marks the server as stopped.
                       The kill signal can corrupt server files and should only be used as a last resort.
        """
        if signal not in POWER_SIGNALS:
            raise BadRequestError('Invalid power signal sent(%s), must be one of: %r' % (signal, POWER_SIGNALS))

        data = {'signal': signal}
        response = self._api_request(endpoint='client/servers/%s/power' % server_id, mode='POST', data=data)
        return response
