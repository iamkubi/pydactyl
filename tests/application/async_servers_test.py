import unittest
from unittest import mock
import asyncio
from pydactyl.async_api_client import AsyncPterodactylClient

class AsyncServersTests(unittest.TestCase):

    def setUp(self):
        self.api = AsyncPterodactylClient(url='https://dummy.com', api_key='dummy')

    def test_list_servers(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={
                    'object': 'list',
                    'data': [],
                    'meta': {'pagination': {'total': 0, 'count': 0, 'per_page': 10, 'current_page': 1, 'total_pages': 1}}
                })
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as client:
                    await client.servers.list_servers()
                
                args, _ = mock_get.call_args
                self.assertIn('application/servers', args[0])

        asyncio.run(run_test())

    def test_get_server_info(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'object': 'server', 'attributes': {'id': 1}})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as client:
                    await client.servers.get_server_info(1)
                
                args, _ = mock_get.call_args
                self.assertIn('application/servers/1', args[0])

        asyncio.run(run_test())

    def test_suspend_server(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as client:
                    await client.servers.suspend_server(1)
                
                args, kwargs = mock_post.call_args
                self.assertIn('application/servers/1/suspend', args[0])

        asyncio.run(run_test())

    def test_unsuspend_server(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as client:
                    await client.servers.unsuspend_server(1)
                
                args, kwargs = mock_post.call_args
                self.assertIn('application/servers/1/unsuspend', args[0])

        asyncio.run(run_test())

    def test_reinstall_server(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as client:
                    await client.servers.reinstall_server(1)
                
                args, kwargs = mock_post.call_args
                self.assertIn('application/servers/1/reinstall', args[0])

        asyncio.run(run_test())

    def test_rebuild_server(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as client:
                    await client.servers.rebuild_server(1)
                
                args, kwargs = mock_post.call_args
                self.assertIn('application/servers/1/rebuild', args[0])

        asyncio.run(run_test())

    def test_delete_server(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.delete') as mock_delete:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_delete.return_value.__aenter__.return_value = mock_response

                async with self.api as client:
                    await client.servers.delete_server(1)
                
                args, kwargs = mock_delete.call_args
                self.assertIn('application/servers/1', args[0])

        asyncio.run(run_test())

    def test_create_server(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post, \
                 mock.patch('aiohttp.ClientSession.get') as mock_get:
                
                # Mock egg info request
                mock_egg_response = mock.Mock()
                mock_egg_response.json = mock.AsyncMock(return_value={
                    'attributes': {
                        'docker_image': 'image',
                        'startup': 'cmd',
                        'relationships': {'variables': {'data': []}}
                    }
                })
                mock_egg_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_egg_response

                # Mock create server request
                mock_create_response = mock.Mock()
                mock_create_response.json = mock.AsyncMock(return_value={'object': 'server', 'attributes': {'id': 1}})
                mock_create_response.status = 201
                mock_post.return_value.__aenter__.return_value = mock_create_response

                async with self.api as client:
                    await client.servers.create_server(
                        name='Test Server', user_id=1, nest_id=1, egg_id=1,
                        memory_limit=1024, swap_limit=0, disk_limit=5000,
                        default_allocation=1
                    )
                
                args, kwargs = mock_post.call_args
                self.assertIn('application/servers', args[0])
                self.assertEqual(kwargs['json']['name'], 'Test Server')

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
