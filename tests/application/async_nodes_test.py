import unittest
from unittest import mock
import asyncio
from pydactyl.async_api_client import AsyncPterodactylClient

class AsyncNodesTests(unittest.TestCase):

    def setUp(self):
        self.api = AsyncPterodactylClient(url='https://dummy.com', api_key='dummy')

    def test_list_nodes(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={
                    'data': [],
                    'meta': {'pagination': {'total': 0, 'count': 0, 'per_page': 10, 'current_page': 1, 'total_pages': 1}}
                })
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as client:
                    await client.nodes.list_nodes()
                
                args, _ = mock_get.call_args
                self.assertIn('application/nodes', args[0])

        asyncio.run(run_test())

    def test_get_node_config(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'config': 'yaml'})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as client:
                    await client.nodes.get_node_config(1)
                
                args, _ = mock_get.call_args
                self.assertIn('application/nodes/1/configuration', args[0])

        asyncio.run(run_test())

    def test_get_node_details(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'attributes': {'id': 1}})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as client:
                    await client.nodes.get_node_details(1)
                
                args, _ = mock_get.call_args
                self.assertIn('application/nodes/1', args[0])

        asyncio.run(run_test())

    def test_create_node(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'attributes': {'id': 1}})
                mock_response.status = 201
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as client:
                    await client.nodes.create_node(name='Test Node', description='Desc', location_id=1, fqdn='test.com', memory=1024, disk=5000)
                
                args, kwargs = mock_post.call_args
                self.assertIn('application/nodes', args[0])
                self.assertEqual(kwargs['json']['name'], 'Test Node')

        asyncio.run(run_test())

    def test_edit_node(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.patch') as mock_patch:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'attributes': {'id': 1}})
                mock_response.status = 200
                mock_patch.return_value.__aenter__.return_value = mock_response

                async with self.api as client:
                    await client.nodes.edit_node(
                        1, name='Updated Node', description='Desc', location_id=1,
                        fqdn='test.com', use_ssl=True, behind_proxy=False,
                        maintenance_mode=False, memory=1024,
                        memory_overallocate=0, disk=5000, disk_overallocate=0,
                        upload_size=100, daemon_sftp=2022, daemon_listen=8080
                    )
                
                args, kwargs = mock_patch.call_args
                self.assertIn('application/nodes/1', args[0])
                self.assertEqual(kwargs['json']['name'], 'Updated Node')

        asyncio.run(run_test())

    def test_delete_node(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.delete') as mock_delete:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_delete.return_value.__aenter__.return_value = mock_response

                async with self.api as client:
                    await client.nodes.delete_node(1)
                
                args, kwargs = mock_delete.call_args
                self.assertIn('application/nodes/1', args[0])

        asyncio.run(run_test())

    def test_list_node_allocations(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={
                    'data': [],
                    'meta': {'pagination': {'total': 0, 'count': 0, 'per_page': 10, 'current_page': 1, 'total_pages': 1}}
                })
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as client:
                    await client.nodes.list_node_allocations(1)
                
                args, _ = mock_get.call_args
                self.assertIn('application/nodes/1/allocations', args[0])

        asyncio.run(run_test())

    def test_create_allocations(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={})
                mock_response.status = 201
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as client:
                    await client.nodes.create_allocations(1, ip='1.2.3.4', ports=['25565'])
                
                args, kwargs = mock_post.call_args
                self.assertIn('application/nodes/1/allocations', args[0])

        asyncio.run(run_test())

    def test_delete_allocation(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.delete') as mock_delete:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_delete.return_value.__aenter__.return_value = mock_response

                async with self.api as client:
                    await client.nodes.delete_allocation(1, 5)
                
                args, kwargs = mock_delete.call_args
                self.assertIn('application/nodes/1/allocations/5', args[0])

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
