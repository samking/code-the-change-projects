"""A utility for tests."""

import os
import unittest

import webtest

from google.appengine.ext import testbed

from ctc.models import user as user_model


class CtcTestCase(unittest.TestCase):
    """The base class for all Code the Change Projects tests."""

    def setUp(self):
        super(CtcTestCase, self).setUp()
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.logged_in_user = None
        # Only some stubs are initialized because we had trouble with some
        # testing environments.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_user_stub()

    def tearDown(self):
        super(CtcTestCase, self).tearDown()
        self.testbed.deactivate()

    def login(self):
        """Creates a user, logs in, and returns the user."""
        if not self.logged_in_user:
            self.logged_in_user = user_model.User(
                id='12345', email='test@codethechange.org')
            self.logged_in_user.put()
        self.testbed.setup_env(
            USER_EMAIL='test@codethechange.org',
            USER_ID=self.logged_in_user.key.id(),
            overwrite=True)
        return self.logged_in_user

    def logout(self):
        """Clears the currently logged in user."""
        self.testbed.setup_env(USER_EMAIL='', USER_ID='', overwrite=True)


class TestApp(webtest.TestApp):
    """A test app for sending requests to handlers that sets PATH_INFO."""

    def post(self, path, *args, **kwargs):
        """Adds PATH_INFO to the environment and sends a POST."""
        os.environ['PATH_INFO'] = path
        return super(TestApp, self).post(path, *args, **kwargs)

    def get(self, path, *args, **kwargs):
        """Adds PATH_INFO to the environment and sends a GET."""
        os.environ['PATH_INFO'] = path
        return super(TestApp, self).get(path, *args, **kwargs)
