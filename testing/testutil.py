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
        self.logged_in_user = None

    def tearDown(self):
        super(CtcTestCase, self).tearDown()
        self.testbed.deactivate()

    def login(self):
        """Creates a user, logs in, and returns the user."""
        if not self.logged_in_user:
            self.logged_in_user = models.user.User()
            self.logged_in_user.put()
        self.testbed.setup_env(
            USER_EMAIL='test@codethechange.org',
            USER_ID=str(self.logged_in_user.key.id()),
            overwrite=True)
        return self.logged_in_user

    def logout(self):
        """Clears the currently logged in user."""
        self.testbed.setup_env(USER_EMAIL='', USER_ID='', overwrite=True)
