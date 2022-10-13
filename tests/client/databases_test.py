import unittest
from unittest import mock

from pydactyl import PterodactylClient


class DatabasesTest(unittest.TestCase):

    def setUp(self):
        self.api = PterodactylClient(url='dummy', api_key='dummy')

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_databases(self, mock_api):
        expected = {
            'endpoint': 'client/servers/fds173/databases',
            'includes': None,
            'params': None,
        }
        self.api.client.servers.databases.list_databases('fds173')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_databases_with_passwords(self, mock_api):
        expected = {
            'endpoint': 'client/servers/fds173/databases',
            'includes': ['password'],
            'params': None,
        }
        self.api.client.servers.databases.list_databases('fds173',
                                                         include_passwords=True)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_create_database(self, mock_api):
        expected = {
            'endpoint': 'client/servers/fds173/databases',
            'mode': 'POST',
            'data': {'database': 'testdb', 'remote': '%'},
        }
        self.api.client.servers.databases.create_database('fds173', 'testdb')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_create_database_with_remote(self, mock_api):
        expected = {
            'endpoint': 'client/servers/fds173/databases',
            'mode': 'POST',
            'data': {'database': 'testdb', 'remote': '1.1.1.1'},
        }
        self.api.client.servers.databases.create_database('fds173', 'testdb',
                                                          '1.1.1.1')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_rotate_database_password(self, mock_api):
        expected = {
            'endpoint': 'client/servers/fds173/databases/longlong/rotate'
                        '-password',
            'mode': 'POST',
        }
        self.api.client.servers.databases.rotate_database_password('fds173',
                                                                   'longlong')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_delete_database(self, mock_api):
        expected = {
            'endpoint': 'client/servers/fds173/databases/longlong',
            'mode': 'DELETE',
        }
        self.api.client.servers.databases.delete_database('fds173', 'longlong')
        mock_api.assert_called_with(**expected)


if __name__ == '__main__':
    unittest.main()
