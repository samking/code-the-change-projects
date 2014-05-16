"""A utility for tests."""

import unittest

from google.appengine.ext import testbed


class CtcTestCase(unittest.TestCase):
    """The base class for all Code the Change Projects tests."""

    def setUp(self):
        super(CtcTestCase, self).setUp()
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        # Only some stubs are initialized because we had trouble with some
        # testing environments.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_user_stub()

    def tearDown(self):
        super(CtcTestCase, self).tearDown()
        self.testbed.deactivate()
