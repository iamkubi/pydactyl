import unittest
from copy import deepcopy

try:
    from unittest import mock
except ImportError:
    import mock

from pydactyl import PterodactylClient
from pydactyl.responses import PaginatedResponse

TEST_META = {
    'pagination':
        {'total': 106, 'count': 25, 'per_page': 25, 'current_page': 2,
         'total_pages': 5, 'links': {
            'next': 'https://panel.mydomain.com/api/application/nodes/1'
                    '/allocations?page=3',
            'previous': 'https://panel.mydomain.com/api/application/nodes/1'
                        '/allocations?page=1'}}}
TEST_DATA = {'data': [{'dummy': 'data1'}, {'dummy': 'data2'}], 'meta':
    TEST_META}


class PaginatedResponseTests(unittest.TestCase):

    def setUp(self):
        self.client = PterodactylClient(url='dummy', api_key='dummy')

    def test_paginated_response_init(self):
        response = PaginatedResponse(self.client, 'anyendpoint', TEST_DATA)

        self.assertEqual(response[0]['dummy'], 'data1')
        self.assertEqual(response[1]['dummy'], 'data2')

    def test_paginated_response_get(self):
        response = PaginatedResponse(self.client, 'anyendpoint', TEST_DATA)
        self.assertEqual(response.get('meta'), TEST_META)

    def test_paginated_response_get_with_default(self):
        response = PaginatedResponse(self.client, 'anyendpoint', TEST_DATA)
        self.assertEqual(response.get('badname', 'test_default'),
                         'test_default')

    def test_paginated_response_get_next_page_link(self):
        response = PaginatedResponse(self.client, 'anyendpoint', TEST_DATA)
        self.assertEqual(
            response.get_next_page_link(),
            'https://panel.mydomain.com/api/application/nodes/1/allocations'
            '?page=3')

    def test_paginated_response_get_previous_page_link(self):
        response = PaginatedResponse(self.client, 'anyendpoint', TEST_DATA)
        self.assertEqual(
            response.get_previous_page_link(),
            'https://panel.mydomain.com/api/application/nodes/1/allocations'
            '?page=1')

    def test_paginated_response_next_page_exists(self):
        self.assertTrue(PaginatedResponse._next_page_exists(TEST_META))

    def test_paginated_response_next_page_does_not_exist(self):
        data = deepcopy(TEST_META)
        self.assertTrue(PaginatedResponse._next_page_exists(data))
        del data['pagination']['links']['next']
        self.assertFalse(PaginatedResponse._next_page_exists(data))
