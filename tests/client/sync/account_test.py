import unittest
from unittest import mock

from pydactyl import PterodactylClient


class AccountTests(unittest.TestCase):

    def setUp(self):
        self.api = PterodactylClient(url='dummy', api_key='dummy')

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_account(self, mock_api):
        expected = {
            'endpoint': 'client/account',
        }
        self.api.client.account.get_account()
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_2fa_setup_code(self, mock_api):
        expected = {
            'endpoint': 'client/account/two-factor',
        }
        self.api.client.account.get_2fa_setup_code()
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_enable_2fa(self, mock_api):
        expected = {
            'endpoint': 'client/account/two-factor',
            'mode': 'POST',
            'data': {'code': '123456'},
        }
        self.api.client.account.enable_2fa('123456')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_disable_2fa(self, mock_api):
        expected = {
            'endpoint': 'client/account/two-factor',
            'mode': 'DELETE',
            'data': {'password': '123456'},
        }
        self.api.client.account.disable_2fa('123456')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_update_email(self, mock_api):
        expected = {
            'endpoint': 'client/account/email',
            'mode': 'PUT',
            'data': {'email': 'me@me.com', 'password': 'hunter2'},
        }
        self.api.client.account.update_email('me@me.com', 'hunter2')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_update_password(self, mock_api):
        expected = {
            'endpoint': 'client/account/password',
            'mode': 'PUT',
            'data': {'current_password': 'hunter2', 'password': 'hunter3',
                     'password_confirmation': 'hunter3'},
        }
        self.api.client.account.update_password('hunter2', 'hunter3', 'hunter3')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_api_keys(self, mock_api):
        expected = {
            'endpoint': 'client/account/api-keys',
        }
        self.api.client.account.api_key_list()
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_create_api_key(self, mock_api):
        expected = {
            'endpoint': 'client/account/api-keys',
            'mode': 'POST',
            'data': {'description': 'Test key', 'allowed_ips': ["127.0.0.1"]},
        }
        self.api.client.account.api_key_create('Test key', ["127.0.0.1"])
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_delete_api_key(self, mock_api):
        expected = {
            'endpoint': 'client/account/api-keys/abc123',
            'mode': 'DELETE',
        }
        self.api.client.account.api_key_delete('abc123')
        mock_api.assert_called_with(**expected)


if __name__ == '__main__':
    unittest.main()
