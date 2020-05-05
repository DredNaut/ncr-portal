import unittest
from ncr_portal_client import NCRPortalClient

class TestRun(unittest.TestCase):

    def test_query_action(self):
        portal = NCRPortalClient()
        self.assertEqual(portal.run("query", "cs447-jaredk"), ("query", "cs447-jaredk"))

    def test_reboot_action(self):
        portal = NCRPortalClient()
        self.assertEqual(portal.run("reboot", "cs447-jaredk"), ("reboot", "cs447-jaredk"))

    def test_shutdown_action(self):
        portal = NCRPortalClient()
        self.assertEqual(portal.run("shutdown", "cs447-jaredk"), ("shutdown", "cs447-jaredk"))

    def test_no_action(self):
        portal = NCRPortalClient()
        self.assertEqual(portal.run("", "cs447-jaredk"), None)

if __name__ == '__main__':
    unittest.main()
