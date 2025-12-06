import unittest
from unittest import mock
import asyncio
from pydactyl.async_api_client import AsyncPterodactylClient

class AsyncUserTests(unittest.TestCase):

    def setUp(self):
        self.api = AsyncPterodactylClient(url='https://dummy.com', api_key='dummy')

    def test_list_users(self):
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
                    await client.user.list_users()
                
                args, _ = mock_get.call_args
                self.assertIn('application/users', args[0])

        asyncio.run(run_test())

    def test_get_user_info(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'object': 'user', 'attributes': {'id': 1}})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as client:
                    await client.user.get_user_info(1)
                
                args, _ = mock_get.call_args
                self.assertIn('application/users/1', args[0])

        asyncio.run(run_test())

    def test_create_user(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'object': 'user', 'attributes': {'id': 1}})
                mock_response.status = 201
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as client:
                    await client.user.create_user(username='user', email='test@test.com', first_name='Test', last_name='User')
                
                args, kwargs = mock_post.call_args
                self.assertIn('application/users', args[0])
                self.assertEqual(kwargs['json']['email'], 'test@test.com')

        asyncio.run(run_test())

    def test_edit_user(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.patch') as mock_patch:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'object': 'user', 'attributes': {'id': 1}})
                mock_response.status = 200
                mock_patch.return_value.__aenter__.return_value = mock_response

                async with self.api as client:
                    await client.user.edit_user(1, username='user', email='update@test.com', first_name='Test', last_name='User')
                
                args, kwargs = mock_patch.call_args
                self.assertIn('application/users/1', args[0])
                self.assertEqual(kwargs['json']['email'], 'update@test.com')

        asyncio.run(run_test())

    def test_delete_user(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.delete') as mock_delete:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_response.json = mock.AsyncMock(return_value={'object': 'user'})

                mock_delete.return_value.__aenter__.return_value = mock_response

                async with self.api as client:
                    await client.user.delete_user(1)
                
                args, kwargs = mock_delete.call_args
                self.assertIn('application/users/1', args[0])

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
