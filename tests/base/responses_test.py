import unittest
from copy import deepcopy
from unittest import mock

from pydactyl import PterodactylClient
from pydactyl.responses import Page, PaginatedResponse

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
LAST_PAGE_META = {
    'pagination':
        {'total': 106, 'count': 1, 'per_page': 25, 'current_page': 5,
         'total_pages': 5, 'links': {
            'previous': 'https://panel.mydomain.com/api/application/nodes/1'
                        '/allocations?page=4'}}}

MULTIPAGE_TEST_DATA = [
    {'data': ['thing1', 'thing2', 'sometimespage1isweird'], 'meta': TEST_META},
    {'data': ['thing3', 'thing4'], 'meta': TEST_META},
    {'data': ['thing84', 'thing97', 'fdas', 'pepperoni'], 'meta': TEST_META},
    {'data': ['one', 'two', 'three', 4, 5, '6'], 'meta': TEST_META},
    {'data': ['pineappleisanacceptablepizzatopping'],
     'meta': LAST_PAGE_META},
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

    def test_paginated_response_yields_page_objects(self):
        self.client._api_request = mock.MagicMock()
        self.client._api_request.side_effect = MULTIPAGE_TEST_DATA[1:]
        response = PaginatedResponse(self.client, 'asdf',
                                     MULTIPAGE_TEST_DATA[0])
        pages = list(response)
        self.assertEqual(len(MULTIPAGE_TEST_DATA), len(pages))
        for number, (page, expected) in enumerate(
                zip(pages, MULTIPAGE_TEST_DATA), start=1):
            self.assertIsInstance(page, Page)
            self.assertEqual(number, page.number)
            self.assertEqual(expected['data'], page.data)
            self.assertEqual(expected['meta'], page.meta)
            self.assertEqual(len(expected['data']), len(page))
            self.assertEqual(expected['data'], list(page))

    def test_paginated_response_requests_sequential_pages(self):
        self.client._api_request = mock.MagicMock()
        self.client._api_request.side_effect = MULTIPAGE_TEST_DATA[1:]
        response = PaginatedResponse(self.client, 'asdf',
                                     MULTIPAGE_TEST_DATA[0])
        list(response)
        self.assertEqual(
            [mock.call(endpoint='asdf', params={'page': n})
             for n in range(2, len(MULTIPAGE_TEST_DATA) + 1)],
            self.client._api_request.call_args_list)

    def test_paginated_response_can_be_iterated_repeatedly(self):
        self.client._api_request = mock.MagicMock()
        self.client._api_request.side_effect = (MULTIPAGE_TEST_DATA[1:]
                                                * 2)
        response = PaginatedResponse(self.client, 'asdf',
                                     MULTIPAGE_TEST_DATA[0])
        expected = [item for data in MULTIPAGE_TEST_DATA for item in
                    data['data']]
        self.assertListEqual(expected,
                             [item for page in response for item in page])
        self.assertListEqual(expected, response.collect())

    def test_paginated_response_data_is_first_page_after_iteration(self):
        self.client._api_request = mock.MagicMock()
        self.client._api_request.side_effect = MULTIPAGE_TEST_DATA[1:]
        response = PaginatedResponse(self.client, 'asdf',
                                     MULTIPAGE_TEST_DATA[0])
        list(response)
        self.assertEqual(MULTIPAGE_TEST_DATA[0]['data'], response.data)
        self.assertEqual(MULTIPAGE_TEST_DATA[0]['meta'], response.meta)

    def test_paginated_response_iter_of_iter_is_same_iterator(self):
        response = PaginatedResponse(self.client, 'anyendpoint', TEST_DATA)
        it = iter(response)
        self.assertIs(it, iter(it))

    def test_page_accessors(self):
        page = Page(TEST_DATA['data'], TEST_META, 1)
        self.assertEqual('data1', page[0]['dummy'])
        self.assertEqual(TEST_META, page['meta'])
        self.assertEqual(TEST_META, page.get('meta'))
        self.assertEqual('dflt', page.get('nope', 'dflt'))
        self.assertEqual(str(TEST_DATA['data']), str(page))
        self.assertEqual(TEST_META['pagination']['links']['next'],
                         page.get_next_page_link())
        self.assertEqual(TEST_META['pagination']['links']['previous'],
                         page.get_previous_page_link())
