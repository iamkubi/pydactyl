import unittest
from unittest import mock
import asyncio
from pydactyl.async_api_client import AsyncPterodactylClient

class AsyncNestsTests(unittest.TestCase):

    def setUp(self):
        self.api = AsyncPterodactylClient(url='https://dummy.com', api_key='dummy')

    def test_list_nests(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={
                    'data': [],
                    'meta': {'pagination': {'total': 0, 'count': 0, 'per_page': 10, 'current_page': 1, 'total_pages': 1}}
                })
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.nests.list_nests()
                
                args, _ = mock_get.call_args
                self.assertIn('application/nests', args[0])

        asyncio.run(run_test())

    def test_get_nest_info(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'attributes': {'id': 1}})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.nests.get_nest_info(1)
                
                args, _ = mock_get.call_args
                self.assertIn('application/nests/1', args[0])

        asyncio.run(run_test())

    def test_get_eggs_in_nest(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'data': []})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.nests.get_eggs_in_nest(1)
                
                args, _ = mock_get.call_args
                self.assertIn('application/nests/1/eggs', args[0])

        asyncio.run(run_test())

    def test_get_egg_info(self):
        async def run_test():
            with mock.patch('aiohttp.ClientSession.get') as mock_get:
                mock_response = mock.Mock()
                mock_response.json = mock.AsyncMock(return_value={'attributes': {'id': 2}})
                mock_response.status = 200
                mock_get.return_value.__aenter__.return_value = mock_response

                async with self.api as api:
                    await api.nests.get_egg_info(1, 2)
                
                args, _ = mock_get.call_args
                self.assertIn('application/nests/1/eggs/2', args[0])

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
