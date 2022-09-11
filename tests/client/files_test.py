import unittest
from unittest import mock

from pydactyl import PterodactylClient


class FilesTest(unittest.TestCase):

    def setUp(self):
        self.api = PterodactylClient(url='dummy', api_key='dummy')

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_files(self, mock_api):
        expected = {
            'endpoint': 'client/servers/gudsrvr/files/list',
            'params': {},
        }
        self.api.client.servers.files.list_files('gudsrvr')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_files_with_path(self, mock_api):
        expected = {
            'endpoint': 'client/servers/gudsrvr/files/list',
            'params': {'directory': 'saves/backups/'},
        }
        self.api.client.servers.files.list_files('gudsrvr', 'saves/backups/')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_download_file(self, mock_api):
        expected = {
            'endpoint': 'client/servers/gudsrvr/files/download',
            'params': {'file': 'backups/today.zip'},
        }
        self.api.client.servers.files.download_file('gudsrvr',
                                                    'backups/today.zip')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_file_contents(self, mock_api):
        expected = {
            'endpoint': 'client/servers/gudsrvr/files/contents',
            'params': {'file': 'backups/today.zip'},
        }
        self.api.client.servers.files.get_file_contents('gudsrvr',
                                                        'backups/today.zip')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_rename_file(self, mock_api):
        expected = {
            'endpoint': 'client/servers/gudsrvr/files/rename',
            'mode': 'PUT',
            'data': {'root': '/', 'files': [{'from': 'old.txt',
                                             'to': 'new.txt'}]},
        }
        self.api.client.servers.files.rename_file('gudsrvr', 'old.txt',
                                                  'new.txt')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_rename_file_with_root(self, mock_api):
        expected = {
            'endpoint': 'client/servers/gudsrvr/files/rename',
            'mode': 'PUT',
            'data': {'root': 'backups', 'files': [{'from': 'today.zip',
                                                   'to': 'yesterday.zip'}]},
        }
        self.api.client.servers.files.rename_file('gudsrvr', 'today.zip',
                                                  'yesterday.zip', 'backups')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_copy_file(self, mock_api):
        expected = {
            'endpoint': 'client/servers/gudsrvr/files/copy',
            'mode': 'POST',
            'data': {'location': 'config.json'},
        }
        self.api.client.servers.files.copy_file('gudsrvr', 'config.json')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_write_file(self, mock_api):
        expected = {
            'endpoint': 'client/servers/gudsrvr/files/write',
            'mode': 'POST',
            'params': {'file': 'eula.txt'},
            'data': 'All your base are belong to us',
            'data_as_json': False,
            'override_headers': {'Content-Type': 'application/text'},
        }
        self.api.client.servers.files.write_file(
            'gudsrvr', 'eula.txt', 'All your base are belong to us')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_compress_files(self, mock_api):
        expected = {
            'endpoint': 'client/servers/gudsrvr/files/compress',
            'mode': 'POST',
            'data': {'root': '/', 'files': ['game.map', 'game.save']},
        }
        self.api.client.servers.files.compress_files(
            'gudsrvr', ['game.map', 'game.save'])
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_compress_files_with_path(self, mock_api):
        expected = {
            'endpoint': 'client/servers/gudsrvr/files/compress',
            'mode': 'POST',
            'data': {'root': 'backups', 'files': ['today.zip',
                                                  'yesterday.zip']},
        }
        self.api.client.servers.files.compress_files(
            'gudsrvr', ['today.zip', 'yesterday.zip'], 'backups')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_decompress_files(self, mock_api):
        expected = {
            'endpoint': 'client/servers/gudsrvr/files/decompress',
            'mode': 'POST',
            'data': {'root': '/', 'file': 'backup.tar.gz'},
        }
        self.api.client.servers.files.decompress_file(
            'gudsrvr', 'backup.tar.gz')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_decompress_files_with_path(self, mock_api):
        expected = {
            'endpoint': 'client/servers/gudsrvr/files/decompress',
            'mode': 'POST',
            'data': {'root': 'gamefiles', 'file': 'backup.tar.gz'},
        }
        self.api.client.servers.files.decompress_file(
            'gudsrvr', 'backup.tar.gz', 'gamefiles')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_delete_files(self, mock_api):
        expected = {
            'endpoint': 'client/servers/gudsrvr/files/delete',
            'mode': 'POST',
            'data': {'root': '/', 'files': ['oldbackup.zip', 'oldconfig.txt']},
        }
        self.api.client.servers.files.delete_files(
            'gudsrvr', ['oldbackup.zip', 'oldconfig.txt'])
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_delete_files_with_path(self, mock_api):
        expected = {
            'endpoint': 'client/servers/gudsrvr/files/delete',
            'mode': 'POST',
            'data': {'root': 'savegames', 'files': ['save1', 'save2']},
        }
        self.api.client.servers.files.delete_files(
            'gudsrvr', ['save1', 'save2'], 'savegames')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_create_folder(self, mock_api):
        expected = {
            'endpoint': 'client/servers/gudsrvr/files/create-folder',
            'mode': 'POST',
            'data': {'root': '/', 'name': 'folders_and_dirs_are_not_the_same'},
        }
        self.api.client.servers.files.create_folder(
            'gudsrvr', 'folders_and_dirs_are_not_the_same')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_create_folder_with_path(self, mock_api):
        expected = {
            'endpoint': 'client/servers/gudsrvr/files/create-folder',
            'mode': 'POST',
            'data': {'root': 'backups', 'name': 'archived'},
        }
        self.api.client.servers.files.create_folder(
            'gudsrvr', 'archived', 'backups')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_upload_file_url(self, mock_api):
        expected = {
            'endpoint': 'client/servers/gudsrvr/files/upload',
        }
        self.api.client.servers.files.get_upload_file_url('gudsrvr')
        mock_api.assert_called_with(**expected)


if __name__ == '__main__':
    unittest.main()
