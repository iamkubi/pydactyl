from pydactyl.api import base


class Backups(base.PterodactylAPI):
    """Pterodactyl Client Server Backups API."""

    def list_backups(self, server_id):
        """List files belonging to specified server.

        Optionally specify a directory and only return results in the
        specified directory.  Directory is relative to the server's root.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
        """
        endpoint = 'client/servers/{}/files/list'.format(server_id)
        response = self._api_request(endpoint=endpoint)
        return response

    def create_backup(self):
        """TODO"""
        pass

    def get_backup_detail(self, backup_id):
        """TODO"""
        pass

    def get_backup_download(self, backup_id):
        """TODO"""
        pass

    def delete_backup(self, backup_id):
        """TODO"""
        pass
