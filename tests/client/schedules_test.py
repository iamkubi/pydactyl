import unittest
from unittest import mock

from pydactyl import PterodactylClient


class SchedulesTests(unittest.TestCase):

    def setUp(self):
        self.api = PterodactylClient(url='dummy', api_key='dummy')

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_list_schedules(self, mock_api):
        expected = {
            'endpoint': 'client/servers/srv123/schedules',
        }
        self.api.client.servers.schedules.list_schedules('srv123')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_create_schedule(self, mock_api):
        expected = {
            'endpoint': 'client/servers/srv123/schedules',
            'mode': 'POST',
            'data': {'name': 'test', 'minute': '*', 'hour': '1',
                     'day_of_week': 'pants', 'day_of_month': 'doggo',
                     'month': 'may', 'only_when_online': False,
                     'is_active': True},
        }
        self.api.client.servers.schedules.create_schedule(
            'srv123', 'test', '*', '1', 'pants', 'doggo', 'may')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_get_schedule_details(self, mock_api):
        expected = {
            'endpoint': 'client/servers/srv123/schedules/3',
        }
        self.api.client.servers.schedules.get_schedule_details('srv123', 3)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_update_schedule(self, mock_api):
        expected = {
            'endpoint': 'client/servers/srv123/schedules/4',
            'mode': 'POST',
            'data': {'name': 'test', 'minute': '*', 'hour': '1',
                     'day_of_week': 'pants', 'day_of_month': 'doggo',
                     'month': 'may', 'only_when_online': False,
                     'is_active': True},
        }
        self.api.client.servers.schedules.update_schedule(
            'srv123', 4, 'test', '*', '1', 'pants', 'doggo', 'may')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_delete_schedule(self, mock_api):
        expected = {
            'endpoint': 'client/servers/srv123/schedules/5',
            'mode': 'DELETE',
        }
        self.api.client.servers.schedules.delete_schedule('srv123', 5)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_create_task(self, mock_api):
        expected = {
            'endpoint': 'client/servers/srv123/schedules/5/tasks',
            'mode': 'POST',
            'data': {'action': 'command', 'payload': 'say Hello World',
                     'time_offset': '6', 'continue_on_failure': False}
        }
        self.api.client.servers.schedules.create_task('srv123', 5, 'command',
                                                      'say Hello World', '6')
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_update_task(self, mock_api):
        expected = {
            'endpoint': 'client/servers/srv123/schedules/5/tasks/4',
            'mode': 'POST',
            'data': {'action': 'command', 'payload': 'say Hello World',
                     'time_offset': '6', 'continue_on_failure': True}
        }
        self.api.client.servers.schedules.update_task('srv123', 5, 4, 'command',
                                                      'say Hello World', '6',
                                                      True)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_delete_task(self, mock_api):
        expected = {
            'endpoint': 'client/servers/srv123/schedules/5/tasks/4',
            'mode': 'DELETE',
        }
        self.api.client.servers.schedules.delete_task('srv123', 5, 4)
        mock_api.assert_called_with(**expected)

    @mock.patch('pydactyl.api.base.PterodactylAPI._api_request')
    def test_run_schedule(self, mock_api):
        expected = {
            'endpoint': 'client/servers/srv123/schedules/7/execute',
            'mode': 'POST',
        }
        self.api.client.servers.schedules.run_schedule('srv123', 7)
        mock_api.assert_called_with(**expected)
        

if __name__ == '__main__':
    unittest.main()
