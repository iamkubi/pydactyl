import unittest
from unittest import mock
import asyncio
from pydactyl.async_api_client import AsyncPterodactylClient

class AsyncUsersTests(unittest.TestCase):

    def setUp(self):
        self.api = AsyncPterodactylClient(url='https://dummy.com', api_key='dummy')

    def test_list_users(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'data': []})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.users.list_users('uuid')
                
                args, _ = mock_get.call_args
                self.assertIn('client/servers/uuid/users', args[0])

        asyncio.run(run_test())

    def test_create_user(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={})
                mock_response.status = 200
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.users.create_user('uuid', 'test@test.com', ['control.start'])
                
                args, kwargs = mock_post.call_args
                self.assertIn('client/servers/uuid/users', args[0])
                self.assertEqual(kwargs['json']['email'], 'test@test.com')

        asyncio.run(run_test())

    def test_get_user(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'object': 'user'})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.users.get_user('uuid', 'uid')
                
                args, _ = mock_get.call_args
                self.assertIn('client/servers/uuid/users/uid', args[0])

        asyncio.run(run_test())

    def test_update_user(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={})
                mock_response.status = 200
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.users.update_user('uuid', 'uid', ['control.stop'])
                
                args, kwargs = mock_post.call_args
                self.assertIn('client/servers/uuid/users/uid', args[0])
                self.assertEqual(kwargs['json']['permissions'], ['control.stop'])

        asyncio.run(run_test())

    def test_delete_user(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.delete') as mock_delete:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_delete.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.users.delete_user('uuid', 'uid')
                
                args, _ = mock_delete.call_args
                self.assertIn('client/servers/uuid/users/uid', args[0])

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
