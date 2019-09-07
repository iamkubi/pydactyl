import unittest
from unittest import mock

from pydactyl import PterodactylClient


class LocationsTests(unittest.TestCase):

    def setUp(self):
        self.client = PterodactylClient(url='dummy', api_key='dummy')

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_locations_called(self, mock_api):
        expected = {
            'endpoint': 'application/locations',
        }
        self.client.locations.list_locations()
        mock_api.assert_called_with(**expected)
