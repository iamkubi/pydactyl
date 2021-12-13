from pydactyl.api import base


class Startup(base.PterodactylAPI):
    """Pterodactyl Client Server Startup API."""

    def list_variables(self, server_id: str):
        """Lists all variables on the server.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
        """
        endpoint = 'client/servers/{}/startup'.format(server_id)
        response = self._api_request(endpoint=endpoint)
        return response

    def update_variable(self, server_id: str, name: str, value: str):
        """Updates the specified server variable.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            name(str): Variable name to update
            value(str): Value to assign to the updated variable
        """
        data = {'key': name, 'value': value}
        endpoint = 'client/servers/{}/startup/variable'.format(server_id)
        response = self._api_request(endpoint=endpoint, mode='PUT', data=data)
        return response
