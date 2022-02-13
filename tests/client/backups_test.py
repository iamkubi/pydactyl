import unittest
from unittest import mock

from pydactyl import PterodactylClient


class BackupsTests(unittest.TestCase):

    def setUp(self):
        self.api = PterodactylClient(url='dummy', api_key='dummy')

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_backups(self, mock_api):
        expected = {
            'endpoint': 'client/servers/fds173/backups',
        }
        self.api.client.servers.backups.list_backups('fds173')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_create_backup(self, mock_api):
        expected = {
            'endpoint': 'client/servers/abc123/backups',
            'mode': 'POST',
        }
        self.api.client.servers.backups.create_backup('abc123')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_backup_detail(self, mock_api):
        expected = {
            'endpoint': 'client/servers/abc123/backups/longid1111',
        }
        self.api.client.servers.backups.get_backup_detail('abc123',
                                                          'longid1111')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_backup_download(self, mock_api):
        expected = {
            'endpoint': 'client/servers/abc123/backups/longid1111/download',
        }
        self.api.client.servers.backups.get_backup_download('abc123',
                                                            'longid1111')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_delete_backup(self, mock_api):
        expected = {
            'endpoint': 'client/servers/abc123/backups/longid1111',
            'mode': 'DELETE',
        }
        self.api.client.servers.backups.delete_backup('abc123', 'longid1111')
        mock_api.assert_called_with(**expected)


if __name__ == '__main__':
    unittest.main()
