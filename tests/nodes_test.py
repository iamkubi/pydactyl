import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from pydactyl import PterodactylClient


class NodesTests(unittest.TestCase):

    def setUp(self):
        self.client = PterodactylClient(url='dummy', api_key='dummy')

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_nodes(self, mock_api):
        expected = {
            'endpoint': 'application/nodes',
        }
        self.client.nodes.list_nodes()
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_node_info(self, mock_api):
        expected = {
            'endpoint': 'application/nodes/11',
        }
        self.client.nodes.get_node_info(11)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_create_node(self, mock_api):
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


if __name__ == '__main__':
    unittest.main()
