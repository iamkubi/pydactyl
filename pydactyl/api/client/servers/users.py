from pydactyl.api import base


class Users(base.PterodactylAPI):
    """Pterodactyl Client Server Backups API."""

    def list_users(self, server_id):
        """List all users added to the server.

        Includes user details and permissions assigned to them.
        """
        endpoint = 'client/servers/{}/users'.format(server_id)
        response = self._api_request(endpoint=endpoint)
        return response

    def create_user(self):
        """TODO"""
        pass

    def get_user(self):
        """TODO"""
        pass

    def update_user(self):
        """TODO"""
        pass

    def delete_user(self):
        """TODO"""
        pass
