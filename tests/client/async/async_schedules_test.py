import unittest
from unittest import mock
import asyncio
from pydactyl.async_api_client import AsyncPterodactylClient

class AsyncSchedulesTests(unittest.TestCase):

    def setUp(self):
        self.api = AsyncPterodactylClient(url='https://dummy.com', api_key='dummy')

    def test_list_schedules(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'data': []})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.schedules.list_schedules('uuid')
                
                args, _ = mock_get.call_args
                self.assertIn('client/servers/uuid/schedules', args[0])

        asyncio.run(run_test())

    def test_create_schedule(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={})
                mock_response.status = 200
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.schedules.create_schedule('uuid', 'Test Schedule', '1', '1', '*', '*', '*')
                
                args, kwargs = mock_post.call_args
                self.assertIn('client/servers/uuid/schedules', args[0])
                self.assertEqual(kwargs['json']['name'], 'Test Schedule')

        asyncio.run(run_test())

    def test_get_schedule_details(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'object': 'schedule'})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.schedules.get_schedule_details('uuid', 1)
                
                args, _ = mock_get.call_args
                self.assertIn('client/servers/uuid/schedules/1', args[0])

        asyncio.run(run_test())

    def test_update_schedule(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={})
                mock_response.status = 200
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.schedules.update_schedule('uuid', 1, 'Updated Schedule', '1', '1', '*', '*', '*')
                
                args, kwargs = mock_post.call_args
                self.assertIn('client/servers/uuid/schedules/1', args[0])
                self.assertEqual(kwargs['json']['name'], 'Updated Schedule')

        asyncio.run(run_test())

    def test_delete_schedule(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.delete') as mock_delete:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_delete.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.schedules.delete_schedule('uuid', 1)
                
                args, _ = mock_delete.call_args
                self.assertIn('client/servers/uuid/schedules/1', args[0])

        asyncio.run(run_test())

    def test_create_task(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={})
                mock_response.status = 200
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.schedules.create_task('uuid', 1, 'command', 'say hello')
                
                args, kwargs = mock_post.call_args
                self.assertIn('client/servers/uuid/schedules/1/tasks', args[0])
                self.assertEqual(kwargs['json']['action'], 'command')

        asyncio.run(run_test())

    def test_update_task(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={})
                mock_response.status = 200
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.schedules.update_task('uuid', 1, 1, 'command', 'say hi')
                
                args, kwargs = mock_post.call_args
                self.assertIn('client/servers/uuid/schedules/1/tasks/1', args[0])
                self.assertEqual(kwargs['json']['payload'], 'say hi')

        asyncio.run(run_test())

    def test_delete_task(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.delete') as mock_delete:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_delete.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.schedules.delete_task('uuid', 1, 1)
                
                args, _ = mock_delete.call_args
                self.assertIn('client/servers/uuid/schedules/1/tasks/1', args[0])

        asyncio.run(run_test())

    def test_run_schedule(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.schedules.run_schedule('uuid', 1)
                
                args, _ = mock_post.call_args
                self.assertIn('client/servers/uuid/schedules/1/execute', args[0])

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
