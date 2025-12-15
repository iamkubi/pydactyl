import asyncio
import unittest
from unittest import mock
from pydactyl.api.client.servers.async_websocket_client import AsyncWebsocketClient
from pydactyl.async_api_client import AsyncPterodactylClient

class AsyncServersBaseTests(unittest.TestCase):

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

                async with self.api as api:
                    await api.client.servers.list_servers()
                
                args, _ = mock_get.call_args
                self.assertIn('client', args[0])

        asyncio.run(run_test())

    def test_get_server(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'object': 'server', 'attributes': {'identifier': 'uuid'}})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.get_server('uuid')
                
                args, _ = mock_get.call_args
                self.assertIn('client/servers/uuid', args[0])

        asyncio.run(run_test())

    def test_get_server_utilization(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'object': 'stats', 'attributes': {'memory': 1024}})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.get_server_utilization('uuid')
                
                args, _ = mock_get.call_args
                self.assertIn('client/servers/uuid/resources', args[0])

        asyncio.run(run_test())

    def test_send_console_command(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.send_console_command('uuid', 'say hello')
                
                args, kwargs = mock_post.call_args
                self.assertIn('client/servers/uuid/command', args[0])
                self.assertEqual(kwargs['json']['command'], 'say hello')

        asyncio.run(run_test())

    def test_send_power_action(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.send_power_action('uuid', 'start')
                
                args, kwargs = mock_post.call_args
                self.assertIn('client/servers/uuid/power', args[0])
                self.assertEqual(kwargs['json']['signal'], 'start')

        asyncio.run(run_test())

    def test_get_websocket(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'data': {'token': 'abc'}})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.get_websocket('uuid')
                
                args, _ = mock_get.call_args
                self.assertIn('client/servers/uuid/websocket', args[0])

        asyncio.run(run_test())

    def test_get_websocket_client(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'data': {'token': 'abc', 'socket': 'wss://test.com'}})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    ws_client = await api.client.servers.get_websocket_client('uuid')
                    
                self.assertIsInstance(ws_client, AsyncWebsocketClient)
                self.assertEqual(ws_client._token, 'abc')
                self.assertEqual(ws_client._url, 'wss://test.com')

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
