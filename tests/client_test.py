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


if __name__ == '__main__':
    unittest.main()
