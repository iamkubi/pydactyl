from unittest import main, mock, TestCase

from pydactyl import PterodactylClient


class NestsTests(TestCase):

    def setUp(self):
        self.client = PterodactylClient(url='dummy', api_key='dummy')

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_nests(self, mock_api):
        expected = {
            'endpoint': 'application/nests',
            'includes': None,
            'params': None,
        }
        self.client.nests.list_nests()
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_nests_with_includes(self, mock_api):
        expected = {
            'endpoint': 'application/nests',
            'includes': ['eggs', 'servers'],
            'params': None,
        }
        self.client.nests.list_nests(['eggs', 'servers'])
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def get_nest_info(self, mock_api):
        expected = {
            'endpoint': 'application/nests/11',
        }
        self.client.nests.get_nest_info(11)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def get_nest_info_with_include(self, mock_api):
        expected = {
            'endpoint': 'application/nests/11',
        }
        self.client.nests.get_nest_info(11, 'config')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_eggs_in_nest(self, mock_api):
        expected = {
            'endpoint': 'application/nests/22/eggs',
            'includes': None,
            'params': None,
        }
        self.client.nests.get_eggs_in_nest(22)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_eggs_in_nest_with_includes(self, mock_api):
        expected = {
            'endpoint': 'application/nests/22/eggs',
            'includes': ['nest', 'config'],
            'params': None,
        }
        self.client.nests.get_eggs_in_nest(22, ['nest', 'config'])
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_egg_info(self, mock_api):
        expected = {
            'endpoint': 'application/nests/33/eggs/44',
            'includes': None,
            'params': None,
        }
        self.client.nests.get_egg_info(33, 44)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_egg_info_with_includes(self, mock_api):
        expected = {
            'endpoint': 'application/nests/33/eggs/44',
            'includes': ('servers', 'config'),
            'params': None,
        }
        self.client.nests.get_egg_info(33, 44, ('servers', 'config'))
        mock_api.assert_called_with(**expected)


if __name__ == '__main__':
    main()
