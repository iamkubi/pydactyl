import unittest

from pydactyl import PterodactylClient


class NodesTests(unittest.TestCase):

    def setUp(self):
        self.client = PterodactylClient(url='dummy', api_key='dummy')
