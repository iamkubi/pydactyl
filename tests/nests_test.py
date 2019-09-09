import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from pydactyl import PterodactylClient


class NestsTests(unittest.TestCase):

    def setUp(self):
        self.client = PterodactylClient(url='dummy', api_key='dummy')

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_nests(self, mock_api):
        expected = {
            'endpoint': 'application/nests',
        }
        self.client.nests.list_nests()
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def get_nest_info(self, mock_api):
        expected = {
            'endpoint': 'application/nests/11',
        }
        self.client.nests.get_nest_info(11)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_eggs_in_nest(self, mock_api):
        expected = {
            'endpoint': 'application/nests/22/eggs',
        }
        self.client.nests.get_eggs_in_nest(22)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_egg_info(self, mock_api):
        expected = {
            'endpoint': 'application/nests/33/eggs/44',
        }
        self.client.nests.get_egg_info(33, 44)
        mock_api.assert_called_with(**expected)


if __name__ == '__main__':
    unittest.main()
