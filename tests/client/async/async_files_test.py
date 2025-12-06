import unittest
from unittest import mock
import asyncio
from pydactyl.async_api_client import AsyncPterodactylClient

class AsyncFilesTests(unittest.TestCase):

    def setUp(self):
        self.api = AsyncPterodactylClient(url='https://dummy.com', api_key='dummy')

    def test_list_files(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'data': []})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.files.list_files('uuid', 'path/to/dir')
                
                args, kwargs = mock_get.call_args
                self.assertIn('client/servers/uuid/files/list', args[0])
                self.assertEqual(kwargs['params']['directory'], 'path/to/dir')

        asyncio.run(run_test())

    def test_download_file(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'attributes': {'url': 'http://download.url'}})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    url = await api.client.servers.files.download_file('uuid', 'file.txt')
                
                args, kwargs = mock_get.call_args
                self.assertIn('client/servers/uuid/files/download', args[0])
                self.assertEqual(kwargs['params']['file'], 'file.txt')
                self.assertEqual(url, 'http://download.url')

        asyncio.run(run_test())

    def test_get_file_contents(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value='content')
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.files.get_file_contents('uuid', 'file.txt')
                
                args, kwargs = mock_get.call_args
                self.assertIn('client/servers/uuid/files/contents', args[0])
                self.assertEqual(kwargs['params']['file'], 'file.txt')

        asyncio.run(run_test())

    def test_rename_file(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.put') as mock_put:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_put.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.files.rename_file('uuid', 'old.txt', 'new.txt')
                
                args, kwargs = mock_put.call_args
                self.assertIn('client/servers/uuid/files/rename', args[0])
                self.assertEqual(kwargs['json']['files'][0]['from'], 'old.txt')
                self.assertEqual(kwargs['json']['files'][0]['to'], 'new.txt')

        asyncio.run(run_test())

    def test_copy_file(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.files.copy_file('uuid', 'file.txt')
                
                args, kwargs = mock_post.call_args
                self.assertIn('client/servers/uuid/files/copy', args[0])
                self.assertEqual(kwargs['json']['location'], 'file.txt')

        asyncio.run(run_test())

    def test_write_file(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.files.write_file('uuid', 'file.txt', 'contents')
                
                args, kwargs = mock_post.call_args
                self.assertIn('client/servers/uuid/files/write', args[0])
                self.assertEqual(kwargs['params']['file'], 'file.txt')
                # For write_file, data is passed as 'data' not 'json' because data_as_json=False
                # However, mocks often capture arguments differently. 
                # Let's verify 'data' in kwargs explicitly if possible, or just checking call args.

        asyncio.run(run_test())
        
    def test_compress_files(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'attributes': {'name': 'archive.tar.gz'}})
                mock_response.status = 200
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.files.compress_files('uuid', ['file1.txt'])
                
                args, kwargs = mock_post.call_args
                self.assertIn('client/servers/uuid/files/compress', args[0])
                self.assertEqual(kwargs['json']['files'], ['file1.txt'])

        asyncio.run(run_test())

    def test_decompress_file(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.files.decompress_file('uuid', 'archive.tar.gz')
                
                args, kwargs = mock_post.call_args
                self.assertIn('client/servers/uuid/files/decompress', args[0])
                self.assertEqual(kwargs['json']['file'], 'archive.tar.gz')

        asyncio.run(run_test())

    def test_delete_files(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.files.delete_files('uuid', ['file1.txt'])
                
                args, kwargs = mock_post.call_args
                self.assertIn('client/servers/uuid/files/delete', args[0])
                self.assertEqual(kwargs['json']['files'], ['file1.txt'])

        asyncio.run(run_test())

    def test_create_folder(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.post') as mock_post:
                mock_response = mock.Mock()
                mock_response.status = 204
                mock_post.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.client.servers.files.create_folder('uuid', 'new_folder')
                
                args, kwargs = mock_post.call_args
                self.assertIn('client/servers/uuid/files/create-folder', args[0])
                self.assertEqual(kwargs['json']['name'], 'new_folder')

        asyncio.run(run_test())

    def test_get_upload_file_url(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'attributes': {'url': 'http://upload.url'}})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    url = await api.client.servers.files.get_upload_file_url('uuid')
                
                args, _ = mock_get.call_args
                self.assertIn('client/servers/uuid/files/upload', args[0])
                self.assertEqual(url, 'http://upload.url')

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
