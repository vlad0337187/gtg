from unittest import TestCase

from GTG.tools.networkmanager import is_connection_up


class TestNetworkManager(TestCase):

    def test_is_connection_up_and_doesnt_throw_exception(self):
        self.assertIn(is_connection_up(), [True, False])
