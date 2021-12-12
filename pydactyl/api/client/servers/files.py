from pydactyl.api import base


class Files(base.PterodactylAPI):
    """Class for interacting with the Pterodactyl Client API."""

    def list_files(self, server_id, path=None):
        """List files belonging to specified server.

        Optionally specify a directory and only return results in the
        specified directory.  Directory is relative to the server's root.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            path(str): Path to list in (e.g. 'save_game')
        """
        params = {}
        endpoint = 'client/servers/%s/files/list' % server_id
        if path is not None:
            params = {'directory': path}
        response = self._api_request(endpoint=endpoint, params=params)
        return response

    def download_file(self, server_id, path):
        """Get a download link for the specified file on the specified server.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            path(str): URL encoded path to desired file (e.g. 'eula.txt')

        Returns:
            response(str): Signed URL to download file
        """
        endpoint = 'client/servers/%s/files/download' % server_id
        params = {'file': path}
        response = self._api_request(endpoint=endpoint, params=params)
        return response.get('attributes').get('url')

    def rename_file(self, server_id, old_name, new_name, root='/'):
        """Rename a file.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            old_name(str): Name of existing file to rename
            new_name(str): New filename
            root(str): Path to files, relative to server root
        """
        endpoint = 'client/servers/%s/files/rename' % server_id
        data = {'root': root, 'files': [{'from': old_name, 'to': new_name}]}
        response = self._api_request(endpoint=endpoint, mode='PUT', data=data)
        return response
