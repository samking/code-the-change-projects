"""A utility for tests."""

import unittest

from google.appengine.ext import testbed

import models.user


class CtcTestCase(unittest.TestCase):
    """The base class for all Code the Change Projects tests."""

    def setUp(self):
        super(CtcTestCase, self).setUp()
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        # It's annoying to have to figure out the right stub while you're
        # writing tests, so initialize ALL the stubs!
        self.testbed.init_all_stubs()

    def tearDown(self):
        super(CtcTestCase, self).tearDown()
        self.testbed.deactivate()

    def login(self):
        """Creates a user, logs in, and returns the user."""
        user = models.user.User()
        user.put()
        self.testbed.setup_env(
            USER_EMAIL='test@codethechange.org',
            USER_ID=str(user.key.id()),
            overwrite=True)
        return user

