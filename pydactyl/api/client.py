from pydactyl.api import base
from pydactyl.constants import POWER_SIGNALS
from pydactyl.exceptions import BadRequestError
from pydactyl.responses import PaginatedResponse


class Client(base.PterodactylAPI):
    """Class for interacting with the Pterdactyl Client API."""

    def list_servers(self):
        """List all servers the client has access to."""
        endpoint = 'client'
        response = self._api_request(endpoint=endpoint)
        return PaginatedResponse(self, endpoint, response)

    def get_server(self, server_id, detail=False):
        """Get information for the specified server.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            detail(bool): If True includes the object type and a nested data
                    structure.  This is not particularly useful.
        """
        response = self._api_request(endpoint='client/servers/%s' % server_id)
        return base.parse_response(response, detail)

    def get_server_utilization(self, server_id, detail=False):
        """Get resource utilization information for the specified server.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            detail(bool): If True includes the object type and a nested data
                    structure.  This is not particularly useful.
        """
        response = self._api_request(
            endpoint='client/servers/%s/utilization' % server_id)
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
        response = self._api_request(
            endpoint='client/servers/%s/command' % server_id, mode='POST',
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
                'Invalid power signal sent(%s), must be one of: %r' % (
                    signal, POWER_SIGNALS))

        data = {'signal': signal}
        response = self._api_request(
            endpoint='client/servers/%s/power' % server_id, mode='POST',
            data=data, json=False)
        return response

    def list_files(self, server_id, path=None):
        """List files belonging to specified server.

        Optionally specify a directory and only return results in the
        specified directory.  Directory is relative to the server's root.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            path(str): Path to list in (e.g. 'save_game')
        """
        params = {}
        endpoint = 'client/servers/%s/files/list' % server_id
        if path is not None:
            params = {'directory': path}
        response = self._api_request(endpoint=endpoint, params=params)
        return response

    def download_file(self, server_id, path):
        """Get a download link for the specified file on the specified server.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            path(str): URL encoded path to desired file (e.g. 'eula.txt')

        Returns:
            response(str): Signed URL to download file
        """
        endpoint = 'client/servers/%s/files/download' % server_id
        params = {'file': path}
        response = self._api_request(endpoint=endpoint, params=params)
        return response.get('attributes').get('url')

    def rename_file(self, server_id, old_name, new_name, root='/'):
        """Rename a file.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            old_name(str): Name of existing file to rename
            new_name(str): New filename
            root(str): Path to files, relative to server root
        """
        endpoint = 'client/servers/%s/files/rename' % server_id
        data = {'root': root, 'files': [{'from': old_name, 'to': new_name}]}
        response = self._api_request(endpoint=endpoint, mode='PUT', data=data)
        return response
