from pydactyl.api import base


class Backups(base.PterodactylAPI):
    """Pterodactyl Client Server Backups API."""

    def list_backups(self, server_id: str):
        """List files belonging to specified server.

        Optionally specify a directory and only return results in the
        specified directory.  Directory is relative to the server's root.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
        """
        endpoint = 'client/servers/{}/backups'.format(server_id)
        response = self._api_request(endpoint=endpoint)
        return response

    def create_backup(self, server_id: str):
        """Create a new backup of the specified server.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
        """
        endpoint = 'client/servers/{}/backups'.format(server_id)
        response = self._api_request(endpoint=endpoint, mode='POST')
        return response

    def get_backup_detail(self, server_id: str, backup_id: str):
        """Retrieves information about the specified backup.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            backup_id(str): Backup identifier (long UUID)
        """
        endpoint = 'client/servers/{}/backups/{}'.format(server_id, backup_id)
        response = self._api_request(endpoint=endpoint)
        return response

    def get_backup_download(self, server_id: str, backup_id: str):
        """Generates a download link for the specified backup.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            backup_id(str): Backup identifier (long UUID)
        """
        endpoint = 'client/servers/{}/backups/{}/download'.format(server_id,
                                                                  backup_id)
        response = self._api_request(endpoint=endpoint)
        return response

    def delete_backup(self, server_id: str, backup_id: str):
        """Deletes the specified backup.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            backup_id(str): Backup identifier (long UUID)
        """
        endpoint = 'client/servers/{}/backups/{}'.format(server_id, backup_id)
        response = self._api_request(endpoint=endpoint, mode='DELETE')
        return response
