from pydactyl.api import base


class Files(base.PterodactylAPI):
    """Class for interacting with the Pterodactyl Client API."""

    def list_files(self, server_id: str, path: str = None):
        """List files belonging to specified server.

        Optionally specify a directory and only return results in the
        specified directory.  Directory is relative to the server's root.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            path(str): Path to list in (e.g. 'save_game')
        """
        params = {}
        endpoint = 'client/servers/{}/files/list'.format(server_id)
        if path is not None:
            params = {'directory': path}
        response = self._api_request(endpoint=endpoint, params=params)
        return response

    def download_file(self, server_id: str, path: str) -> str:
        """Get a download link for the specified file on the specified server.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            path(str): URL encoded path to desired file (e.g. 'eula.txt')

        Returns:
            response(str): Signed URL to download file
        """
        endpoint = 'client/servers/{}/files/download'.format(server_id)
        params = {'file': path}
        response = self._api_request(endpoint=endpoint, params=params)
        return response.get('attributes').get('url')

    def get_file_contents(self, server_id: str, path: str) -> str:
        """Get contents of the specified file on the specified server.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            path(str): URL encoded path to desired file (e.g. 'eula.txt')
        """
        endpoint = 'client/servers/{}/files/contents'.format(server_id)
        params = {'file': path}
        response = self._api_request(endpoint=endpoint, params=params)
        return response

    def rename_file(self, server_id: str, old_name: str, new_name: str,
                    root: str = '/'):
        """Rename a file.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            old_name(str): Name of existing file to rename
            new_name(str): New filename
            root(str): Path to files, relative to server root
        """
        endpoint = 'client/servers/{}/files/rename'.format(server_id)
        data = {'root': root, 'files': [{'from': old_name, 'to': new_name}]}
        response = self._api_request(endpoint=endpoint, mode='PUT', data=data)
        return response

    def copy_file(self, server_id: str, path: str):
        """Makes a copy of a file.

        This is primarily used by the file manager.

        Makes a copy of the file with a unique name.  You cannot specify the
        new name of the file, it just picks one for you.  For example
        'test.txt' will have a copy created named 'test copy.txt'.  Running
        it again will create 'test copy 1.txt'.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            path(str): URL encoded path to desired file (e.g. 'eula.txt')
        """
        endpoint = 'client/servers/{}/files/copy'.format(server_id)
        data = {'location': path}
        response = self._api_request(endpoint=endpoint, mode='POST', data=data)
        return response

    def write_file(self, server_id: str, path: str, contents: str):
        """Writes contents to a file.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            path(str): Path to desired file (e.g. 'eula.txt')
            contents(str): Contents to write to the file.
        """
        params = {'file': path}
        endpoint = 'client/servers/{}/files/write'.format(server_id)
        response = self._api_request(
            endpoint=endpoint, mode='POST', params=params, data=contents,
            override_headers={'Content-Type': 'application/text'},
            data_as_json=False)
        return response

    def compress_files(self, server_id: str, files: iter, path: str = '/'):
        """Creates a compressed archive.

        Creates a tar.gz compressed file containing the listed files.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            files(iter): List of files to add to the archive
            path(str): Root path to create the archive from
        """
        data = {'root': path, 'files': files}
        endpoint = 'client/servers/{}/files/compress'.format(server_id)
        response = self._api_request(endpoint=endpoint, mode='POST',
                                     data=data)
        return response

    def decompress_file(self, server_id: str, file: str, path: str = '/'):
        """Decompresses an archive.

        Decompresses a compressed file to the specified path.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            file(str): Name of the archive file to decompress
            path(str): Root path to decompress in
        """
        data = {'root': path, 'file': file}
        endpoint = 'client/servers/{}/files/decompress'.format(server_id)
        response = self._api_request(endpoint=endpoint, mode='POST',
                                     data=data)
        return response

    def delete_files(self, server_id: str, files: iter, path: str = '/'):
        """Deletes the specified file(s) or directory(s).

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            files(iter): List of files to delete
            path(str): Root path look for files in
        """
        data = {'root': path, 'files': files}
        endpoint = 'client/servers/{}/files/delete'.format(server_id)
        response = self._api_request(endpoint=endpoint, mode='POST',
                                     data=data)
        return response

    def create_folder(self, server_id: str, name: str, path: str = '/'):
        """Creates the specified folder in the specified directory.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            name(str): Name of the directory to create
            path(str): Root path to create the directory in
        """
        data = {'root': path, 'name': name}
        endpoint = 'client/servers/{}/files/create-folder'.format(server_id)
        response = self._api_request(endpoint=endpoint, mode='POST',
                                     data=data)
        return response

    def get_upload_file_url(self, server_id: str) -> str:
        """Returns a signed URL used to upload files to the server using POST.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
        """
        endpoint = 'client/servers/{}/files/upload'.format(server_id)
        response = self._api_request(endpoint=endpoint)
        return response.get('attributes').get('url')
