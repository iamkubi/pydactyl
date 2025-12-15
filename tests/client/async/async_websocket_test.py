import aiohttp
import asyncio
import unittest
from unittest import mock
from pydactyl.api.client.servers.async_websocket_client import AsyncWebsocketClient

class AsyncWebsocketTests(unittest.TestCase):

    def setUp(self):
        self.url = 'wss://dummy.com'
        self.token = 'dummy_token'
        self.ws_client = AsyncWebsocketClient(self.url, self.token)

    def test_connect_and_authenticate(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.ws_connect', new_callable=mock.AsyncMock) as mock_ws_connect:
                mock_ws = mock.AsyncMock()
                mock_ws_connect.return_value = mock_ws
                
                await self.ws_client.connect()
                
                mock_ws_connect.assert_called_with(self.url)
                # Check authentication message
                expected_auth = {"event": "auth", "args": [self.token]}
                # The first send_json call should be auth
                args, _ = mock_ws.send_json.call_args
                self.assertEqual(args[0], expected_auth)

        asyncio.run(run_test())

    def test_send_command(self):
        async def run_test():
            self.ws_client._ws = mock.AsyncMock()
            await self.ws_client.send_command('help')
            
            expected_payload = {"event": "send", "args": ['help']}
            self.ws_client._ws.send_json.assert_called_with(expected_payload)

        asyncio.run(run_test())

    def test_send_power_action(self):
        async def run_test():
            self.ws_client._ws = mock.AsyncMock()
            await self.ws_client.send_power_action('start')
            
            expected_payload = {"event": "set state", "args": ['start']}
            self.ws_client._ws.send_json.assert_called_with(expected_payload)

        asyncio.run(run_test())
    
    def test_listen(self):
        async def run_test():
            mock_ws = mock.AsyncMock()
            msg1 = mock.Mock()
            msg1.type = aiohttp.WSMsgType.TEXT
            msg1.data = '{"event": "console output", "args": ["line 1"]}'
            
            msg2 = mock.Mock()
            msg2.type = aiohttp.WSMsgType.TEXT
            msg2.data = '{"event": "console output", "args": ["line 2"]}'
            
            # Make the mock iterable
            mock_ws.__aiter__.return_value = [msg1, msg2]
            
            self.ws_client._ws = mock_ws
            
            messages = []
            async for msg in self.ws_client.listen():
                messages.append(msg)
            
            self.assertEqual(len(messages), 2)
            self.assertEqual(messages[0]['args'][0], 'line 1')
            self.assertEqual(messages[1]['args'][0], 'line 2')

        asyncio.run(run_test())

    def test_context_manager(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.ws_connect', new_callable=mock.AsyncMock) as mock_ws_connect:
                mock_ws = mock.AsyncMock()
                mock_ws_connect.return_value = mock_ws
                
                async with self.ws_client as ws:
                    self.assertIsNotNone(ws._ws)
                    
                # Should close on exit
                mock_ws.close.assert_called()

        asyncio.run(run_test())

    def test_token_refresh(self):
        async def run_test():
            mock_refresher = mock.AsyncMock()
            mock_refresher.return_value = {'data': {'token': 'new_token'}}
            
            self.ws_client._token_refresher = mock_refresher
            self.ws_client._ws = mock.AsyncMock()
            
            msg1 = mock.Mock()
            msg1.type = aiohttp.WSMsgType.TEXT
            msg1.data = '{"event": "token expiring"}'
            
            msg2 = mock.Mock()
            msg2.type = aiohttp.WSMsgType.TEXT
            msg2.data = '{"event": "auth success"}'
            
            self.ws_client._ws.__aiter__.return_value = [msg1, msg2]
            
            messages = []
            async for msg in self.ws_client.listen():
                messages.append(msg)
                
            mock_refresher.assert_called_once()
            self.assertEqual(self.ws_client._token, 'new_token')
            expected_auth_payload = {"event": "auth", "args": ['new_token']}
            self.ws_client._ws.send_json.assert_any_call(expected_auth_payload)
            
            self.assertEqual(len(messages), 2)
            self.assertEqual(messages[0]['event'], 'token expiring')
            self.assertEqual(messages[1]['event'], 'auth success')

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
