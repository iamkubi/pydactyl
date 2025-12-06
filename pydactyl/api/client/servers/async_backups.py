from pydactyl.api.async_base import AsyncPterodactylAPI

class AsyncBackups(AsyncPterodactylAPI):
    """Async Pterodactyl Client Server Backups API."""

    async def list_backups(self, server_id: str):
        """List files belonging to specified server."""
        endpoint = 'client/servers/{}/backups'.format(server_id)
        response = await self._api_request(endpoint=endpoint)
        return response

    async def create_backup(self, server_id: str):
        """Create a new backup of the specified server."""
        endpoint = 'client/servers/{}/backups'.format(server_id)
        response = await self._api_request(endpoint=endpoint, mode='POST')
        return response

    async def get_backup_detail(self, server_id: str, backup_id: str):
        """Retrieves information about the specified backup."""
        endpoint = 'client/servers/{}/backups/{}'.format(server_id, backup_id)
        response = await self._api_request(endpoint=endpoint)
        return response

    async def get_backup_download(self, server_id: str, backup_id: str):
        """Generates a download link for the specified backup."""
        endpoint = 'client/servers/{}/backups/{}/download'.format(server_id,
                                                                  backup_id)
        response = await self._api_request(endpoint=endpoint)
        return response

    async def restore_backup(self, server_id: str, backup_id: str):
        """Restores the specified backup."""
        endpoint = 'client/servers/{}/backups/{}/restore'.format(server_id,
                                                                 backup_id)
        response = await self._api_request(endpoint=endpoint, mode='POST')
        return response

    async def delete_backup(self, server_id: str, backup_id: str):
        """Deletes the specified backup."""
        endpoint = 'client/servers/{}/backups/{}'.format(server_id, backup_id)
        response = await self._api_request(endpoint=endpoint, mode='DELETE')
        return response
