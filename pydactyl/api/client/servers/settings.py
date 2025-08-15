from pydactyl.api import base


class Settings(base.PterodactylAPI):
    """Pterodactyl Client Server Settings API."""

    def rename_server(self, server_id: str, name: str, description: str | None = None):
        """Renames the server.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            name(str): New name for the server
            description(str|None) New description for the server (if description None, not change)
        """

        if name == "":
            raise Exception('name can not been "empty"')

        if description is None:
            data = {'name': name}
        else:
            data = {'name': name, 'description': description}

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
