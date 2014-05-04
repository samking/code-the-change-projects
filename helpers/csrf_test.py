"""Tests for the CSRF helper."""

import unittest

import mock

import helpers.csrf
from testing import testutil


# Tests don't need docstrings, so pylint: disable=C0111
# Tests can test protected members, so pylint: disable=W0212
class CsrfTests(testutil.CtcTestCase):

    # Helpers

    def test_get_secret_key(self):
        first_key = helpers.csrf._get_secret_key() 
        self.assertEqual(len(first_key), 32)
        second_key = helpers.csrf._get_secret_key()
        self.assertEqual(first_key, second_key)

    def test_tokens_are_equal(self):
        # It should fail if the tokens aren't equal length.
        self.assertFalse(helpers.csrf._tokens_are_equal('a', 'ab'))
        # It should fail if the tokens are different.
        self.assertFalse(helpers.csrf._tokens_are_equal('abcde', 'abcdf'))
        # It should succeed if the tokens are the same.
        self.assertTrue(helpers.csrf._tokens_are_equal('abcde', 'abcde'))


    # Make Token

    def test_make_token_includes_time(self):
        self.login()
        # It should get the current time.
        time_mock = mock.Mock()
        helpers.csrf.time = time_mock
        time_mock.time = mock.Mock(return_value=123)
        token1 = helpers.csrf.make_token()
        self.assertEqual(token1.split()[-1], '123')
        # It should use the provided time.
        token2 = helpers.csrf.make_token(token_time='456')
        self.assertEqual(token2.split()[-1], '456')
        # Different time should cause the digest to be different.
        self.assertNotEqual(token1.split()[0], token2.split()[0])
        token3 = helpers.csrf.make_token(token_time='456')
        self.assertEqual(token2, token3)

    def test_make_token_requires_login(self):
        token1 = helpers.csrf.make_token()
        self.assertIsNone(token1)
        self.login()
        token2 = helpers.csrf.make_token()
        self.assertIsNotNone(token2)

    def test_make_token_includes_path(self):
        self.login()
        # It should get the current path.
        self.testbed.setup_env(PATH_INFO='/action/1', overwrite=True)
        token1 = helpers.csrf.make_token(token_time='123')
        self.testbed.setup_env(PATH_INFO='/action/23', overwrite=True)
        token2 = helpers.csrf.make_token(token_time='123')
        token3 = helpers.csrf.make_token(token_time='123')
        self.assertNotEqual(token1, token2)
        self.assertEqual(token2, token3)
        # It should let the client pass in a path.
        token4 = helpers.csrf.make_token(path='/action/4', token_time='123')
        token5 = helpers.csrf.make_token(path='/action/56', token_time='123')
        token6 = helpers.csrf.make_token(path='/action/56', token_time='123')
        self.assertNotEqual(token4, token5)
        self.assertEqual(token5, token6)

    # Token Is Valid

    def test_token_is_valid(self):
        self.login()
        # Token is required.
        self.assertFalse(helpers.csrf.token_is_valid(None))
        # Token needs to have a timestamp on it.
        self.assertFalse(helpers.csrf.token_is_valid('hello'))
        # The timestamp needs to be within the current date range.
        time_mock = mock.Mock()
        helpers.csrf.time = time_mock
        time_mock.time = mock.Mock(return_value=9999999999999)
        self.assertFalse(helpers.csrf.token_is_valid('hello 123'))
        # The user needs to be logged in.
        token = helpers.csrf.make_token()
        self.logout()
        self.assertFalse(helpers.csrf.token_is_valid(token))
        self.login()
        # Modifying the token should break everything.
        modified_token = '0' + token[1:]
        if token == modified_token:
            modified_token = '1' + token[1:]
        self.assertFalse(helpers.csrf.token_is_valid(modified_token))
        # The original token that we got should work.
        self.assertTrue(helpers.csrf.token_is_valid(token))


if __name__ == '__main__':
    unittest.main()
