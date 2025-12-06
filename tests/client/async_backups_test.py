import unittest
from unittest import mock
import asyncio
from pydactyl.async_api_client import AsyncPterodactylClient

class AsyncBackupsTests(unittest.TestCase):

    def setUp(self):
        self.api = AsyncPterodactylClient(url='dummy', api_key='dummy')

    def test_list_backups(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'data': []})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.backups.list_backups('fds173')
                
                # Verify the call
                args, kwargs = mock_get.call_args
                self.assertIn('client/servers/fds173/backups', args[0])

        asyncio.run(run_test())



if __name__ == '__main__':
    unittest.main()
