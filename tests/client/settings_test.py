import unittest
from unittest import mock

from pydactyl import PterodactylClient


class SettingsTests(unittest.TestCase):

    def setUp(self):
        self.api = PterodactylClient(url='dummy', api_key='dummy')

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_rename_server(self, mock_api):
        expected = {
            'endpoint': 'client/servers/f1d2s3/settings/rename',
            'mode': 'POST',
            'data': {'name': 'newname'},
        }
        self.api.client.servers.settings.rename_server('f1d2s3', 'newname')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_reinstall_server(self, mock_api):
        expected = {
            'endpoint': 'client/servers/f1d2s3/settings/reinstall',
            'mode': 'POST',
        }
        self.api.client.servers.settings.reinstall_server('f1d2s3')
        mock_api.assert_called_with(**expected)


if __name__ == '__main__':
    unittest.main()
