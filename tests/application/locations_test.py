from unittest import main, mock, TestCase

from pydactyl import PterodactylClient
from pydactyl.exceptions import BadRequestError


class LocationsTests(TestCase):

    def setUp(self):
        self.client = PterodactylClient(url='dummy', api_key='dummy')

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_locations(self, mock_api):
        expected = {
            'endpoint': 'application/locations',
            'includes': None,
            'params': None,
        }
        self.client.locations.list_locations()
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_location_info(self, mock_api):
        expected = {
            'endpoint': 'application/locations/11',
            'includes': None,
            'params': None,
        }
        self.client.locations.get_location_info(11)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_create_location(self, mock_api):
        expected = {
            'endpoint': 'application/locations',
            'mode': 'POST',
            'data': {'shortcode': 'eu.ams.1-2_3',
                     'description': 'Test Location'},
        }
        self.client.locations.create_location('eu.ams.1-2_3', 'Test Location')
        mock_api.assert_called_with(**expected)

    def test_edit_location_invalid_arguments(self):
        with self.assertRaises(BadRequestError):
            self.client.locations.edit_location(5)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_edit_location(self, mock_api):
        expected = {
            'endpoint': 'application/locations/33',
            'mode': 'PATCH',
            'data': {'shortcode': 'us.nyc.lvl3',
                     'description': 'Level3 NYC Server'},
        }
        self.client.locations.edit_location(33, shortcode='us.nyc.lvl3',
                                            description='Level3 NYC Server')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_delete_location(self, mock_api):
        expected = {
            'endpoint': 'application/locations/44',
            'mode': 'DELETE',
        }
        self.client.locations.delete_location(44)
        mock_api.assert_called_with(**expected)


if __name__ == '__main__':
    main()
