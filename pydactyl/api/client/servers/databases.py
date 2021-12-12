from pydactyl.api import base


class Databases(base.PterodactylAPI):
    """Pterodactyl Client Server Databases API."""

    def list_databases(self, server_id: str, include_passwords: bool = False):
        """List all databases for a server.

        Optionally includes the database user passwords.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            include_passwords(bool): True to include database user passwords
        """
        params = {}
        if include_passwords:
            params['include'] = 'passwords'
        endpoint = 'client/servers/{}/databases'.format(server_id)
        response = self._api_request(endpoint=endpoint, params=params)
        return response

    def create_database(self):
        """TODO"""
        pass

    def rotate_database_password(self):
        """TODO"""
        pass

    def delete_database(self, database_id):
        """TODO"""
        pass
