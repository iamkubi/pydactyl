from unittest import main, mock, TestCase

from pydactyl import PterodactylClient


class NodesTests(TestCase):

    def setUp(self):
        self.client = PterodactylClient(url='dummy', api_key='dummy')

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_nodes(self, mock_api):
        expected = {
            'endpoint': 'application/nodes',
            'params': {},
        }
        self.client.nodes.list_nodes()
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_nodes_with_includes(self, mock_api):
        expected = {
            'endpoint': 'application/nodes',
            'params': {'include': 'location,other'},
        }
        self.client.nodes.list_nodes(include='location,other')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_node_details(self, mock_api):
        expected = {
            'endpoint': 'application/nodes/11',
        }
        self.client.nodes.get_node_details(11)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_node_config(self, mock_api):
        expected = {
            'endpoint': 'application/nodes/111/configuration',
        }
        self.client.nodes.get_node_config(111)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_create_node(self, mock_api):
        expected_data = {
            'name': 'Test-Name 1_2.3',
            'description': 'foo bar',
            'location_id': 1,
            'fqdn': 'server1.testy.com',
            'memory': 1024,
            'disk': 5000,
            'memory_overallocate': 0,
            'disk_overallocate': 0,
            'use_ssl': True,
            'behind_proxy': False,
            'daemon_base': '/srv/daemon-data',
            'daemon_sftp': 2022,
            'daemon_listen': 8080,
            'upload_size': 100,
            'public': True,
            'maintenance_mode': False,
        }

        self.client.nodes.create_node(**expected_data)
        del expected_data['use_ssl']
        expected_data['scheme'] = 'https'

        expected = {
            'endpoint': 'application/nodes',
            'mode': 'POST',
            'data': expected_data,
        }

        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_edit_node(self, mock_api):
        expected_data = {
            'name': 'nodey node',
            'description': 'does stuff',
            'location_id': 33,
            'fqdn': 'nodey.nodeynode.com',
            'memory': 1024,
            'disk': 5000,
            'memory_overallocate': 0,
            'disk_overallocate': 0,
            'use_ssl': True,
            'behind_proxy': False,
            'daemon_sftp': 2022,
            'daemon_listen': 8080,
            'upload_size': 222,
            'maintenance_mode': False,
        }

        self.client.nodes.edit_node(11, **expected_data)
        del expected_data['use_ssl']
        expected_data['scheme'] = 'https'

        expected = {
            'endpoint': 'application/nodes/11',
            'mode': 'PATCH',
            'data': expected_data,
        }

        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_node_allocations(self, mock_api):
        expected = {
            'endpoint': 'application/nodes/12/allocations',
        }
        self.client.nodes.list_node_allocations(12)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_create_allocation_single(self, mock_api):
        expected = {
            'endpoint': 'application/nodes/13/allocations',
            'mode': 'POST',
            'data': {'ip': '10.2.3.4', 'alias': '1.2.3.4', 'ports': ['5000']},
            'json': False,
        }
        self.client.nodes.create_allocations(13, '10.2.3.4', ['5000'],
                                             '1.2.3.4')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_create_allocation_multiple(self, mock_api):
        expected = {
            'endpoint': 'application/nodes/14/allocations',
            'mode': 'POST',
            'data': {'ip': '10.2.3.4', 'alias': '1.2.3.4', 'ports': ['5000',
                                                                     '5005']},
            'json': False,
        }
        self.client.nodes.create_allocations(14, '10.2.3.4', ['5000', '5005'],
                                             '1.2.3.4')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_create_allocation_without_alias(self, mock_api):
        expected = {
            'endpoint': 'application/nodes/15/allocations',
            'mode': 'POST',
            'data': {'ip': '1.2.3.4', 'ports': ['5001']},
            'json': False,
        }
        self.client.nodes.create_allocations(
            15, '1.2.3.4', ['5001'])
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_delete_allocation(self, mock_api):
        expected = {
            'endpoint': 'application/nodes/16/allocations/123',
            'mode': 'DELETE',
            'json': False,
        }
        self.client.nodes.delete_allocation(16, 123)
        mock_api.assert_called_with(**expected)


if __name__ == '__main__':
    main()
