import unittest
from unittest import mock

from requests import Session

from pydactyl.api import base


class BaseTests(unittest.TestCase):

    def setUp(self):
        self.api = base.PterodactylAPI(url='https://dummy.com',
                                       api_key='dummy_key')

    def test_init(self):
        self.assertEqual('dummy_key', self.api._api_key)
        self.assertEqual('https://dummy.com', self.api._url)

    def test_get_headers(self):
        expected = {
            'Authorization': 'Bearer dummy_key',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        self.assertDictEqual(expected, self.api._get_headers())

    def test_url_join(self):
        self.assertEqual('www.test.com/path', base.url_join(
            'www.test.com', 'path'))
        self.assertEqual('test.com/path/to/thing',
                         base.url_join('test.com', 'path', 'to', 'thing'))
        self.assertEqual('https://asdf.com/api/other/things',
                         base.url_join('https://asdf.com', '/api/',
                                       'other/things'))

    def test_parse_response_with_detail(self):
        expected = {'object': 'server', 'attributes': {'id': 12}}
        self.assertEqual(expected, base.parse_response(expected, detail=True))

    def test_parse_response_without_detail(self):
        expected = {'id': 12}
        response = {'object': 'server', 'attributes': {'id': 12}}
        self.assertEqual(expected, base.parse_response(response, detail=False))

    def test_parse_response_list_object_with_detail(self):
        expected = {'object': 'list',
                    'data': [{'object': 'server', 'attributes': {'id': 5}},
                             {'object': 'server', 'attributes': {'id': 6}}]}
        self.assertEqual(expected, base.parse_response(expected, detail=True))

    def test_parse_response_list_object_without_detail(self):
        expected = [{'id': 5}, {'id': 6}]
        response = {'object': 'list',
                    'data': [{'object': 'server', 'attributes': {'id': 5}},
                             {'object': 'server', 'attributes': {'id': 6}}]}
        self.assertEqual(expected, base.parse_response(response, detail=False))

    @mock.patch.object(Session, 'get')
    def test_valid_api_get_request(self, mock_request):
        expected = {
            'params': None,
            'headers': self.api._get_headers(),
        }
        self.api._api_request(endpoint='nomorecoffee')
        mock_request.assert_called_with('https://dummy.com/api/nomorecoffee',
                                        **expected)

    @mock.patch.object(Session, 'post')
    def test_valid_api_post_request(self, mock_request):
        data = {'test': 'data'}
        expected = {
            'params': None,
            'headers': self.api._get_headers(),
        }
        self.api._api_request(endpoint='foo', mode='POST', data=data)
        mock_request.assert_called_with('https://dummy.com/api/foo', json=data,
                                        **expected)

    @mock.patch.object(Session, 'patch')
    def test_valid_api_patch_request(self, mock_request):
        data = {'patch': 'me'}
        expected = {
            'params': None,
            'headers': self.api._get_headers(),
            'json': data,
        }
        self.api._api_request(endpoint='bar', mode='PATCH', data=data)
        mock_request.assert_called_with('https://dummy.com/api/bar', **expected)

    @mock.patch.object(Session, 'delete')
    def test_valid_api_delete_request(self, mock_request):
        expected = {
            'params': None,
            'headers': self.api._get_headers(),
        }
        self.api._api_request(endpoint='havecoffee', mode='DELETE')
        mock_request.assert_called_with('https://dummy.com/api/havecoffee',
                                        **expected)

    @mock.patch.object(Session, 'put')
    def test_valid_api_put_request(self, mock_request):
        data = {'put': 'me'}
        expected = {
            'params': None,
            'headers': self.api._get_headers(),
            'json': data,
        }
        self.api._api_request(endpoint='putstuff', mode='PUT', data=data)
        mock_request.assert_called_with('https://dummy.com/api/putstuff',
                                        **expected)

    @mock.patch.object(Session, 'post')
    def test_api_request_with_override_headers(self, mock_request):
        data = {'dummy': 'asdf'}
        expected_headers = self.api._get_headers()
        expected_headers['Content-Type'] = 'application/text'
        expected = {
            'params': None,
            'headers': expected_headers,
            'json': data,
        }
        self.api._api_request(
            endpoint='overridetest', mode='POST', data=data,
            override_headers={'Content-Type': 'application/text'})
        mock_request.assert_called_with('https://dummy.com/api/overridetest',
                                        **expected)
