import unittest
from unittest import mock

from pydactyl import PterodactylClient


class UsersTests(unittest.TestCase):

    def setUp(self):
        self.api = PterodactylClient(url='dummy', api_key='dummy')

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_users(self, mock_api):
        expected = {
            'endpoint': 'client/servers/bofh44/users',
        }
        self.api.client.servers.users.list_users('bofh44')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_create_user(self, mock_api):
        expected = {
            'endpoint': 'client/servers/bofh44/users',
            'mode': 'POST',
            'data': {'email': 'noob@noob.noob', 'permissions': [
                'control.console'], 'username': 'test'}
        }
        self.api.client.servers.users.create_user(
            server_id='bofh44', email='noob@noob.noob',
            permissions=['control.console'], username='test')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_user(self, mock_api):
        expected = {
            'endpoint': 'client/servers/bofh44/users/longuuid',
        }
        self.api.client.servers.users.get_user('bofh44', 'longuuid')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_update_user(self, mock_api):
        expected = {
            'endpoint': 'client/servers/bofh44/users/longuuid',
            'mode': 'POST',
            'data': {'permissions': ['control.console']}
        }
        self.api.client.servers.users.update_user('bofh44', 'longuuid',
                                                  ['control.console'])
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_delete_user(self, mock_api):
        expected = {
            'endpoint': 'client/servers/bofh44/users/longuuid',
            'mode': 'DELETE',
        }
        self.api.client.servers.users.delete_user('bofh44', 'longuuid')
        mock_api.assert_called_with(**expected)


if __name__ == '__main__':
    unittest.main()
