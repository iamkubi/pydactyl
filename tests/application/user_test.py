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
            'includes': None,
            'params': {},
        }
        self.client.user.list_users()
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_users_with_filter(self, mock_api):
        expected = {
            'endpoint': 'application/users',
            'includes': None,
            'params': {'filter[email]': 'best@test.com'}
        }
        self.client.user.list_users(email='best@test.com')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_users_with_multiple_filter_params(self, mock_api):
        expected = {
            'endpoint': 'application/users',
            'includes': None,
            'params': {'filter[email]': 'best@test.com',
                       'filter[uuid]': 2,
                       'filter[username]': 'best',
                       'filter[external_id]': 4}
        }
        self.client.user.list_users(email='best@test.com', uuid=2,
                                    username='best', external_id=4)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_users_with_multiple_filter_params_and_includes(
            self, mock_api):
        expected = {
            'endpoint': 'application/users',
            'params': {'filter[email]': 'best@test.com',
                       'filter[username]': 'best',
                       'per_page': 300},
            'includes': ['servers', 'databases']
        }
        self.client.user.list_users(
            email='best@test.com', username='best', params={'per_page': 300},
            includes=['servers', 'databases'])
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_users_with_one_param_no_filters(
            self, mock_api):
        expected = {
            'endpoint': 'application/users',
            'includes': None,
            'params': {'per_page': 300},
        }
        self.client.user.list_users(params={'per_page': 300})
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_user_info_by_external_id(self, mock_api):
        expected = {
            'endpoint': 'application/users/external/11',
            'includes': None,
            'params': None,
        }
        self.client.user.get_user_info(external_id=11)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_user_info_by_user_id(self, mock_api):
        expected = {
            'endpoint': 'application/users/22',
            'includes': None,
            'params': None,
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

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_create_user(self, mock_api):
        expected = {
            'endpoint': 'application/users',
            'mode': 'POST',
            'data': {'username': 'best', 'email': 'best@test.com',
                     'first_name': 'first', 'last_name': 'last',
                     'external_id': 42,
                     'password': 'hunter2', 'root_admin': True, 'language': 'en'
             },
        }
        self.client.user.create_user(
            username='best', email='best@test.com', first_name='first',
            last_name='last', external_id=42, password='hunter2',
            root_admin=True, language='en')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_edit_user(self, mock_api):
        expected = {
            'endpoint': 'application/users/11',
            'mode': 'PATCH',
            'data': {'username': 'best', 'email': 'best@test.com',
                     'first_name': 'first', 'last_name': 'last',
                     'external_id': 43,
                     'password': 'hunter2', 'root_admin': False, 'language':
                         'en'
             },
        }
        self.client.user.edit_user(
            user_id=11, username='best', email='best@test.com',
            first_name='first', last_name='last', external_id=43,
            password='hunter2', root_admin=False, language='en')
        mock_api.assert_called_with(**expected)


if __name__ == '__main__':
    main()
