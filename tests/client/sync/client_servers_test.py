import unittest
from unittest import mock

from pydactyl import PterodactylClient
from pydactyl.exceptions import BadRequestError


class ClientServersTests(unittest.TestCase):

    def setUp(self):
        self.api = PterodactylClient(url='dummy', api_key='dummy')
    def test_invalid_power_action_raises_exception(self):
        with self.assertRaises(BadRequestError):
            self.api.client.servers.send_power_action(1, 'BADSIGNAL')

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_servers(self, mock_api):
        expected = {
            'endpoint': 'client',
            'includes': ('egg', 'subusers'),
            'params': {'per_page': 800},
        }
        self.api.client.servers.list_servers(includes=('egg','subusers'),
                                             params={'per_page': 800})
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_permissions(self, mock_api):
        expected = {
            'endpoint': 'client/permissions',
        }
        self.api.client.servers.list_permissions()
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_server(self, mock_api):
        expected = {
            'endpoint': 'client/servers/11',
            'includes': None,
            'params': None,
        }
        self.api.client.servers.get_server(11)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_server_utilization(self, mock_api):
        expected = {
            'endpoint': 'client/servers/22/resources',
        }
        self.api.client.servers.get_server_utilization(22)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_send_console_command(self, mock_api):
        expected = {
            'endpoint': 'client/servers/33/command',
            'mode': 'POST',
            'data': {'command': 'say Test Command'},
            'json': False,
        }
        self.api.client.servers.send_console_command(33, 'say Test Command')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_valid_power_action_valid_request(self, mock_api):
        expected = {
            'endpoint': 'client/servers/1/power',
            'mode': 'POST',
            'data': {'signal': 'start'},
            'json': False,
        }
        self.api.client.servers.send_power_action(1, 'start')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_websocket(self, mock_api):
        expected = {
            'endpoint': 'client/servers/44/websocket',
            'mode': 'GET',
        }
        self.api.client.servers.get_websocket(44)
        mock_api.assert_called_with(**expected)


if __name__ == '__main__':
    unittest.main()
