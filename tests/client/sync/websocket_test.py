import unittest
from unittest import mock
from pydactyl.api.client.servers.websocket_client import WebsocketClient

class WebsocketTests(unittest.TestCase):

    def setUp(self):
        self.url = 'wss://dummy.com'
        self.token = 'dummy_token'
        self.ws_client = WebsocketClient(self.url, self.token)

    def test_connect_and_authenticate(self):
        with mock.patch('websocket.create_connection') as mock_create_connection:
            mock_ws = mock.Mock()
            mock_create_connection.return_value = mock_ws
            
            self.ws_client.connect()
            
            mock_create_connection.assert_called_with(self.url)
            expected_auth = '{"event": "auth", "args": ["dummy_token"]}'
            
            mock_ws.send.assert_called_with(expected_auth)

    def test_send_command(self):
        self.ws_client._ws = mock.Mock()
        self.ws_client.send_command('help')
        
        expected_payload = '{"event": "send command", "args": ["help"]}'
        self.ws_client._ws.send.assert_called_with(expected_payload)

    def test_send_power_action(self):
        self.ws_client._ws = mock.Mock()
        self.ws_client.send_power_action('start')
        
        expected_payload = '{"event": "set state", "args": ["start"]}'
        self.ws_client._ws.send.assert_called_with(expected_payload)
    
    def test_listen(self):
        mock_ws = mock.Mock()
        # Mock receiving messages
        mock_ws.recv.side_effect = [
            '{"event": "console output", "args": ["line 1"]}',
            '{"event": "console output", "args": ["line 2"]}',
            None # Ends the loop
        ]
        
        self.ws_client._ws = mock_ws
        
        messages = []
        for msg in self.ws_client.listen():
            messages.append(msg)
        
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['args'][0], 'line 1')
        self.assertEqual(messages[1]['args'][0], 'line 2')

    def test_context_manager(self):
        with mock.patch('websocket.create_connection') as mock_create_connection:
            mock_ws = mock.Mock()
            mock_create_connection.return_value = mock_ws
            
            with self.ws_client as ws:
                self.assertIsNotNone(ws._ws)
                
            # Should close on exit
            mock_ws.close.assert_called()

    def test_token_refresh(self):
        mock_refresher = mock.Mock()
        mock_refresher.return_value = {'data': {'token': 'new_token'}}
        
        self.ws_client._token_refresher = mock_refresher
        mock_ws = mock.Mock()
        
        mock_ws.recv.side_effect = [
            '{"event": "token expiring"}',
            '{"event": "auth success"}',
            None # Ends the loop
        ]
        
        self.ws_client._ws = mock_ws
        
        messages = []
        for msg in self.ws_client.listen():
            messages.append(msg)
            
        mock_refresher.assert_called_once()
        self.assertEqual(self.ws_client._token, 'new_token')
        
        expected_auth_payload = '{"event": "auth", "args": ["new_token"]}'
        mock_ws.send.assert_called_with(expected_auth_payload)
        
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['event'], 'token expiring')
        self.assertEqual(messages[1]['event'], 'auth success')

if __name__ == '__main__':
    unittest.main()
