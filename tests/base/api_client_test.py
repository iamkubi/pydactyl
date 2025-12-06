import unittest

from pydactyl.exceptions import ClientConfigError
from pydactyl import api_client


class ApiClientTests(unittest.TestCase):

    def test_pterodactyl_client_raises_without_required_params(self):
        with self.assertRaises(ClientConfigError):
            api_client.PterodactylClient(api_key='key', url=None)
        with self.assertRaises(ClientConfigError):
            api_client.PterodactylClient(api_key=None, url='url')
