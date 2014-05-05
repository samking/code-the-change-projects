"""A utility for tests."""

import unittest

from google.appengine.ext import testbed


class CtcTestCase(unittest.TestCase):
    """The base class for all Code the Change Projects tests."""

    def setUp(self):
        super(CtcTestCase, self).setUp()
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        # It's annoying to have to figure out the right stub while you're
        # writing tests, so initialize ALL the stubs!
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_user_stub()

    def tearDown(self):
        super(CtcTestCase, self).tearDown()
        self.testbed.deactivate()
