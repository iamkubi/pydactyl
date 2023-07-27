import unittest
from copy import deepcopy
from unittest import mock

from pydactyl import PterodactylClient
from pydactyl.responses import PaginatedResponse

TEST_META = {
    'pagination':
        {'total': 106, 'count': 25, 'per_page': 25, 'current_page': 1,
         'total_pages': 5, 'links': {
            'next': 'https://panel.mydomain.com/api/application/nodes/1'
                    '/allocations?page=3',
            'previous': 'https://panel.mydomain.com/api/application/nodes/1'
                        '/allocations?page=1'}}}
TEST_DATA = {'data': [{'dummy': 'data1'}, {'dummy': 'data2'}], 'meta':
    TEST_META}

MULTIPAGE_TEST_DATA = [
    {'data': ['thing1', 'thing2', 'sometimespage1isweird'], 'meta': TEST_META},
    {'data': ['thing3', 'thing4'], 'meta': TEST_META},
    {'data': ['thing84', 'thing97', 'fdas', 'pepperoni'], 'meta': TEST_META},
    {'data': ['one', 'two', 'three', 4, 5, '6'], 'meta': TEST_META},
    {'data': ['pineappleisanacceptablepizzatopping'], 'meta': TEST_META},
]


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

    def test_paginated_response_get_nonexistant_item(self):
        response = PaginatedResponse(self.client, 'anyendpoint', TEST_DATA)
        self.assertEqual(response.get('fountainofyouth'), None)

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

    def test_paginated_response_fetches_first_page(self):
        expected = {
            'endpoint': 'api/asdf',
            'params': {'page': 2},
        }
        self.client._api_request = mock.MagicMock()
        response = PaginatedResponse(self.client, 'api/asdf', TEST_DATA)
        for _ in response:
            continue

        self.client._api_request.assert_called_with(**expected)

    def test_paginated_response_data_property_returns_data(self):
        response = PaginatedResponse(self.client, 'anyendpoint', TEST_DATA)
        self.assertEqual(response.data, TEST_DATA['data'])

    def test_paginated_response_str_method(self):
        response = PaginatedResponse(self.client, 'anyendpoint', TEST_DATA)
        self.assertEqual(str(response), str(TEST_DATA['data']))

    def test_paginated_response_collect_method(self):
        self.client._api_request = mock.MagicMock()
        self.client._api_request.side_effect = MULTIPAGE_TEST_DATA[1:]
        response = PaginatedResponse(self.client, 'asdf',
                                     MULTIPAGE_TEST_DATA[0])
        self.assertListEqual(
            response.collect(),
            [item for data in MULTIPAGE_TEST_DATA for item in data['data']])

    def test_paginated_response_multipage_iterator(self):
        self.client._api_request = mock.MagicMock()
        self.client._api_request.side_effect = MULTIPAGE_TEST_DATA[1:]
        response = PaginatedResponse(self.client, 'asdf',
                                     MULTIPAGE_TEST_DATA[0])
        expected = [item for data in MULTIPAGE_TEST_DATA for item in
                    data['data']]
        self.assertListEqual(expected,
                             [item for page in response for item in page])

    def test_paginated_response_has_correct_number_of_items(self):
        self.client._api_request = mock.MagicMock()
        self.client._api_request.side_effect = MULTIPAGE_TEST_DATA[1:]
        response = PaginatedResponse(self.client, 'asdf',
                                     MULTIPAGE_TEST_DATA[0])
        expected = [item for data in MULTIPAGE_TEST_DATA for item in
                    data['data']]
        expected_count = 16
        self.assertEqual(expected_count, len(expected))
        self.assertEqual(expected_count, len(response.collect()))

    def test_paginated_response_len(self):
        response = PaginatedResponse(self.client, 'anyendpoint', TEST_DATA)

        self.assertEqual(106, len(response))
