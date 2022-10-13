from unittest import main, mock, TestCase

from pydactyl import PterodactylClient
from pydactyl.exceptions import BadRequestError


class ServersTests(TestCase):

    def setUp(self):
        self.client = PterodactylClient(url='dummy', api_key='dummy')

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_servers(self, mock_api):
        expected = {
            'endpoint': 'application/servers',
            'includes': None,
            'params': None,
        }
        self.client.servers.list_servers()
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_server_info_by_external_id(self, mock_api):
        expected = {
            'endpoint': 'application/servers/external/11',
            'includes': None,
            'params': None,
        }
        self.client.servers.get_server_info(external_id=11)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_server_info_by_server_id(self, mock_api):
        expected = {
            'endpoint': 'application/servers/22',
            'includes': None,
            'params': None,
        }
        self.client.servers.get_server_info(server_id=22)
        mock_api.assert_called_with(**expected)

    def test_get_server_info_raises_with_no_id(self):
        with self.assertRaises(BadRequestError):
            self.client.servers.get_server_info()

    def test_get_server_info_raises_with_both_ids(self):
        with self.assertRaises(BadRequestError):
            self.client.servers.get_server_info(server_id=1, external_id=2)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_suspend_server(self, mock_api):
        expected = {
            'endpoint': 'application/servers/33/suspend',
            'mode': 'POST',
        }
        self.client.servers.suspend_server(server_id=33)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_unsuspend_server(self, mock_api):
        expected = {
            'endpoint': 'application/servers/44/unsuspend',
            'mode': 'POST',
        }
        self.client.servers.unsuspend_server(server_id=44)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_reinstall_server(self, mock_api):
        expected = {
            'endpoint': 'application/servers/55/reinstall',
            'mode': 'POST',
        }
        self.client.servers.reinstall_server(server_id=55)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_rebuild_server(self, mock_api):
        expected = {
            'endpoint': 'application/servers/66/rebuild',
            'mode': 'POST',
        }
        self.client.servers.rebuild_server(server_id=66)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_delete_server(self, mock_api):
        expected = {
            'endpoint': 'application/servers/77',
            'mode': 'DELETE',
        }
        self.client.servers.delete_server(server_id=77)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_force_delete_server(self, mock_api):
        expected = {
            'endpoint': 'application/servers/88/force',
            'mode': 'DELETE',
        }
        self.client.servers.delete_server(server_id=88, force=True)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_server_databases(self, mock_api):
        expected = {
            'endpoint': 'application/servers/99/databases',
            'includes': None,
            'params': None,
        }
        self.client.servers.list_server_databases(server_id=99)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_server_database_info(self, mock_api):
        expected = {
            'endpoint': 'application/servers/111/databases/5',
            'includes': None,
            'params': None,
        }
        self.client.servers.get_server_database_info(server_id=111,
                                                     database_id=5)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_create_server_database(self, mock_api):
        expected = {
            'endpoint': 'application/servers/222/databases',
            'mode': 'POST',
        }
        self.client.servers.create_server_database(server_id=222)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_delete_server_database(self, mock_api):
        expected = {
            'endpoint': 'application/servers/333/databases/6',
            'mode': 'DELETE',
        }
        self.client.servers.delete_server_database(server_id=333, database_id=6)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_reset_server_database_password(self, mock_api):
        expected = {
            'endpoint': 'application/servers/333/databases/6/reset-password',
            'mode': 'POST',
        }
        self.client.servers.reset_server_database_password(server_id=333,
                                                           database_id=6)
        mock_api.assert_called_with(**expected)

    def test_create_server_without_allocation_or_location_raises(self):
        with self.assertRaisesRegex(BadRequestError, 'default_allocation'):
            self.client.servers.create_server('test server', 1, 1, 1, 0, 0, 0)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_create_server_with_location(self, mock_api):
        self.client.servers.create_server('test server', 1, 2, 3, 4, 5, 6,
                                          location_ids=[7])
        mock_api.assert_called()

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_create_server_with_allocation(self, mock_api):
        self.client.servers.create_server('test server', 1, 2, 3, 4, 5, 6,
                                          default_allocation=1234)
        mock_api.assert_called()

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_update_server_build(self, mock_api):
        expected = {
            'endpoint': 'application/servers/42/build',
            'mode': 'PATCH',
            'data': {'allocation': 88,
                     'limits': {'memory': 1024, 'swap': 1, 'disk': 5000,
                                'cpu': 150, 'io': 500},
                     'feature_limits': {'databases': 3, 'allocations': 9,
                                        'backups': 2},
                     'add_allocations': 89,
                     'remove_allocations': 88,
                     'oom_disabled': True,
                     },
            'json': False,
        }
        self.client.servers.update_server_build(
            server_id=42, allocation_id=88, memory_limit=1024, swap_limit=1,
            disk_limit=5000, cpu_limit=150, io_limit=500, database_limit=3,
            allocation_limit=9, backup_limit=2, add_allocations=89,
            remove_allocations=88, oom_disabled=True)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_update_server_startup(self, mock_api):
        expected = {
            'endpoint': 'application/servers/11/startup',
            'mode': 'PATCH',
            'data': {'egg': 19, 'startup': 'startup.sh', 'image':
                'ghcr.io/image:tag', 'skip_scripts': False, 'environment': {}},
            'json': False}
        self.client.servers.update_server_startup(
            server_id=11, egg_id=19, docker_image='ghcr.io/image:tag',
            startup_cmd='startup.sh', skip_scripts=False)
        mock_api.assert_called_with(**expected)

if __name__ == '__main__':
    main()
