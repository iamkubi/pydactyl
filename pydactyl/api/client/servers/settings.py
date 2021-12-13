from pydactyl.api import base


class Settings(base.PterodactylAPI):
    """Pterodactyl Client Server Settings API."""

    def rename_server(self, server_id: str, name: str):
        """Renames the server.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            name(str): New name for the server
        """
        data = {'name': name}
        endpoint = 'client/servers/{}/settings/rename'.format(server_id)
        response = self._api_request(endpoint=endpoint, mode='POST', data=data)
        return response

    def reinstall_server(self, server_id: str):
        """Reinstalls the specified server.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
        """
        endpoint = 'client/servers/{}/settings/reinstall'.format(server_id)
        response = self._api_request(endpoint=endpoint, mode='POST')
        return response
