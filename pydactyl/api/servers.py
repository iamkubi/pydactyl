from pydactyl.api.base import PterodactylAPI
from pydactyl.exceptions import BadRequestError

class Servers(PterodactylAPI):
    """Class for interacting with the Pterdactyl Servers API."""

    def list_servers(self):
        """List all servers."""
        response = self._api_request('application/servers')
        return response

    def get_server_info(self, server_id=None, external_id=None):
        """Get detailed info for the specified server.

        Args:
            server_id(int): Pterodactyl Server ID.
            external_id(int): Server ID from an external system like WHMCS
        """
        if not server_id and not external_id:
            raise BadRequestError('Must specify either server_id or '
                                  'external_id.')
        if server_id and external_id:
            raise BadRequestError('Specify either server_id or external_id, '
                                  'not both.')

        server_id = server_id or external_id
        response = self._api_request('application/servers/%s' % server_id)
        return response
