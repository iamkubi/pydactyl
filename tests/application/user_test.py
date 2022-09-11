from unittest import main, mock, TestCase

from pydactyl import PterodactylClient
from pydactyl.exceptions import BadRequestError


class UserTests(TestCase):

    def setUp(self):
        self.client = PterodactylClient(url='dummy', api_key='dummy')

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_users(self, mock_api):
        expected = {
            'endpoint': 'application/users',
            'params': {},
        }
        self.client.user.list_users()
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_users_with_filter(self, mock_api):
        expected = {
            'endpoint': 'application/users',
            'params': {'filter[email]': 'best@test.com'}
        }
        self.client.user.list_users(email='best@test.com')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_users_with_multiple_filter_params(self, mock_api):
        expected = {
            'endpoint': 'application/users',
            'params': {'filter[email]': 'best@test.com',
                       'filter[username]': 'best'}
        }
        self.client.user.list_users(email='best@test.com', username='best')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_user_info_by_external_id(self, mock_api):
        expected = {
            'endpoint': 'application/users/external/11',
        }
        self.client.user.get_user_info(external_id=11)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_user_info_by_user_id(self, mock_api):
        expected = {
            'endpoint': 'application/users/22',
        }
        self.client.user.get_user_info(user_id=22)
        mock_api.assert_called_with(**expected)

    def test_get_user_info_raises_with_no_id(self):
        with self.assertRaises(BadRequestError):
            self.client.user.get_user_info()

    def test_get_user_info_raises_with_both_ids(self):
        with self.assertRaises(BadRequestError):
            self.client.user.get_user_info(user_id=1, external_id=2)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_delete_user_with_user_id(self, mock_api):
        expected = {
            'endpoint': 'application/users/77',
            'mode': 'DELETE',
        }
        self.client.user.delete_user(user_id=77)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_delete_user_with_external_id(self, mock_api):
        mock_api.return_value = {'attributes': {'id': 88}}
        expected = [mock.call(endpoint='application/users/external/11'),
                    mock.call(endpoint='application/users/88', mode='DELETE')]
        self.client.user.delete_user(external_id=11)
        mock_api.assert_has_calls(expected)

    def test_delete_user_raises_with_no_id(self):
        with self.assertRaises(BadRequestError):
            self.client.user.delete_user()

    def test_delete_user_raises_with_both_ids(self):
        with self.assertRaises(BadRequestError):
            self.client.user.delete_user(user_id=1, external_id=2)


if __name__ == '__main__':
    main()
