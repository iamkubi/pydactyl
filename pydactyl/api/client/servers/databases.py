from pydactyl.api import base


class Databases(base.PterodactylAPI):
    """Pterodactyl Client Server Databases API."""

    def list_databases(self, server_id: str, include_passwords: bool = False,
                       includes: list = [], params: dict = None):
        """List all databases for a server.

        Optionally includes the database user passwords.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            include_passwords(bool): True to include database user passwords
            includes(iter): List of includes, e.g. ('password')
            params(dict): Extra parameters to pass, e.g. {'per_page': 300}
        """
        if include_passwords:
            includes.append('password')
        endpoint = 'client/servers/{}/databases'.format(server_id)
        response = self._api_request(endpoint=endpoint,
                                     includes=includes or None, params=params)
        return response

    def create_database(self, server_id: str, name: str, remote: str = '%'):
        """Create a new database for the specified server.

        Limits connections to the address specified in remote, defaulting to
        allowing from all.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            remote(str): Remote address to allow connections from (e.g. 1.2.3.4)
        """
        data = {'database': name, 'remote': remote}
        endpoint = 'client/servers/{}/databases'.format(server_id)
        response = self._api_request(endpoint=endpoint, mode='POST', data=data)
        return response

    def rotate_database_password(self, server_id: str, database_id: str):
        """Changes the password of the specified database.

        Generates a new password and returns it in the response.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            database_id(str): Database identifier (long UUID)
        """
        endpoint = 'client/servers/{}/databases/{}/rotate-password'.format(
            server_id, database_id)
        response = self._api_request(endpoint=endpoint, mode='POST')
        return response

    def delete_database(self, server_id: str, database_id: str):
        """Deletes the specified database.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            database_id(str): Database identifier (long UUID)
        """
        endpoint = 'client/servers/{}/databases/{}'.format(server_id,
                                                           database_id)
        response = self._api_request(endpoint=endpoint, mode='DELETE')
        return response
