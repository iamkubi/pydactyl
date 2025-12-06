import unittest
from unittest import mock
import asyncio
from pydactyl.async_api_client import AsyncPterodactylClient

class AsyncStartupTests(unittest.TestCase):

    def setUp(self):
        self.api = AsyncPterodactylClient(url='https://dummy.com', api_key='dummy')

    def test_list_variables(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'data': []})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.startup.list_variables('uuid')
                
                args, _ = mock_get.call_args
                self.assertIn('client/servers/uuid/startup', args[0])

        asyncio.run(run_test())

    def test_update_variable(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.put') as mock_put:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={})
                mock_response.status = 200
                mock_put.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.startup.update_variable('uuid', 'VAR', 'VAL')
                
                args, kwargs = mock_put.call_args
                self.assertIn('client/servers/uuid/startup/variable', args[0])
                self.assertEqual(kwargs['json']['key'], 'VAR')
                self.assertEqual(kwargs['json']['value'], 'VAL')

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
