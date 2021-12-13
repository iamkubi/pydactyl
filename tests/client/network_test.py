import unittest
from unittest import mock

from pydactyl import PterodactylClient


class NetworkTests(unittest.TestCase):

    def setUp(self):
        self.api = PterodactylClient(url='dummy', api_key='dummy')

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_allocations(self, mock_api):
        expected = {
            'endpoint': 'client/servers/notwork/network/allocations',
        }
        self.api.client.servers.network.list_allocations('notwork')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_assign_allocation(self, mock_api):
        expected = {
            'endpoint': 'client/servers/notwork/network/allocations',
            'mode': 'POST',
        }
        self.api.client.servers.network.assign_allocation('notwork')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_set_allocation_note(self, mock_api):
        expected = {
            'endpoint': 'client/servers/notwork/network/allocations/2',
            'mode': 'POST',
            'data': {'notes': 'some note'},
        }
        self.api.client.servers.network.set_allocation_note('notwork', 2,
                                                            'some note')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_set_primary_allocation(self, mock_api):
        expected = {
            'endpoint': 'client/servers/notwork/network/allocations/33/primary',
            'mode': 'POST',
        }
        self.api.client.servers.network.set_primary_allocation('notwork', 33)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_unassign_allocation(self, mock_api):
        expected = {
            'endpoint': 'client/servers/notwork/network/allocations/44',
            'mode': 'DELETE',
        }
        self.api.client.servers.network.unassign_allocation('notwork', 44)
        mock_api.assert_called_with(**expected)


if __name__ == '__main__':
    unittest.main()
