import unittest
from unittest import mock

from pydactyl import PterodactylClient


class StartupTests(unittest.TestCase):

    def setUp(self):
        self.api = PterodactylClient(url='dummy', api_key='dummy')

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_variables(self, mock_api):
        expected = {
            'endpoint': 'client/servers/srv123/startup',
        }
        self.api.client.servers.startup.list_variables('srv123')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_update_variable(self, mock_api):
        expected = {
            'endpoint': 'client/servers/srv123/startup/variable',
            'mode': 'PUT',
            'data': {'key': 'varname', 'value': 'someval'},
        }
        self.api.client.servers.startup.update_variable('srv123', 'varname',
                                                        'someval')
        mock_api.assert_called_with(**expected)


if __name__ == '__main__':
    unittest.main()
