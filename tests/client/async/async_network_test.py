import unittest
from unittest import mock
import asyncio
from pydactyl.async_api_client import AsyncPterodactylClient

class AsyncNetworkTests(unittest.TestCase):

    def setUp(self):
        self.api = AsyncPterodactylClient(url='https://dummy.com', api_key='dummy')

    def test_list_allocations(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'data': []})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.network.list_allocations('uuid')
                
                args, _ = mock_get.call_args
                self.assertIn('client/servers/uuid/network/allocations', args[0])

        asyncio.run(run_test())

    def test_assign_allocation(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={})
                mock_response.status = 200
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.network.assign_allocation('uuid')
                
                args, _ = mock_post.call_args
                self.assertIn('client/servers/uuid/network/allocations', args[0])

        asyncio.run(run_test())

    def test_set_allocation_note(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={})
                mock_response.status = 200
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.network.set_allocation_note('uuid', 1, 'note')
                
                args, kwargs = mock_post.call_args
                self.assertIn('client/servers/uuid/network/allocations/1', args[0])
                self.assertEqual(kwargs['json']['notes'], 'note')

        asyncio.run(run_test())

    def test_set_primary_allocation(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={})
                mock_response.status = 200
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.network.set_primary_allocation('uuid', 1)
                
                args, _ = mock_post.call_args
                self.assertIn('client/servers/uuid/network/allocations/1/primary', args[0])

        asyncio.run(run_test())

    def test_unassign_allocation(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.delete') as mock_delete:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_delete.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.network.unassign_allocation('uuid', 1)
                
                args, _ = mock_delete.call_args
                self.assertIn('client/servers/uuid/network/allocations/1', args[0])

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
