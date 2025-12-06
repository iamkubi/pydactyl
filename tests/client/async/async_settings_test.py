import unittest
from unittest import mock
import asyncio
from pydactyl.async_api_client import AsyncPterodactylClient

class AsyncSettingsTests(unittest.TestCase):

    def setUp(self):
        self.api = AsyncPterodactylClient(url='https://dummy.com', api_key='dummy')

    def test_rename_server(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.settings.rename_server('uuid', 'new name', 'new desc')
                
                args, kwargs = mock_post.call_args
                self.assertIn('client/servers/uuid/settings/rename', args[0])
                self.assertEqual(kwargs['json']['name'], 'new name')
                self.assertEqual(kwargs['json']['description'], 'new desc')

        asyncio.run(run_test())

    def test_reinstall_server(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.settings.reinstall_server('uuid')
                
                args, _ = mock_post.call_args
                self.assertIn('client/servers/uuid/settings/reinstall', args[0])

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
