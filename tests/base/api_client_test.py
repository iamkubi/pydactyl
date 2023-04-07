import logging
import unittest

from pydactyl.exceptions import ClientConfigError
from pydactyl import api_client


class ApiClientTests(unittest.TestCase):

    def test_pterodactyl_client_raises_without_required_params(self):
        with self.assertRaises(ClientConfigError):
            api_client.PterodactylClient(api_key='key', url=None)
        with self.assertRaises(ClientConfigError):
            api_client.PterodactylClient(api_key=None, url='url')

    def test_pterodactyl_client_debug_param(self):
        requests_log = logging.getLogger('requests.packages.urllib3')
        self.assertEqual(logging.NOTSET, requests_log.level)
        api_client.PterodactylClient('foo', 'bar', debug=True)
        self.assertEqual(logging.DEBUG, requests_log.level)
        api_client.PterodactylClient('foo', 'bar', debug=False)
        self.assertEqual(logging.NOTSET, requests_log.level)
