import unittest
from unittest import mock
import asyncio
from pydactyl.async_api_client import AsyncPterodactylClient

class AsyncDatabasesTests(unittest.TestCase):

    def setUp(self):
        self.api = AsyncPterodactylClient(url='https://dummy.com', api_key='dummy')

    def test_list_databases(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'data': []})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.databases.list_databases('uuid')
                
                args, _ = mock_get.call_args
                self.assertIn('client/servers/uuid/databases', args[0])

        asyncio.run(run_test())

    def test_create_database(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={})
                mock_response.status = 200
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.databases.create_database('uuid', 'dbname')
                
                args, kwargs = mock_post.call_args
                self.assertIn('client/servers/uuid/databases', args[0])
                self.assertEqual(kwargs['json']['database'], 'dbname')

        asyncio.run(run_test())

    def test_rotate_database_password(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={})
                mock_response.status = 200
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.databases.rotate_database_password('uuid', 'dbid')
                
                args, _ = mock_post.call_args
                self.assertIn('client/servers/uuid/databases/dbid/rotate-password', args[0])

        asyncio.run(run_test())

    def test_delete_database(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.delete') as mock_delete:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_delete.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.databases.delete_database('uuid', 'dbid')
                
                args, _ = mock_delete.call_args
                self.assertIn('client/servers/uuid/databases/dbid', args[0])

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
