import unittest
from unittest import mock
import asyncio
from pydactyl.responses import Page, PaginatedResponse
from pydactyl.async_api_client import AsyncPterodactylClient

class AsyncPaginationTests(unittest.TestCase):

    def test_async_iteration(self):
        async def run_test():
            # Mock client and api_request
            client = mock.Mock(spec=AsyncPterodactylClient)
            # api_request must return a coroutine
            client._api_request = mock.AsyncMock()
            
            # Setup first page data
            data = {
                'data': [{'id': 1}],
                'meta': {
                    'pagination': {
                        'total': 2,
                        'links': {'next': 'http://next'}
                    }
                }
            }
            
            # Setup second page response
            second_page_response = {
                'data': [{'id': 2}],
                'meta': {
                    'pagination': {
                        'total': 2,
                        'links': {'next': ''}
                    }
                }
            }
            
            client._api_request.return_value = second_page_response
            
            paginated = PaginatedResponse(client, 'endpoint', data)
            
            items = []
            async for page in paginated:
                items.extend(page.data)
                
            self.assertEqual(len(items), 2)
            self.assertEqual(items[0]['id'], 1)
            self.assertEqual(items[1]['id'], 2)
            
        asyncio.run(run_test())

    def test_collect_async(self):
        async def run_test():
            client = mock.Mock(spec=AsyncPterodactylClient)
            client._api_request = mock.AsyncMock()
            
            data = {
                'data': [{'id': 1}],
                'meta': {
                    'pagination': {
                        'total': 2,
                        'links': {'next': 'http://next'}
                    }
                }
            }
             
            second_page_response = {
                'data': [{'id': 2}],
                'meta': {
                    'pagination': {
                        'total': 2,
                        'links': {'next': ''}
                    }
                }
            }
            
            client._api_request.return_value = second_page_response
            
            paginated = PaginatedResponse(client, 'endpoint', data)
            
            items = await paginated.collect_async()
            
            self.assertEqual(len(items), 2)
            self.assertEqual(items[0]['id'], 1)
            self.assertEqual(items[1]['id'], 2)

        asyncio.run(run_test())

    def test_async_iteration_repeatable_and_yields_pages(self):
        async def run_test():
            client = mock.Mock(spec=AsyncPterodactylClient)
            client._api_request = mock.AsyncMock()
            data = {'data': [{'id': 1}],
                    'meta': {'pagination': {
                        'total': 2, 'links': {'next': 'http://next'}}}}
            client._api_request.return_value = {
                'data': [{'id': 2}],
                'meta': {'pagination': {'total': 2, 'links': {'next': ''}}}}

            paginated = PaginatedResponse(client, 'endpoint', data)

            for _ in range(2):
                pages = [page async for page in paginated]
                self.assertTrue(all(isinstance(p, Page) for p in pages))
                self.assertEqual([1, 2], [p.number for p in pages])
                self.assertEqual([{'id': 1}, {'id': 2}],
                                 [item for p in pages for item in p])
            self.assertEqual(2, client._api_request.await_count)
            self.assertEqual(data['data'], paginated.data)

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
