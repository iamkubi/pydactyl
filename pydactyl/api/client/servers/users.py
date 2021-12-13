from pydactyl.api import base


class Users(base.PterodactylAPI):
    """Pterodactyl Client Server Backups API."""

    def list_users(self, server_id: str):
        """List all users added to the server.

        Includes user details and permissions assigned to them.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
        """
        endpoint = 'client/servers/{}/users'.format(server_id)
        response = self._api_request(endpoint=endpoint)
        return response

    def create_user(self, server_id: str, email: str, permissions: iter,
                    username: str = None):
        """Adds a new user to the server.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            email(str): Email address of the new user
            permissions(iter): List of permissions to assign to the user
            username(str): Username to assign, randomized if not specified
        """
        data = {'email': email, 'permissions': permissions}
        if username:
            data['username'] = username
        endpoint = 'client/servers/{}/users'.format(server_id)
        response = self._api_request(endpoint=endpoint, mode='POST', data=data)
        return response

    def get_user(self, server_id: str, user_id: str):
        """Retrieves details about the specified user.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            user_id(str): User identifier (long UUID)
        """
        endpoint = 'client/servers/{}/users/{}'.format(server_id, user_id)
        response = self._api_request(endpoint=endpoint)
        return response

    def update_user(self, server_id: str, user_id: str, permissions):
        """Updates the specified user.

        This probably has more options than the documentation list.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            user_id(str): User identifier (long UUID)
            permissions(iter): List of permissions to assign to the user
        """
        data = {'permissions': permissions}
        endpoint = 'client/servers/{}/users/{}'.format(server_id, user_id)
        response = self._api_request(endpoint=endpoint, mode='POST', data=data)
        return response

    def delete_user(self, server_id: str, user_id: str):
        """Deletes the specified user.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            user_id(str): User identifier (long UUID)
        """
        endpoint = 'client/servers/{}/users/{}'.format(server_id, user_id)
        response = self._api_request(endpoint=endpoint, mode='DELETE')
        return response
