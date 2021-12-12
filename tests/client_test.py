import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from pydactyl import PterodactylClient
from pydactyl.exceptions import BadRequestError


class ClientTests(unittest.TestCase):

    def setUp(self):
        self.client = PterodactylClient(url='dummy', api_key='dummy')

    def test_invalid_power_action_raises_exception(self):
        with self.assertRaises(BadRequestError):
            self.client.client.send_power_action(1, 'BADSIGNAL')

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_server(self, mock_api):
        expected = {
            'endpoint': 'client/servers/11',
        }
        self.client.client.get_server(11)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_server_utilization(self, mock_api):
        expected = {
            'endpoint': 'client/servers/22/resources',
        }
        self.client.client.get_server_utilization(22)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_send_console_command(self, mock_api):
        expected = {
            'endpoint': 'client/servers/33/command',
            'mode': 'POST',
            'data': {'command': 'say Test Command'},
            'json': False,
        }
        self.client.client.send_console_command(33, 'say Test Command')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_valid_power_action_valid_request(self, mock_api):
        expected = {
            'endpoint': 'client/servers/1/power',
            'mode': 'POST',
            'data': {'signal': 'start'},
            'json': False,
        }
        self.client.client.send_power_action(1, 'start')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_files(self, mock_api):
        expected = {
            'endpoint': 'client/servers/1/files/list',
            'params': {},
        }
        self.client.client.list_files(1)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_files_with_path(self, mock_api):
        expected = {
            'endpoint': 'client/servers/1/files/list',
            'params': {'directory': '/foo'}
        }
        self.client.client.list_files(1, '/foo')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_download_file(self, mock_api):
        expected = {
            'endpoint': 'client/servers/2/files/download',
            'params': {'file': 'backups/savegame.zip'},
        }
        self.client.client.download_file(2, 'backups/savegame.zip')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_rename_file(self, mock_api):
        expected = {
            'endpoint': 'client/servers/3/files/rename',
            'mode': 'PUT',
            'data': {'root': '/', 'files': [{'from': 'today.zip',
                                             'to': 'yesterday.zip'}]},
        }
        self.client.client.rename_file(3, 'today.zip', 'yesterday.zip')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_rename_file_with_root(self, mock_api):
        expected = {
            'endpoint': 'client/servers/3/files/rename',
            'mode': 'PUT',
            'data': {'root': 'backups',
                     'files': [{'from': 'today.zip',
                                'to': 'yesterday.zip'}]},
        }
        self.client.client.rename_file(3, 'today.zip', 'yesterday.zip',
                                       'backups')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_api_keys(self, mock_api):
        expected = {
            'endpoint': 'client/account/api-keys',
        }
        self.client.client.api_key_list()
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_create_api_key(self, mock_api):
        expected = {
            'endpoint': 'client/account/api-keys',
            'mode': 'POST',
            'data': {'description': 'Test key', 'allowed_ips': ["127.0.0.1"]},
        }
        self.client.client.api_key_create('Test key', ["127.0.0.1"])
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_delete_api_key(self, mock_api):
        expected = {
            'endpoint': 'client/account/api-keys/abc123',
            'mode': 'DELETE',
        }
        self.client.client.api_key_delete('abc123')
        mock_api.assert_called_with(**expected)


if __name__ == '__main__':
    unittest.main()
