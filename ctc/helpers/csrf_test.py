"""Tests for the CSRF helper."""

import unittest

import mock
import webapp2
import webtest

from ctc.helpers import csrf
from ctc.testing import testutil


MOCKED_TIME = 123


# Tests don't need docstrings, so pylint: disable=C0111
# Tests can test protected members, so pylint: disable=W0212
class CsrfTests(testutil.CtcTestCase):

    # Helpers

    class TestHandler(csrf.CsrfHandler):
        """A handler for testing whether or not requests are CSRF protected."""

        def get(self):
            self.response.write('CSRF Token:%s' % self.csrf_token)

        def post(self):
            pass

        def put(self):
            pass

        def delete(self):
            pass

    def setUp(self):
        super(CsrfTests, self).setUp()
        # The CSRF library uses the time, so we mock it out.
        self.time_mock = mock.Mock()
        csrf.time = self.time_mock
        self.time_mock.time = mock.Mock(return_value=MOCKED_TIME)
        # The handler tests need a WSGIApplication.
        app = webapp2.WSGIApplication([('/', self.TestHandler)])
        self.testapp = webtest.TestApp(app)

    def test_get_secret_key(self):
        first_key = csrf._get_secret_key()
        self.assertEqual(len(first_key), 32)
        second_key = csrf._get_secret_key()
        self.assertEqual(first_key, second_key)

    def test_tokens_are_equal(self):
        # It should fail if the tokens aren't equal length.
        self.assertFalse(csrf._tokens_are_equal('a', 'ab'))
        # It should fail if the tokens are different.
        self.assertFalse(csrf._tokens_are_equal('abcde', 'abcdf'))
        # It should succeed if the tokens are the same.
        self.assertTrue(csrf._tokens_are_equal('abcde', 'abcde'))

    # Make Token

    def test_make_token_includes_time(self):
        self.login()
        # It should get the current time.
        token1 = csrf.make_token()
        self.assertEqual(token1.split()[-1], str(MOCKED_TIME))
        # It should use the provided time.
        token2 = csrf.make_token(token_time='456')
        self.assertEqual(token2.split()[-1], '456')
        # Different time should cause the digest to be different.
        self.assertNotEqual(token1.split()[0], token2.split()[0])
        token3 = csrf.make_token(token_time='456')
        self.assertEqual(token2, token3)

    def test_make_token_requires_login(self):
        token1 = csrf.make_token()
        self.assertIsNone(token1)
        self.login()
        token2 = csrf.make_token()
        self.assertIsNotNone(token2)

    def test_make_token_includes_path(self):
        self.login()
        # It should get the current path.
        self.testbed.setup_env(PATH_INFO='/action/1', overwrite=True)
        token1 = csrf.make_token(token_time='123')
        self.testbed.setup_env(PATH_INFO='/action/23', overwrite=True)
        token2 = csrf.make_token(token_time='123')
        token3 = csrf.make_token(token_time='123')
        self.assertNotEqual(token1, token2)
        self.assertEqual(token2, token3)
        # It should let the client pass in a path.
        token4 = csrf.make_token(path='/action/4', token_time='123')
        token5 = csrf.make_token(path='/action/56', token_time='123')
        token6 = csrf.make_token(path='/action/56', token_time='123')
        self.assertNotEqual(token4, token5)
        self.assertEqual(token5, token6)

    # Token Is Valid

    def test_token_is_valid(self):
        self.login()
        # Token is required.
        self.assertFalse(csrf.token_is_valid(None))
        # Token needs to have a timestamp on it.
        self.assertFalse(csrf.token_is_valid('hello'))
        # The timestamp needs to be within the current date range.
        self.time_mock.time = mock.Mock(return_value=9999999999999)
        self.assertFalse(csrf.token_is_valid('hello 123'))
        # The user needs to be logged in.
        token = csrf.make_token()
        self.logout()
        self.assertFalse(csrf.token_is_valid(token))
        self.login()
        # Modifying the token should break everything.
        modified_token = '0' + token[1:]
        if token == modified_token:
            modified_token = '1' + token[1:]
        self.assertFalse(csrf.token_is_valid(modified_token))
        # The original token that we got should work.
        self.assertTrue(csrf.token_is_valid(token))

    def test_get_has_csrf_token(self):
        self.login()
        response = self.testapp.get('/', status=200).body
        self.assertIn('CSRF Token:', response)
        self.assertEqual(response.split(':')[-1], csrf.make_token())

    def test_mutators_require_csrf_token(self):
        self.login()
        self.testapp.put('/', status=403)
        self.testapp.post('/', status=403)
        self.testapp.delete('/', status=403)
        csrf_param = 'csrf_token=' + csrf.make_token(path='/')
        self.testapp.put('/', params=csrf_param, status=200)
        self.testapp.post('/', params=csrf_param, status=200)
        # Though the spec allows DELETE to have a body, it tends to be ignored
        # by servers (http://stackoverflow.com/questions/299628), and webapp2
        # ignores it as well, so we have to put the params in the URL.
        self.testapp.delete('/?' + csrf_param, status=200)


if __name__ == '__main__':
    unittest.main()
