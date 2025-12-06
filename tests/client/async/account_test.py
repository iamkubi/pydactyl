import unittest
from unittest import mock
import asyncio
from pydactyl.async_api_client import AsyncPterodactylClient

class AsyncAccountTests(unittest.TestCase):

    def setUp(self):
        self.api = AsyncPterodactylClient(url='https://dummy.com', api_key='dummy')

    def test_get_account(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'attributes': {'id': 1}})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.account.get_account()
                
                args, _ = mock_get.call_args
                self.assertIn('client/account', args[0])

        asyncio.run(run_test())

    def test_get_2fa_setup_code(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'data': 'qr_code'})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.account.get_2fa_setup_code()
                
                args, _ = mock_get.call_args
                self.assertIn('client/account/two-factor', args[0])

        asyncio.run(run_test())

    def test_enable_2fa(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={})
                mock_response.status = 200
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.account.enable_2fa('123456')
                
                args, kwargs = mock_post.call_args
                self.assertIn('client/account/two-factor', args[0])
                self.assertEqual(kwargs['json']['code'], '123456')

        asyncio.run(run_test())

    def test_disable_2fa(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.delete') as mock_delete:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={})
                mock_response.status = 200
                mock_delete.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.account.disable_2fa('password')
                
                args, kwargs = mock_delete.call_args
                self.assertIn('client/account/two-factor', args[0])
                self.assertEqual(kwargs['json']['password'], 'password')

        asyncio.run(run_test())

    def test_update_email(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.put') as mock_put:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={})
                mock_response.status = 200
                mock_put.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.account.update_email('new@test.com', 'password')
                
                args, kwargs = mock_put.call_args
                self.assertIn('client/account/email', args[0])
                self.assertEqual(kwargs['json']['email'], 'new@test.com')

        asyncio.run(run_test())

    def test_update_password(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.put') as mock_put:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={})
                mock_response.status = 200
                mock_put.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.account.update_password('curr', 'new', 'new')
                
                args, kwargs = mock_put.call_args
                self.assertIn('client/account/password', args[0])
                self.assertEqual(kwargs['json']['password'], 'new')

        asyncio.run(run_test())

    def test_api_key_list(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'object': 'list', 'data': []})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.account.api_key_list()
                
                args, _ = mock_get.call_args
                self.assertIn('client/account/api-keys', args[0])

        asyncio.run(run_test())

    def test_api_key_create(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={})
                mock_response.status = 200
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.account.api_key_create('desc', ['1.1.1.1'])
                
                args, kwargs = mock_post.call_args
                self.assertIn('client/account/api-keys', args[0])
                self.assertEqual(kwargs['json']['description'], 'desc')

        asyncio.run(run_test())

    def test_api_key_delete(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.delete') as mock_delete:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={})
                mock_response.status = 200
                mock_delete.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.account.api_key_delete('key_id')
                
                args, kwargs = mock_delete.call_args
                self.assertIn('client/account/api-keys/key_id', args[0])

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
