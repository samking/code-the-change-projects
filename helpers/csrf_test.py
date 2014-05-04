"""Tests for the CSRF helper."""

import unittest

import helpers.csrf
from testing import testutil


# Tests don't need docstrings, so pylint: disable=C0111
class CsrfTests(testutil.CtcTestCase):

    def test_get_csrf_key(self):
        csrf_key = helpers.csrf.get_csrf_key() 
        self.assertEqual(len(csrf_key), 32)
        second_key = helpers.csrf.get_csrf_key()
        self.assertEqual(csrf_key, second_key)


if __name__ == '__main__':
    unittest.main()
