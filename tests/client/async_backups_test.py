import unittest
from unittest import mock
import asyncio
from pydactyl.async_api_client import AsyncPterodactylClient

class AsyncBackupsTests(unittest.TestCase):

    def setUp(self):
        self.api = AsyncPterodactylClient(url='https://dummy.com', api_key='dummy')

    def test_list_backups(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'data': []})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.backups.list_backups('fds173')
                
                args, _ = mock_get.call_args
                self.assertIn('client/servers/fds173/backups', args[0])

        asyncio.run(run_test())

    def test_create_backup(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'attributes': {'uuid': 'new_backup'}})
                mock_response.status = 200
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.backups.create_backup('fds173')
                
                args, kwargs = mock_post.call_args
                self.assertIn('client/servers/fds173/backups', args[0])

        asyncio.run(run_test())

    def test_get_backup_detail(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'attributes': {'uuid': 'backup_123'}})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.backups.get_backup_detail('fds173', 'backup_123')
                
                args, _ = mock_get.call_args
                self.assertIn('client/servers/fds173/backups/backup_123', args[0])

        asyncio.run(run_test())

    def test_get_backup_download(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'attributes': {'url': 'http://download'}})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.backups.get_backup_download('fds173', 'backup_123')
                
                args, _ = mock_get.call_args
                self.assertIn('client/servers/fds173/backups/backup_123/download', args[0])

        asyncio.run(run_test())

    def test_restore_backup(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={})
                mock_response.status = 200
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.backups.restore_backup('fds173', 'backup_123')
                
                args, kwargs = mock_post.call_args
                self.assertIn('client/servers/fds173/backups/backup_123/restore', args[0])

        asyncio.run(run_test())

    def test_delete_backup(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.delete') as mock_delete:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_delete.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.backups.delete_backup('fds173', 'backup_123')
                
                args, kwargs = mock_delete.call_args
                self.assertIn('client/servers/fds173/backups/backup_123', args[0])

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
